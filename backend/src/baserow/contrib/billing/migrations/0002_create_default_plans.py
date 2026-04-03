from django.db import migrations


def create_default_plans(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")

    if not Plan.objects.exists():
        Plan.objects.create(
            slug="free",
            name="Free",
            description="Basic free plan",
            is_default=True,
            is_active=True,
            order=0,
            price_monthly=0,
            price_yearly=0,
            currency="RUB",
            max_rows_per_workspace=1000,
            max_storage_mb=100,
            max_workspaces=1,
            max_collaborators_per_workspace=3,
            max_automations=0,
            max_api_calls_per_month=1000,
            features=[],
        )


def reverse_default_plans(apps, schema_editor):
    Plan = apps.get_model("billing", "Plan")
    Plan.objects.filter(slug="free", is_default=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_plans, reverse_default_plans),
    ]
