"""
DRF throttle that enforces ``Plan.max_api_calls_per_month``.

The counter lives in Django's default cache (Redis in production) with a
key per user per calendar month.  The plan limit is cached for 60 s to
avoid hitting the DB on every request.
"""

import calendar
from datetime import datetime

from django.core.cache import cache

from rest_framework.throttling import BaseThrottle

_SENTINEL = object()
_PLAN_CACHE_TTL = 60  # seconds


class BillingApiCallThrottle(BaseThrottle):
    """
    Counts authenticated (non-staff) API calls per calendar month and
    compares against the user's plan ``max_api_calls_per_month``.
    Returns ``False`` (→ HTTP 429) when the quota is exceeded.
    """

    def allow_request(self, request, view):
        user = request.user
        if not getattr(user, "is_authenticated", False) or user.is_staff:
            return True

        max_calls = self._get_max_calls(user)
        if max_calls <= 0:
            return True

        now = datetime.utcnow()
        counter_key = f"billing_api_calls:{user.id}:{now.year}-{now.month:02d}"

        try:
            count = cache.incr(counter_key)
        except ValueError:
            days = calendar.monthrange(now.year, now.month)[1]
            end = datetime(now.year, now.month, days, 23, 59, 59)
            timeout = max(int((end - now).total_seconds()) + 1, 1)
            cache.set(counter_key, 1, timeout=timeout)
            count = 1

        if count > max_calls:
            self._remaining_seconds = self._seconds_until_month_end(now)
            return False
        return True

    def wait(self):
        return getattr(self, "_remaining_seconds", None)

    # ------------------------------------------------------------------

    @staticmethod
    def _get_max_calls(user):
        """
        Return the plan's ``max_api_calls_per_month`` for *user*, using a
        short-lived cache to avoid a DB hit on every request.
        A cached value of ``-1`` means "unlimited".
        """

        limit_key = f"billing_api_limit:{user.id}"
        cached = cache.get(limit_key, _SENTINEL)
        if cached is not _SENTINEL:
            return cached

        from baserow.contrib.billing.handler import BillingHandler

        sub = BillingHandler.get_subscription_safe(user)
        if sub and sub.is_usable and sub.plan.max_api_calls_per_month:
            max_calls = sub.plan.max_api_calls_per_month
        else:
            max_calls = -1

        cache.set(limit_key, max_calls, timeout=_PLAN_CACHE_TTL)
        return max_calls

    @staticmethod
    def _seconds_until_month_end(now):
        days = calendar.monthrange(now.year, now.month)[1]
        end = datetime(now.year, now.month, days, 23, 59, 59)
        return max(int((end - now).total_seconds()), 1)
