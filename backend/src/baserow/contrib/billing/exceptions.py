class BillingError(Exception):
    pass


class PlanNotFoundError(BillingError):
    pass


class PlanLimitExceededError(BillingError):
    def __init__(self, limit_type: str, current: int = 0, maximum: int = 0):
        self.limit_type = limit_type
        self.current = current
        self.maximum = maximum
        super().__init__(
            f"Plan limit exceeded: {limit_type} ({current}/{maximum})"
        )


class SubscriptionNotFoundError(BillingError):
    pass


class SubscriptionAlreadyExistsError(BillingError):
    pass


class PaymentProviderNotConfiguredError(BillingError):
    pass


class PaymentProviderNotActiveError(BillingError):
    pass


class PaymentVerificationError(BillingError):
    pass


class CannotDeleteDefaultPlanError(BillingError):
    pass


class CannotDeletePlanWithSubscriptionsError(BillingError):
    pass


class InvalidPlanChangeError(BillingError):
    pass
