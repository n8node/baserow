from decimal import Decimal
from urllib.parse import parse_qs, urlparse

import pytest

from baserow.contrib.billing.models import PaymentProviderConfig
from baserow.contrib.billing.providers.robokassa import RobokassaProvider


@pytest.fixture
def robokassa_config(db):
    return PaymentProviderConfig.objects.create(
        provider_type=PaymentProviderConfig.ProviderType.ROBOKASSA,
        merchant_login="demo",
        password1="password_1",
        password2="password_2",
        test_mode=False,
        hash_algorithm="md5",
        fiscalization_enabled=False,
    )


@pytest.mark.django_db
def test_create_payment_url_signature_matches_official_formula(robokassa_config):
    """
    Official sample: md5("MerchantLogin:OutSum:InvId:Password1").
    https://docs.robokassa.ru/ru/pay-interface
    """
    provider = RobokassaProvider(robokassa_config)
    url = provider.create_payment_url(
        invoice_id=12,
        amount=Decimal("990.00"),
        description="Оплата заказа №12",
        email="buyer@example.com",
    )

    query = parse_qs(urlparse(url).query)
    assert query["MerchantLogin"] == ["demo"]
    assert query["OutSum"] == ["990.00"]
    assert query["InvId"] == ["12"]
    assert "IsTest" not in query

    # md5("demo:990.00:12:password_1") from Robokassa docs style
    import hashlib

    expected = hashlib.md5(b"demo:990.00:12:password_1").hexdigest().upper()
    assert query["SignatureValue"] == [expected]


@pytest.mark.django_db
def test_create_payment_url_strips_credentials_and_sets_test_flag(db):
    config = PaymentProviderConfig.objects.create(
        provider_type=PaymentProviderConfig.ProviderType.ROBOKASSA,
        merchant_login="  demo  ",
        password1="  password_1  ",
        password2="password_2",
        test_mode=True,
    )
    provider = RobokassaProvider(config)
    url = provider.create_payment_url(
        invoice_id=5,
        amount=Decimal("1200"),
        description="Популярный (monthly)",
    )
    query = parse_qs(urlparse(url).query)
    assert query["MerchantLogin"] == ["demo"]
    assert query["OutSum"] == ["1200.00"]
    assert query["IsTest"] == ["1"]

    import hashlib

    expected = hashlib.md5(b"demo:1200.00:5:password_1").hexdigest().upper()
    assert query["SignatureValue"] == [expected]


@pytest.mark.django_db
def test_create_payment_url_sha256_when_configured(robokassa_config):
    robokassa_config.hash_algorithm = "sha256"
    robokassa_config.save(update_fields=["hash_algorithm"])
    provider = RobokassaProvider(robokassa_config)
    url = provider.create_payment_url(
        invoice_id=1,
        amount=Decimal("10.00"),
        description="Test",
    )
    query = parse_qs(urlparse(url).query)

    import hashlib

    expected = hashlib.sha256(b"demo:10.00:1:password_1").hexdigest().upper()
    assert query["SignatureValue"] == [expected]


@pytest.mark.django_db
def test_create_payment_url_includes_receipt_in_signature(robokassa_config):
    from urllib.parse import quote

    robokassa_config.fiscalization_enabled = True
    robokassa_config.receipt_tax = "none"
    robokassa_config.save(
        update_fields=["fiscalization_enabled", "receipt_tax"]
    )
    provider = RobokassaProvider(robokassa_config)
    url = provider.create_payment_url(
        invoice_id=7,
        amount=Decimal("100.00"),
        description="Service",
    )
    query = parse_qs(urlparse(url).query)
    assert "Receipt" in query

    receipt = query["Receipt"][0]
    receipt_for_sign = quote(receipt, safe="")

    import hashlib

    raw = f"demo:100.00:7:{receipt_for_sign}:password_1"
    expected = hashlib.md5(raw.encode("utf-8")).hexdigest().upper()
    assert query["SignatureValue"] == [expected]


@pytest.mark.django_db
def test_verify_callback_uses_password2(robokassa_config):
    provider = RobokassaProvider(robokassa_config)
    import hashlib

    out_sum = "1200.00"
    inv_id = "42"
    sig = hashlib.md5(f"{out_sum}:{inv_id}:password_2".encode()).hexdigest()
    assert provider.verify_callback(
        {"OutSum": out_sum, "InvId": inv_id, "SignatureValue": sig}
    )
    assert not provider.verify_callback(
        {"OutSum": out_sum, "InvId": inv_id, "SignatureValue": "deadbeef"}
    )


@pytest.mark.django_db
def test_format_out_sum_consistent():
    assert RobokassaProvider.format_out_sum(Decimal("1200")) == "1200.00"
    assert RobokassaProvider.format_out_sum("1200.5") == "1200.50"
    assert RobokassaProvider.format_out_sum(10) == "10.00"
