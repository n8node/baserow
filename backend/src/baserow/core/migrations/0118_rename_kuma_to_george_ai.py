from django.db import migrations


REPLACEMENTS = (
    ("Kuma AI", "George AI"),
    ("Kuma", "George AI"),
    ("Кума ИИ", "George AI"),
    ("Кума", "George AI"),
)


def _replace_text(value):
    if not isinstance(value, str):
        return value
    result = value
    for old, new in REPLACEMENTS:
        result = result.replace(old, new)
    return result


def _replace_nested(value):
    if isinstance(value, str):
        return _replace_text(value)
    if isinstance(value, list):
        return [_replace_nested(item) for item in value]
    if isinstance(value, dict):
        return {key: _replace_nested(item) for key, item in value.items()}
    return value


def forwards(apps, schema_editor):
    LandingBlock = apps.get_model("core", "LandingBlock")

    for block in LandingBlock.objects.all():
        updated = False
        for field in (
            "title",
            "subtitle",
            "body",
            "primary_cta_label",
            "secondary_cta_label",
        ):
            current = getattr(block, field)
            new_value = _replace_text(current)
            if new_value != current:
                setattr(block, field, new_value)
                updated = True

        current_extra = block.extra_data
        new_extra = _replace_nested(current_extra)
        if new_extra != current_extra:
            block.extra_data = new_extra
            updated = True

        if updated:
            block.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0117_seed_landing_baserow_io"),
    ]

    operations = [
        migrations.RunPython(forwards, reverse_code=migrations.RunPython.noop),
    ]
