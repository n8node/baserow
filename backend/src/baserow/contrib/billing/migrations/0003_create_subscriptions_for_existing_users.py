from django.db import migrations


def create_subscriptions(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Plan = apps.get_model("billing", "Plan")
    Subscription = apps.get_model("billing", "Subscription")

    default_plan = Plan.objects.filter(is_default=True).first()
    if not default_plan:
        return

    existing_user_ids = set(
        Subscription.objects.values_list("user_id", flat=True)
    )
    users_without_sub = User.objects.exclude(id__in=existing_user_ids)

    subs = []
    for user in users_without_sub:
        subs.append(
            Subscription(
                user=user,
                plan=default_plan,
                status="active",
            )
        )

    if subs:
        Subscription.objects.bulk_create(subs, batch_size=500)


def reverse_subscriptions(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("billing", "0002_create_default_plans"),
    ]

    operations = [
        migrations.RunPython(create_subscriptions, reverse_subscriptions),
    ]
