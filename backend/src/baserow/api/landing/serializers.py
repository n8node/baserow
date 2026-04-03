from rest_framework import serializers

from baserow.core.models import LandingBlock


class PublicLandingBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingBlock
        fields = (
            "id",
            "order",
            "block_type",
            "title",
            "subtitle",
            "body",
            "image_url",
            "primary_cta_label",
            "primary_cta_url",
            "secondary_cta_label",
            "secondary_cta_url",
        )


class AdminLandingBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandingBlock
        fields = (
            "id",
            "order",
            "locale",
            "enabled",
            "block_type",
            "title",
            "subtitle",
            "body",
            "image_url",
            "primary_cta_label",
            "primary_cta_url",
            "secondary_cta_label",
            "secondary_cta_url",
        )
