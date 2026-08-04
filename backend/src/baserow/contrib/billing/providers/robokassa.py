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

    def test_connection(self) -> dict:
        """
        Verify Robokassa merchant credentials against XML interfaces.

        - GetCurrencies → MerchantLogin exists / shop active
        - OpStateExt → Password #2 + hash algorithm (Result 0 or 3 = signature OK)
        - Password #1 → only checked as present; used when building payment links
        """
        import re as _re
        import urllib.error
        import urllib.request
        import xml.etree.ElementTree as ET

        checks: list[dict] = []
        ok = True

        if not self.merchant_login:
            return {
                "ok": False,
                "message": "MerchantLogin не задан.",
                "checks": [],
                "test_mode": bool(self.config.test_mode),
                "hash_algorithm": self.hash_algorithm,
            }
        if not self.password1:
            return {
                "ok": False,
                "message": "Password #1 не задан.",
                "checks": [],
                "test_mode": bool(self.config.test_mode),
                "hash_algorithm": self.hash_algorithm,
            }
        if not self.password2:
            return {
                "ok": False,
                "message": "Password #2 не задан.",
                "checks": [],
                "test_mode": bool(self.config.test_mode),
                "hash_algorithm": self.hash_algorithm,
            }

        def _http_get(url: str) -> str:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Baserow-Robokassa-Check/1.0"},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=20) as resp:
                return resp.read().decode("utf-8", errors="replace")

        def _result_code(xml_text: str) -> tuple[Optional[int], str]:
            try:
                root = ET.fromstring(xml_text)
            except ET.ParseError:
                return None, "Некорректный XML-ответ Robokassa"
            # Namespace-agnostic search for Result/Code
            code_el = None
            for el in root.iter():
                tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag
                if tag == "Code" and code_el is None:
                    # Prefer Result/Code: walk parents is awkward; take first Code
                    # under an element named Result if possible.
                    code_el = el
            # Prefer Code inside Result
            for el in root.iter():
                tag = el.tag.split("}")[-1] if "}" in el.tag else el.tag
                if tag == "Result":
                    for child in el:
                        ctag = child.tag.split("}")[-1] if "}" in child.tag else child.tag
                        if ctag == "Code" and child.text is not None:
                            try:
                                return int(child.text.strip()), ""
                            except ValueError:
                                return None, f"Неверный Result.Code: {child.text}"
            if code_el is not None and code_el.text:
                try:
                    return int(code_el.text.strip()), ""
                except ValueError:
                    return None, f"Неверный Code: {code_el.text}"
            snippet = _re.sub(r"\s+", " ", xml_text)[:200]
            return None, f"Result.Code не найден ({snippet})"

        # 1) MerchantLogin via GetCurrencies
        currencies_url = (
            "https://auth.robokassa.ru/Merchant/WebService/Service.asmx/"
            f"GetCurrencies?MerchantLogin={quote(self.merchant_login, safe='')}"
            "&Language=ru"
        )
        try:
            currencies_xml = _http_get(currencies_url)
            code, err = _result_code(currencies_xml)
            if err:
                checks.append(
                    {
                        "name": "merchant_login",
                        "ok": False,
                        "detail": err,
                    }
                )
                ok = False
            elif code == 0:
                checks.append(
                    {
                        "name": "merchant_login",
                        "ok": True,
                        "detail": "Магазин найден (GetCurrencies).",
                    }
                )
            elif code == 2:
                checks.append(
                    {
                        "name": "merchant_login",
                        "ok": False,
                        "detail": "Магазин не найден или не активирован (код 2).",
                    }
                )
                ok = False
            else:
                checks.append(
                    {
                        "name": "merchant_login",
                        "ok": False,
                        "detail": f"GetCurrencies вернул код {code}.",
                    }
                )
                ok = False
        except urllib.error.HTTPError as exc:
            checks.append(
                {
                    "name": "merchant_login",
                    "ok": False,
                    "detail": f"HTTP {exc.code} при GetCurrencies.",
                }
            )
            ok = False
        except Exception as exc:  # noqa: BLE001 — surface any network failure
            checks.append(
                {
                    "name": "merchant_login",
                    "ok": False,
                    "detail": f"Сеть: {exc}",
                }
            )
            ok = False

        # 2) Password #2 + hash via OpStateExt (nonexistent invoice)
        probe_invoice = "2147483646"
        signature = self._sign(self.merchant_login, probe_invoice, self.password2)
        opstate_url = (
            "https://auth.robokassa.ru/Merchant/WebService/Service.asmx/"
            f"OpStateExt?MerchantLogin={quote(self.merchant_login, safe='')}"
            f"&InvoiceID={probe_invoice}"
            f"&Signature={signature}"
        )
        try:
            opstate_xml = _http_get(opstate_url)
            code, err = _result_code(opstate_xml)
            if err:
                checks.append({"name": "password2", "ok": False, "detail": err})
                ok = False
            elif code == 1:
                checks.append(
                    {
                        "name": "password2",
                        "ok": False,
                        "detail": (
                            "Неверная подпись (код 1): проверьте Password #2 и "
                            f"алгоритм хеша ({self.hash_algorithm}). "
                            "В тестовом режиме нужны тестовые пароли."
                        ),
                    }
                )
                ok = False
            elif code == 2:
                checks.append(
                    {
                        "name": "password2",
                        "ok": False,
                        "detail": "Магазин не найден при OpStateExt (код 2).",
                    }
                )
                ok = False
            elif code in (0, 3, 4):
                # 3 = invoice not found → signature accepted
                checks.append(
                    {
                        "name": "password2",
                        "ok": True,
                        "detail": (
                            f"Password #2 и {self.hash_algorithm.upper()} "
                            f"приняты Robokassa (OpStateExt код {code})."
                        ),
                    }
                )
            else:
                checks.append(
                    {
                        "name": "password2",
                        "ok": False,
                        "detail": f"OpStateExt вернул код {code}.",
                    }
                )
                ok = False
        except Exception as exc:  # noqa: BLE001
            checks.append(
                {
                    "name": "password2",
                    "ok": False,
                    "detail": f"Сеть OpStateExt: {exc}",
                }
            )
            ok = False

        checks.append(
            {
                "name": "password1",
                "ok": True,
                "detail": (
                    "Password #1 задан и будет использован в SignatureValue "
                    "платёжной ссылки (удалённо не проверяется без создания платежа)."
                ),
            }
        )

        if self.config.test_mode:
            mode_note = (
                "Включён тестовый режим (IsTest=1): в кабинете Robokassa должны "
                "быть указаны именно тестовые Password #1/#2."
            )
        else:
            mode_note = "Боевой режим: используйте основные (не тестовые) пароли."

        if ok:
            message = f"Соединение с Robokassa успешно. {mode_note}"
        else:
            message = f"Проверка не пройдена. {mode_note}"

        return {
            "ok": ok,
            "message": message,
            "checks": checks,
            "test_mode": bool(self.config.test_mode),
            "hash_algorithm": self.hash_algorithm,
            "merchant_login": self.merchant_login,
        }
