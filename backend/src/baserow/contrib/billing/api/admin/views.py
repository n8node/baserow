from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.contrib.billing.api.serializers import (
    CreatePlanSerializer,
    PaymentProviderConfigSerializer,
    PlanSerializer,
    SubscriptionSerializer,
    UpdatePaymentProviderSerializer,
    UpdatePlanSerializer,
)
from baserow.contrib.billing.handler import BillingHandler
from baserow.contrib.billing.models import Subscription


class AdminPlansView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        plans = BillingHandler.get_all_plans()
        return Response(PlanSerializer(plans, many=True).data)

    def post(self, request):
        serializer = CreatePlanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = BillingHandler.create_plan(**serializer.validated_data)
        return Response(PlanSerializer(plan).data, status=201)


class AdminPlanView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, plan_id):
        plan = BillingHandler.get_plan(plan_id)
        return Response(PlanSerializer(plan).data)

    def patch(self, request, plan_id):
        serializer = UpdatePlanSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        plan = BillingHandler.update_plan(plan_id, **serializer.validated_data)
        return Response(PlanSerializer(plan).data)

    def delete(self, request, plan_id):
        BillingHandler.delete_plan(plan_id)
        return Response(status=204)


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
