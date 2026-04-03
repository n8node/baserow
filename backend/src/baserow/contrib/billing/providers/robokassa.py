import hashlib
from decimal import Decimal
from typing import Optional
from urllib.parse import urlencode

from baserow.contrib.billing.models import PaymentProviderConfig
from baserow.contrib.billing.providers.base import PaymentProviderBase


class RobokassaProvider(PaymentProviderBase):
    LIVE_URL = "https://auth.robokassa.ru/Merchant/Index.aspx"
    TEST_URL = "https://auth.robokassa.ru/Merchant/Index.aspx"

    def __init__(self, config: PaymentProviderConfig):
        self.config = config

    def _sign(self, *parts: str) -> str:
        raw = ":".join(str(p) for p in parts)
        return hashlib.md5(raw.encode("utf-8")).hexdigest()

    def create_payment_url(
        self,
        invoice_id: int,
        amount: Decimal,
        description: str,
        email: str = "",
        **kwargs,
    ) -> str:
        out_sum = f"{amount:.2f}"
        signature = self._sign(
            self.config.merchant_login,
            out_sum,
            invoice_id,
            self.config.password1,
        )

        params = {
            "MerchantLogin": self.config.merchant_login,
            "OutSum": out_sum,
            "InvId": invoice_id,
            "Description": description[:250],
            "SignatureValue": signature,
            "Culture": "ru",
        }
        if email:
            params["Email"] = email
        if self.config.test_mode:
            params["IsTest"] = 1

        return f"{self.LIVE_URL}?{urlencode(params)}"

    def verify_callback(self, data: dict) -> bool:
        out_sum = data.get("OutSum", "")
        inv_id = data.get("InvId", "")
        received_sig = data.get("SignatureValue", "")

        expected = self._sign(out_sum, inv_id, self.config.password2)
        return expected.lower() == received_sig.lower()

    def get_payment_id_from_callback(self, data: dict) -> Optional[str]:
        return data.get("InvId")

    def get_invoice_id_from_callback(self, data: dict) -> Optional[int]:
        try:
            return int(data.get("InvId", 0))
        except (ValueError, TypeError):
            return None

    def success_response(self, inv_id) -> str:
        return f"OK{inv_id}"
