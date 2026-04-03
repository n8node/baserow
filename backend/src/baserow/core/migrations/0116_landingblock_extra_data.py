from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0115_landingblock"),
    ]

    operations = [
        migrations.AddField(
            model_name="landingblock",
            name="extra_data",
            field=models.JSONField(
                blank=True,
                default=dict,
                help_text="Structured data for complex blocks (items, features, etc.).",
            ),
        ),
    ]
