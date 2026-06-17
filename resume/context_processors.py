from django.conf import settings
from django.urls import translate_url

from .admin_content_lang import get_ui_lang
from .dashboard_i18n import get_dashboard_strings
from .models import SiteSettings


def site_theme(request):
    return {"active_theme": SiteSettings.load().theme}


def language_switch_urls(request):
    paths = {}
    for code, _ in settings.LANGUAGES:
        try:
            paths[code] = translate_url(request.path, code)
        except Exception:
            paths[code] = request.path
    return {"switch_urls": paths}


def dashboard_ui_strings(request):
    """/admin/ ostidagi panellar uchun `dash` lug‘ati (matnlar)."""
    path = getattr(request, "path", "") or ""
    if not path.startswith("/admin/"):
        return {}
    lang = get_ui_lang(request)
    return {"dash": get_dashboard_strings(lang), "admin_ui_lang": lang}
