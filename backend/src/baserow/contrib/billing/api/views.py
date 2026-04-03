from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.contrib.billing.api.serializers import (
    PaymentSerializer,
    PlanPublicSerializer,
    SubscribeRequestSerializer,
    SubscriptionSerializer,
)
from baserow.contrib.billing.handler import BillingHandler


class PublicPlansView(APIView):
    permission_classes = []

    def get(self, request):
        plans = BillingHandler.get_active_plans()
        return Response(PlanPublicSerializer(plans, many=True).data)


class MySubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sub = BillingHandler.get_subscription_safe(request.user)
        if sub is None:
            return Response(
                {"plan_slug": "free", "status": "none", "plan": None}
            )
        return Response(SubscriptionSerializer(sub).data)


class SubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SubscribeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plan_id = serializer.validated_data["plan_id"]
        billing_period = serializer.validated_data.get("billing_period", "monthly")
        plan = BillingHandler.get_plan(plan_id)

        if plan.price_monthly == 0 and plan.price_yearly == 0:
            sub = BillingHandler.change_plan(request.user, plan_id)
            return Response(SubscriptionSerializer(sub).data)

        amount = plan.price_yearly if billing_period == "yearly" else plan.price_monthly

        try:
            provider_config = BillingHandler.get_active_provider()
        except Exception:
            return Response(
                {"error": "No active payment provider configured."},
                status=503,
            )

        sub = BillingHandler.get_subscription_safe(request.user)
        if sub is None:
            sub = BillingHandler.create_default_subscription(request.user)

        payment = BillingHandler.record_payment(
            subscription=sub,
            amount=amount,
            provider=provider_config.provider_type,
            description=f"Subscription: {plan.name} ({billing_period})",
            metadata={"plan_id": plan.id, "billing_period": billing_period},
        )

        from baserow.contrib.billing.providers.robokassa import RobokassaProvider
        from baserow.contrib.billing.providers.yookassa import YooKassaProvider

        if provider_config.provider_type == "robokassa":
            provider = RobokassaProvider(provider_config)
            payment_url = provider.create_payment_url(
                invoice_id=payment.pk,
                amount=amount,
                description=f"{plan.name} ({billing_period})",
                email=request.user.email,
            )
        else:
            provider = YooKassaProvider(provider_config)
            payment_url = provider.create_payment_url(
                invoice_id=payment.pk,
                amount=amount,
                description=f"{plan.name} ({billing_period})",
                email=request.user.email,
                return_url=request.build_absolute_uri("/billing/success/"),
            )

        return Response({"payment_url": payment_url, "payment_id": payment.pk})


class CancelSubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sub = BillingHandler.get_subscription(request.user)
        try:
            default_plan = BillingHandler.get_default_plan()
            sub.plan = default_plan
        except Exception:
            pass
        sub.status = "cancelled"
        sub.save(update_fields=["plan", "status"])
        return Response(SubscriptionSerializer(sub).data)


class MyPaymentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sub = BillingHandler.get_subscription_safe(request.user)
        if sub is None:
            return Response([])
        payments = sub.payments.all()[:50]
        return Response(PaymentSerializer(payments, many=True).data)


class RobokassaCallbackView(APIView):
    permission_classes = []

    def post(self, request):
        from baserow.contrib.billing.providers.robokassa import RobokassaProvider

        try:
            provider_config = BillingHandler.get_provider("robokassa")
        except Exception:
            return Response("error", status=400)

        provider = RobokassaProvider(provider_config)
        if not provider.verify_callback(request.data):
            return Response("signature mismatch", status=400)

        inv_id = provider.get_invoice_id_from_callback(request.data)
        if inv_id:
            payment = BillingHandler.confirm_payment(inv_id)
            plan_id = payment.metadata.get("plan_id")
            if plan_id:
                BillingHandler.change_plan(payment.subscription.user, plan_id)

        return Response(provider.success_response(inv_id), content_type="text/plain")


class YooKassaWebhookView(APIView):
    permission_classes = []

    def post(self, request):
        from baserow.contrib.billing.providers.yookassa import YooKassaProvider

        try:
            provider_config = BillingHandler.get_provider("yookassa")
        except Exception:
            return Response("error", status=400)

        provider = YooKassaProvider(provider_config)
        event_type = request.data.get("event")

        if event_type == "payment.succeeded":
            if not provider.verify_callback(request.data):
                return Response("verification failed", status=400)

            inv_id = provider.get_invoice_id_from_callback(request.data)
            if inv_id:
                payment = BillingHandler.confirm_payment(inv_id)
                plan_id = payment.metadata.get("plan_id")
                if plan_id:
                    BillingHandler.change_plan(payment.subscription.user, plan_id)

        return Response(status=200)
