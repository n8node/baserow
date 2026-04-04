import hashlib
from decimal import Decimal
from typing import Optional
from urllib.parse import urlencode

from baserow.contrib.billing.models import PaymentProviderConfig
from baserow.contrib.billing.providers.base import PaymentProviderBase


class RobokassaProvider(PaymentProviderBase):
    """Robokassa MD5 signatures per https://docs.robokassa.ru/ru/notifications-and-redirects"""

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

    @staticmethod
    def normalize_callback_payload(data: dict) -> dict:
        """
        Robokassa usually sends InvId / OutSum / SignatureValue; tolerate variants
        and trim the signature (docs: hex 0-9A-F).
        """

        if not data:
            return {}
        out = {k: v for k, v in data.items() if v is not None}

        aliases_inv = ("InvID", "invid", "invoice_id", "InvoiceID")
        if not out.get("InvId"):
            for key in aliases_inv:
                if out.get(key) not in (None, ""):
                    out["InvId"] = out[key]
                    break

        aliases_sum = ("out_summ", "Outsumm")
        if not out.get("OutSum"):
            for key in aliases_sum:
                if out.get(key) not in (None, ""):
                    out["OutSum"] = out[key]
                    break

        aliases_sig = ("crc", "Signature")
        if not out.get("SignatureValue"):
            for key in aliases_sig:
                if out.get(key) not in (None, ""):
                    out["SignatureValue"] = out[key]
                    break

        sig = out.get("SignatureValue")
        if isinstance(sig, str):
            out["SignatureValue"] = sig.strip()

        return out

    def verify_callback(self, data: dict) -> bool:
        data = self.normalize_callback_payload(data)
        out_sum = data.get("OutSum", "")
        inv_id = data.get("InvId", "")
        received_sig = data.get("SignatureValue", "")

        expected = self._sign(out_sum, inv_id, self.config.password2)
        return expected.lower() == received_sig.lower()

    def get_payment_id_from_callback(self, data: dict) -> Optional[str]:
        data = self.normalize_callback_payload(data)
        raw = data.get("InvId")
        return str(raw) if raw not in (None, "") else None

    def get_invoice_id_from_callback(self, data: dict) -> Optional[int]:
        data = self.normalize_callback_payload(data)
        raw = data.get("InvId")
        if raw is None or raw == "":
            return None
        try:
            return int(raw)
        except (ValueError, TypeError):
            return None

    def success_response(self, inv_id) -> str:
        return f"OK{inv_id}"
