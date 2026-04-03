from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from baserow.core.models import LandingBlock

from .serializers import AdminLandingBlockSerializer, PublicLandingBlockSerializer


class PublicLandingBlocksView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        tags=["Landing"],
        operation_id="landing_blocks_list",
        description="Returns enabled homepage blocks for the given locale (ru or en).",
        responses={200: PublicLandingBlockSerializer(many=True)},
    )
    def get(self, request: Request) -> Response:
        locale = request.query_params.get("locale") or "ru"
        if locale not in (LandingBlock.Locale.RU, LandingBlock.Locale.EN):
            locale = LandingBlock.Locale.RU
        qs: QuerySet[LandingBlock] = LandingBlock.objects.filter(
            locale=locale, enabled=True
        ).order_by("order", "id")
        return Response(PublicLandingBlockSerializer(qs, many=True).data)


class AdminLandingBlocksView(APIView):
    permission_classes = (IsAdminUser,)

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_landing_blocks_list",
        responses={200: AdminLandingBlockSerializer(many=True)},
    )
    def get(self, request: Request) -> Response:
        locale = request.query_params.get("locale") or "ru"
        if locale not in (LandingBlock.Locale.RU, LandingBlock.Locale.EN):
            locale = LandingBlock.Locale.RU
        qs = LandingBlock.objects.filter(locale=locale).order_by("order", "id")
        return Response(AdminLandingBlockSerializer(qs, many=True).data)

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_landing_blocks_create",
        request=AdminLandingBlockSerializer,
        responses={201: AdminLandingBlockSerializer},
    )
    def post(self, request: Request) -> Response:
        serializer = AdminLandingBlockSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AdminLandingBlockView(APIView):
    permission_classes = (IsAdminUser,)

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_landing_block_get",
        responses={200: AdminLandingBlockSerializer},
    )
    def get(self, request: Request, block_id: int) -> Response:
        block = get_object_or_404(LandingBlock, pk=block_id)
        return Response(AdminLandingBlockSerializer(block).data)

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_landing_block_update",
        request=AdminLandingBlockSerializer,
        responses={200: AdminLandingBlockSerializer},
    )
    def patch(self, request: Request, block_id: int) -> Response:
        block = get_object_or_404(LandingBlock, pk=block_id)
        serializer = AdminLandingBlockSerializer(block, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @extend_schema(
        tags=["Admin"],
        operation_id="admin_landing_block_delete",
        responses={204: None},
    )
    def delete(self, request: Request, block_id: int) -> Response:
        LandingBlock.objects.filter(pk=block_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
