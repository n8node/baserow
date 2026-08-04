import hashlib
import json
import re
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Union
from urllib.parse import quote, urlencode

from baserow.contrib.billing.models import PaymentProviderConfig
from baserow.contrib.billing.providers.base import PaymentProviderBase

# Robokassa algorithms from merchant «Технические настройки».
_HASH_FUNCS = {
    "md5": hashlib.md5,
    "sha1": hashlib.sha1,
    "sha256": hashlib.sha256,
    "sha384": hashlib.sha384,
    "sha512": hashlib.sha512,
}


class RobokassaProvider(PaymentProviderBase):
    """Robokassa signatures per https://docs.robokassa.ru/ru/pay-interface"""

    LIVE_URL = "https://auth.robokassa.ru/Merchant/Index.aspx"

    def __init__(self, config: PaymentProviderConfig):
        self.config = config

    @property
    def merchant_login(self) -> str:
        return (self.config.merchant_login or "").strip()

    @property
    def password1(self) -> str:
        return (self.config.password1 or "").strip()

    @property
    def password2(self) -> str:
        return (self.config.password2 or "").strip()

    @property
    def hash_algorithm(self) -> str:
        algo = (getattr(self.config, "hash_algorithm", None) or "md5").strip().lower()
        return algo if algo in _HASH_FUNCS else "md5"

    def _sign(self, *parts: str) -> str:
        raw = ":".join(str(p) for p in parts)
        digest = _HASH_FUNCS[self.hash_algorithm](raw.encode("utf-8")).hexdigest()
        # Robokassa accepts either case; uppercase matches official PHP samples.
        return digest.upper()

    @staticmethod
    def format_out_sum(amount: Union[Decimal, str, float, int]) -> str:
        """OutSum must use a dot decimal separator and match the signed value."""
        value = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return f"{value:.2f}"

    @staticmethod
    def _sanitize_description(description: str, max_len: int = 100) -> str:
        # Docs: up to 100 chars, without special characters.
        cleaned = re.sub(r"[^\w\s\-.,а-яА-ЯёЁ]+", " ", description or "", flags=re.UNICODE)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        return cleaned[:max_len] or "Baserow subscription"

    def _build_receipt(self, out_sum: str, description: str) -> Optional[str]:
        """
        Compact JSON for 54-FZ fiscalization. Included in SignatureValue when set.

        Signature uses URL-encoded JSON; the request param is raw JSON (encoded once
        by urlencode).
        """
        if not getattr(self.config, "fiscalization_enabled", False):
            return None

        tax = (getattr(self.config, "receipt_tax", None) or "none").strip() or "none"
        sno = (getattr(self.config, "receipt_sno", None) or "").strip()
        item = {
            "name": description[:128],
            "quantity": 1,
            "sum": float(out_sum),
            "tax": tax,
            "payment_object": "service",
            "payment_method": "full_prepayment",
        }
        receipt: dict = {"items": [item]}
        if sno:
            receipt["sno"] = sno
        return json.dumps(receipt, ensure_ascii=False, separators=(",", ":"))

    def create_payment_url(
        self,
        invoice_id: int,
        amount: Decimal,
        description: str,
        email: str = "",
        **kwargs,
    ) -> str:
        if not self.merchant_login:
            raise ValueError("Robokassa MerchantLogin is not configured.")
        if not self.password1:
            raise ValueError("Robokassa Password #1 is not configured.")

        out_sum = self.format_out_sum(amount)
        inv_id = str(int(invoice_id))
        desc = self._sanitize_description(description)
        receipt_json = self._build_receipt(out_sum, desc)

        # MerchantLogin:OutSum:InvId[:Receipt]:Password#1
        sign_parts: list[str] = [self.merchant_login, out_sum, inv_id]
        if receipt_json is not None:
            # Docs: URL-encode Receipt before inserting into the signature string.
            sign_parts.append(quote(receipt_json, safe=""))
        sign_parts.append(self.password1)
        signature = self._sign(*sign_parts)

        params = {
            "MerchantLogin": self.merchant_login,
            "OutSum": out_sum,
            "InvId": inv_id,
            "Description": desc,
            "SignatureValue": signature,
            "Culture": "ru",
            "Encoding": "utf-8",
        }
        if receipt_json is not None:
            params["Receipt"] = receipt_json
        if email:
            params["Email"] = email.strip()
        # IsTest=1 requires the *test* Password#1/#2 pair from Robokassa cabinet.
        # Using live passwords with IsTest=1 yields error 29.
        if self.config.test_mode:
            params["IsTest"] = "1"

        return f"{self.LIVE_URL}?{urlencode(params, doseq=True, encoding='utf-8')}"

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
        if not received_sig or not self.password2:
            return False

        expected = self._sign(out_sum, inv_id, self.password2)
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
