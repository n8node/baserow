import abc
from decimal import Decimal
from typing import Optional


class PaymentProviderBase(abc.ABC):
    @abc.abstractmethod
    def create_payment_url(
        self,
        invoice_id: int,
        amount: Decimal,
        description: str,
        email: str = "",
        **kwargs,
    ) -> str:
        """Return a URL where the user should be redirected to pay."""

    @abc.abstractmethod
    def verify_callback(self, data: dict) -> bool:
        """Verify the payment callback signature."""

    @abc.abstractmethod
    def get_payment_id_from_callback(self, data: dict) -> Optional[str]:
        """Extract the external payment ID from callback data."""

    @abc.abstractmethod
    def get_invoice_id_from_callback(self, data: dict) -> Optional[int]:
        """Extract our internal invoice/payment ID from callback data."""
