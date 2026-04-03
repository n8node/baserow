from datetime import datetime, timezone


def check_expired_subscriptions():
    """Downgrade expired subscriptions to the default (free) plan."""
    from baserow.contrib.billing.handler import BillingHandler
    from baserow.contrib.billing.models import Subscription

    now = datetime.now(tz=timezone.utc)
    expired = Subscription.objects.filter(
        status=Subscription.Status.ACTIVE,
        current_period_end__lt=now,
    ).exclude(current_period_end__isnull=True)

    try:
        default_plan = BillingHandler.get_default_plan()
    except Exception:
        return

    count = 0
    for sub in expired:
        sub.status = Subscription.Status.EXPIRED
        sub.plan = default_plan
        sub.save(update_fields=["status", "plan"])
        count += 1

    return count
