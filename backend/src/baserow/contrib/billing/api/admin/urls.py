from django.urls import re_path

from .views import (
    AdminAssignPlanView,
    AdminAvailableFeaturesView,
    AdminPlanSetDefaultView,
    AdminPlansView,
    AdminPlanView,
    AdminProviderActivateView,
    AdminProviderDeactivateView,
    AdminProvidersView,
    AdminProviderView,
    AdminRobokassaTestConnectionView,
    AdminRobokassaUrlsView,
    AdminSubscriptionsView,
    AdminSubscriptionView,
)

app_name = "baserow.contrib.billing.api.admin"

urlpatterns = [
    re_path(r"^plans/$", AdminPlansView.as_view(), name="plans"),
    re_path(
        r"^plans/(?P<plan_id>\d+)/$", AdminPlanView.as_view(), name="plan"
    ),
    re_path(
        r"^plans/(?P<plan_id>\d+)/set-default/$",
        AdminPlanSetDefaultView.as_view(),
        name="plan_set_default",
    ),
    re_path(
        r"^robokassa-urls/$",
        AdminRobokassaUrlsView.as_view(),
        name="robokassa_urls",
    ),
    re_path(
        r"^robokassa-test/$",
        AdminRobokassaTestConnectionView.as_view(),
        name="robokassa_test",
    ),
    re_path(
        r"^providers/$", AdminProvidersView.as_view(), name="providers"
    ),
    re_path(
        r"^providers/(?P<provider_type>\w+)/$",
        AdminProviderView.as_view(),
        name="provider",
    ),
    re_path(
        r"^providers/(?P<provider_type>\w+)/activate/$",
        AdminProviderActivateView.as_view(),
        name="provider_activate",
    ),
    re_path(
        r"^providers/(?P<provider_type>\w+)/deactivate/$",
        AdminProviderDeactivateView.as_view(),
        name="provider_deactivate",
    ),
    re_path(
        r"^subscriptions/$",
        AdminSubscriptionsView.as_view(),
        name="subscriptions",
    ),
    re_path(
        r"^subscriptions/(?P<subscription_id>\d+)/$",
        AdminSubscriptionView.as_view(),
        name="subscription",
    ),
    re_path(
        r"^assign-plan/$",
        AdminAssignPlanView.as_view(),
        name="assign_plan",
    ),
    re_path(
        r"^available-features/$",
        AdminAvailableFeaturesView.as_view(),
        name="available_features",
    ),
]
