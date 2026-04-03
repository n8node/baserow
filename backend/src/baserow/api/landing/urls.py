from django.urls import path

from .views import AdminLandingBlockView, AdminLandingBlocksView, PublicLandingBlocksView

app_name = "baserow.api.landing"

urlpatterns = [
    path("blocks/", PublicLandingBlocksView.as_view(), name="blocks"),
]
