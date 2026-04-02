# Generated manually for n8node fork: only en/ru UI languages.

from django.db import migrations, models


def forwards_map_languages(apps, schema_editor):
    UserProfile = apps.get_model("core", "UserProfile")
    UserProfile.objects.exclude(language__in=["en", "ru"]).update(language="ru")


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0113_alter_notification_options_and_more"),
    ]

    operations = [
        migrations.RunPython(forwards_map_languages, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="userprofile",
            name="language",
            field=models.TextField(
                choices=[("en", "English"), ("ru", "Russian")],
                default="ru",
                help_text="An ISO 639 language code (with optional variant) selected "
                "by the user. Ex: en-GB.",
                max_length=10,
            ),
        ),
    ]
