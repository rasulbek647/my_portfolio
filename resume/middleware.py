"""
Til: URL prefiksisiz loyihada ham LANGUAGE_COOKIE (set_language) ishlashi.
Dastlabki LocaleMiddleware sharti i18n_patterns=False bo‘lganda cookie o‘qilmay qolardi.
"""

from django.conf import settings
from django.conf.urls.i18n import is_language_prefix_patterns_used
from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class CookieAwareLocaleMiddleware(LocaleMiddleware):
    def process_request(self, request):
        urlconf = getattr(request, "urlconf", settings.ROOT_URLCONF)
        i18n_patterns_used, _prefixed_default = is_language_prefix_patterns_used(urlconf)
        language_from_path = translation.get_language_from_path(request.path_info)
        if language_from_path:
            language = language_from_path
        else:
            cookie_lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
            if cookie_lang and translation.check_for_language(cookie_lang):
                language = cookie_lang
            else:
                language = translation.get_language_from_request(request, check_path=i18n_patterns_used)
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()
