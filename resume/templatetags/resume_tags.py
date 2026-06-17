from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import get_language

from ..contact_dynamic_icons import svg_for_icon
from ..contact_links import (
    ensure_url,
    instagram_href,
    instagram_label,
    phone_tel_href,
    telegram_href,
    telegram_label,
    whatsapp_href,
)
from ..i18n_field import localized_model_value
from ..ui_strings import ui_text

register = template.Library()


@register.filter
def contact_ensure_url(value):
    return ensure_url(value)


@register.filter
def contact_telegram_url(value):
    return telegram_href(value)


@register.filter
def contact_instagram_url(value):
    return instagram_href(value)


@register.filter
def contact_whatsapp_url(value):
    return whatsapp_href(value)


@register.filter
def contact_phone_tel(value):
    return phone_tel_href(value)


@register.filter
def contact_telegram_label(value):
    return telegram_label(value) or value or ""


@register.filter
def contact_instagram_label(value):
    return instagram_label(value) or value or ""


@register.simple_tag
def uitext(key: str):
    return ui_text(key)


@register.simple_tag
def dynamic_contact_icon(icon_key=None):
    return mark_safe(svg_for_icon(icon_key))


@register.filter
def split_skill_tags(value):
    """Ko‘nikmalar matnini qatorlar va vergul bo‘yicha ajratadi."""
    if not value:
        return []
    out: list[str] = []
    for chunk in str(value).replace(",", "\n").split("\n"):
        s = chunk.strip()
        if s:
            out.append(s)
    return out


@register.simple_tag
def localized_field(obj, base_name: str):
    """Tanlangan til → _lang; bo‘sh bo‘lsa manba maydon; yana bo‘sh bo‘lsa boshqa til."""
    code = (get_language() or "en")[:2]
    return localized_model_value(obj, base_name, code)


@register.simple_tag
def localized_field_lang(obj, base_name: str, lang_code: str):
    """Ro‘yxatlar uchun aniq til kodi (masalan: panel til)."""
    return localized_model_value(obj, base_name, (lang_code or "en")[:2])
