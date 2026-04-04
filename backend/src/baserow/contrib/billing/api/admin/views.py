from django.contrib.auth import get_user_model
from django.db.models import Count
from django.urls import NoReverseMatch, reverse

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.api.exceptions import RequestBodyValidationException
from baserow.contrib.billing.api.serializers import (
    CreatePlanSerializer,
    PaymentProviderConfigSerializer,
    PlanSerializer,
    SubscriptionSerializer,
    UpdatePaymentProviderSerializer,
    UpdatePlanSerializer,
)
from baserow.contrib.billing.exceptions import (
    CannotDeleteDefaultPlanError,
    CannotDeletePlanWithSubscriptionsError,
    PlanNotFoundError,
)
from baserow.contrib.billing.handler import BillingHandler
from baserow.contrib.billing.models import Plan, Subscription

User = get_user_model()


class AdminPlansView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        plans = (
            Plan.objects.annotate(subscription_count=Count("subscriptions"))
            .order_by("order")
        )
        return Response(PlanSerializer(plans, many=True).data)

    def post(self, request):
        serializer = CreatePlanSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            raise RequestBodyValidationException(detail=exc.detail) from exc
        plan = BillingHandler.create_plan(**serializer.validated_data)
        return Response(PlanSerializer(plan).data, status=201)


class AdminPlanView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, plan_id):
        plan = BillingHandler.get_plan(plan_id)
        return Response(PlanSerializer(plan).data)

    def patch(self, request, plan_id):
        try:
            plan = BillingHandler.get_plan(plan_id)
        except PlanNotFoundError as exc:
            return Response(
                {"error": "ERROR_BILLING_PLAN_NOT_FOUND", "detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = UpdatePlanSerializer(
            instance=plan, data=request.data, partial=True
        )
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as exc:
            raise RequestBodyValidationException(detail=exc.detail) from exc
        plan = BillingHandler.update_plan(plan_id, **serializer.validated_data)
        return Response(PlanSerializer(plan).data)

    def delete(self, request, plan_id):
        try:
            BillingHandler.delete_plan(plan_id)
        except PlanNotFoundError as exc:
            return Response(
                {"error": "ERROR_BILLING_PLAN_NOT_FOUND", "detail": str(exc)},
                status=status.HTTP_404_NOT_FOUND,
            )
        except CannotDeleteDefaultPlanError as exc:
            return Response(
                {
                    "error": "ERROR_BILLING_CANNOT_DELETE_DEFAULT_PLAN",
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except CannotDeletePlanWithSubscriptionsError as exc:
            return Response(
                {
                    "error": "ERROR_BILLING_PLAN_HAS_SUBSCRIPTIONS",
                    "detail": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminPlanSetDefaultView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, plan_id):
        plan = BillingHandler.update_plan(plan_id, is_default=True)
        return Response(PlanSerializer(plan).data)


class AdminProvidersView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        providers = BillingHandler.get_all_providers()
        return Response(
            PaymentProviderConfigSerializer(providers, many=True).data
        )


class AdminRobokassaUrlsView(APIView):
    """
    Absolute URLs to configure in the Robokassa merchant cabinet (Result URL, etc.).
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            path = reverse("api:billing:robokassa_callback")
        except NoReverseMatch:
            path = "/api/billing/robokassa/callback/"
        return Response(
            {"robokassa_result_url": request.build_absolute_uri(path)}
        )


class AdminProviderView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, provider_type):
        serializer = UpdatePaymentProviderSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        config = BillingHandler.update_provider(
            provider_type, **serializer.validated_data
        )
        return Response(PaymentProviderConfigSerializer(config).data)


class AdminProviderActivateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, provider_type):
        config = BillingHandler.activate_provider(provider_type)
        return Response(PaymentProviderConfigSerializer(config).data)


class AdminProviderDeactivateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, provider_type):
        config = BillingHandler.deactivate_provider(provider_type)
        return Response(PaymentProviderConfigSerializer(config).data)


class AdminSubscriptionsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        subs = (
            Subscription.objects.select_related("plan", "user")
            .all()
            .order_by("-created_at")[:200]
        )
        data = []
        for sub in subs:
            item = SubscriptionSerializer(sub).data
            item["user_email"] = sub.user.email
            item["user_id"] = sub.user.id
            data.append(item)
        return Response(data)


class AdminSubscriptionView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, subscription_id):
        try:
            sub = Subscription.objects.get(pk=subscription_id)
        except Subscription.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

        plan_id = request.data.get("plan_id")
        status = request.data.get("status")

        if plan_id:
            plan = BillingHandler.get_plan(plan_id)
            sub.plan = plan
        if status:
            sub.status = status
        sub.save()

        return Response(SubscriptionSerializer(sub).data)


class AdminAssignPlanView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        user_id = request.data.get("user_id")
        plan_id = request.data.get("plan_id")

        if not user_id or not plan_id:
            return Response(
                {"error": "user_id and plan_id are required."}, status=400
            )

        try:
            target_user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        plan = BillingHandler.get_plan(plan_id)

        sub, created = Subscription.objects.get_or_create(
            user=target_user,
            defaults={
                "plan": plan,
                "status": Subscription.Status.ACTIVE,
            },
        )
        if not created:
            sub.plan = plan
            sub.status = Subscription.Status.ACTIVE
            sub.save(update_fields=["plan", "status"])

        result = SubscriptionSerializer(sub).data
        result["user_id"] = target_user.id
        result["plan_name"] = plan.name
        return Response(result)


class AdminAvailableFeaturesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        features = [
            {"key": "premium", "name": "Premium features"},
            {"key": "row_comments", "name": "Row comments"},
            {"key": "kanban_view", "name": "Kanban view"},
            {"key": "calendar_view", "name": "Calendar view"},
            {"key": "timeline_view", "name": "Timeline view"},
            {"key": "survey_form", "name": "Survey form mode"},
            {"key": "personal_views", "name": "Personal views"},
            {"key": "export_json_xml", "name": "JSON/XML export"},
            {"key": "ai_field", "name": "AI field"},
            {"key": "chart_widget", "name": "Chart widgets"},
            {"key": "no_branding", "name": "No branding"},
            {"key": "rbac", "name": "RBAC (role-based access)"},
            {"key": "teams", "name": "Teams"},
            {"key": "audit_log", "name": "Audit log"},
            {"key": "sso", "name": "SSO (Single Sign-On)"},
            {"key": "data_sync", "name": "Data sync"},
            {"key": "advanced_webhooks", "name": "Advanced webhooks"},
            {"key": "secure_file_serve", "name": "Secure file serve"},
        ]
        return Response(features)
