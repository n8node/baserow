import hashlib
import hmac
import json
from decimal import Decimal
from typing import Optional

import requests
from requests.auth import HTTPBasicAuth

from baserow.contrib.billing.models import PaymentProviderConfig
from baserow.contrib.billing.providers.base import PaymentProviderBase


class YooKassaProvider(PaymentProviderBase):
    API_URL = "https://api.yookassa.ru/v3"

    def __init__(self, config: PaymentProviderConfig):
        self.config = config

    def _auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(self.config.shop_id, self.config.secret_key)

    def create_payment_url(
        self,
        invoice_id: int,
        amount: Decimal,
        description: str,
        email: str = "",
        return_url: str = "",
        **kwargs,
    ) -> str:
        import uuid

        payload = {
            "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
            "confirmation": {
                "type": "redirect",
                "return_url": return_url or kwargs.get("return_url", ""),
            },
            "capture": True,
            "description": description[:128],
            "metadata": {"invoice_id": invoice_id},
        }
        if email:
            payload["receipt"] = {
                "customer": {"email": email},
                "items": [
                    {
                        "description": description[:128],
                        "quantity": "1",
                        "amount": {"value": f"{amount:.2f}", "currency": "RUB"},
                        "vat_code": 1,
                    }
                ],
            }

        headers = {
            "Idempotence-Key": str(uuid.uuid4()),
            "Content-Type": "application/json",
        }

        resp = requests.post(
            f"{self.API_URL}/payments",
            json=payload,
            auth=self._auth(),
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["confirmation"]["confirmation_url"]

    def verify_callback(self, data: dict) -> bool:
        # YooKassa sends webhook with event object; verification is done
        # via IP whitelist or by checking payment status via API.
        payment_id = self._extract_yookassa_payment_id(data)
        if not payment_id:
            return False

        resp = requests.get(
            f"{self.API_URL}/payments/{payment_id}",
            auth=self._auth(),
            timeout=30,
        )
        if resp.status_code != 200:
            return False

        payment_data = resp.json()
        return payment_data.get("status") == "succeeded"

    def _extract_yookassa_payment_id(self, data: dict) -> Optional[str]:
        obj = data.get("object", {})
        return obj.get("id")

    def get_payment_id_from_callback(self, data: dict) -> Optional[str]:
        return self._extract_yookassa_payment_id(data)

    def get_invoice_id_from_callback(self, data: dict) -> Optional[int]:
        obj = data.get("object", {})
        metadata = obj.get("metadata", {})
        try:
            return int(metadata.get("invoice_id", 0))
        except (ValueError, TypeError):
            return None
