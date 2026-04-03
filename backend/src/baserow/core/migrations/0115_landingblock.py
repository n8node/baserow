# Generated manually for n8node fork: public marketing landing blocks.

from django.db import migrations, models


def seed_landing_blocks(apps, schema_editor):
    LandingBlock = apps.get_model("core", "LandingBlock")
    if LandingBlock.objects.exists():
        return
    rows = [
        # Russian (default)
        dict(
            locale="ru",
            order=0,
            enabled=True,
            block_type="hero",
            title="Создавайте базы данных без кода",
            subtitle="Открытая платформа для команд: таблицы, представления, API и автоматизация в одном месте.",
            body="",
            image_url="",
            primary_cta_label="Начать бесплатно",
            primary_cta_url="/signup",
            secondary_cta_label="Войти",
            secondary_cta_url="/login",
        ),
        dict(
            locale="ru",
            order=1,
            enabled=True,
            block_type="section",
            title="Гибкие таблицы и представления",
            subtitle="",
            body="Стройте структуру данных как в привычных таблицах: поля, связи, формулы, права доступа по ролям.",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
        ),
        dict(
            locale="ru",
            order=2,
            enabled=True,
            block_type="cta",
            title="Готовы попробовать?",
            subtitle="Создайте аккаунт и первое рабочее пространство за пару минут.",
            body="",
            image_url="",
            primary_cta_label="Регистрация",
            primary_cta_url="/signup",
            secondary_cta_label="",
            secondary_cta_url="",
        ),
        # English
        dict(
            locale="en",
            order=0,
            enabled=True,
            block_type="hero",
            title="Build databases without code",
            subtitle="An open platform for teams: tables, views, API, and automation in one place.",
            body="",
            image_url="",
            primary_cta_label="Get started",
            primary_cta_url="/signup",
            secondary_cta_label="Log in",
            secondary_cta_url="/login",
        ),
        dict(
            locale="en",
            order=1,
            enabled=True,
            block_type="section",
            title="Flexible tables and views",
            subtitle="",
            body="Model your data like in a spreadsheet: fields, relations, formulas, and role-based permissions.",
            image_url="",
            primary_cta_label="",
            primary_cta_url="",
            secondary_cta_label="",
            secondary_cta_url="",
        ),
        dict(
            locale="en",
            order=2,
            enabled=True,
            block_type="cta",
            title="Ready to try it?",
            subtitle="Create an account and your first workspace in minutes.",
            body="",
            image_url="",
            primary_cta_label="Sign up",
            primary_cta_url="/signup",
            secondary_cta_label="",
            secondary_cta_url="",
        ),
    ]
    for row in rows:
        LandingBlock.objects.create(**row)


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0114_userprofile_language_en_ru_only"),
    ]

    operations = [
        migrations.CreateModel(
            name="LandingBlock",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                (
                    "locale",
                    models.CharField(
                        choices=[("ru", "Russian"), ("en", "English")],
                        db_index=True,
                        default="ru",
                        max_length=5,
                    ),
                ),
                ("enabled", models.BooleanField(default=True)),
                (
                    "block_type",
                    models.CharField(
                        default="section",
                        help_text="Layout hint for the frontend: hero, section, cta.",
                        max_length=32,
                    ),
                ),
                ("title", models.TextField(blank=True)),
                ("subtitle", models.TextField(blank=True)),
                ("body", models.TextField(blank=True)),
                ("image_url", models.URLField(blank=True, max_length=2048)),
                ("primary_cta_label", models.CharField(blank=True, max_length=255)),
                ("primary_cta_url", models.CharField(blank=True, max_length=2048)),
                ("secondary_cta_label", models.CharField(blank=True, max_length=255)),
                ("secondary_cta_url", models.CharField(blank=True, max_length=2048)),
            ],
            options={
                "ordering": ("locale", "order", "id"),
            },
        ),
        migrations.AddIndex(
            model_name="landingblock",
            index=models.Index(
                fields=["locale", "enabled", "order"],
                name="core_landin_locale__d7f9bc_idx",
            ),
        ),
        migrations.RunPython(seed_landing_blocks, migrations.RunPython.noop),
    ]
