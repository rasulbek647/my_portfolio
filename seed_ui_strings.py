"""
Barcha standart UI kalit va qiymatlarini UiString jadvaliga yozadi.
Mavjud qatorlarni qayta yozmaydi.
"""
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from resume.models import UiString
from resume.ui_strings import _TEXTS

keys = list(_TEXTS["en"].keys())
created = 0
for key in keys:
    obj, is_new = UiString.objects.get_or_create(
        key=key,
        defaults={
            "text_en": _TEXTS["en"].get(key, ""),
            "text_uz": _TEXTS["uz"].get(key, ""),
            "text_ru": _TEXTS["ru"].get(key, ""),
        }
    )
    if is_new:
        created += 1
        print(f"  + {key}")
    else:
        print(f"  ~ {key} (mavjud)")

print(f"\nNatija: {created} ta yangi, {len(keys) - created} ta mavjud")
