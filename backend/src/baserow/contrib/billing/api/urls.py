from django.urls import include, re_path

from .views import (
    CancelSubscriptionView,
    MyPaymentsView,
    MySubscriptionView,
    PublicPlansView,
    RobokassaCallbackView,
    SubscribeView,
    YooKassaWebhookView,
)

app_name = "baserow.contrib.billing.api"

urlpatterns = [
    re_path(r"^plans/$", PublicPlansView.as_view(), name="plans"),
    re_path(
        r"^subscription/$",
        MySubscriptionView.as_view(),
        name="subscription",
    ),
    re_path(r"^subscribe/$", SubscribeView.as_view(), name="subscribe"),
    re_path(r"^cancel/$", CancelSubscriptionView.as_view(), name="cancel"),
    re_path(r"^payments/$", MyPaymentsView.as_view(), name="payments"),
    re_path(
        r"^robokassa/callback/$",
        RobokassaCallbackView.as_view(),
        name="robokassa_callback",
    ),
    re_path(
        r"^yookassa/webhook/$",
        YooKassaWebhookView.as_view(),
        name="yookassa_webhook",
    ),
    re_path(r"^admin/", include("baserow.contrib.billing.api.admin.urls")),
]
