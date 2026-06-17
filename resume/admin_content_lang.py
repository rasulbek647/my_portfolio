"""Admin: kontent kiritish tili va panel UI tili (alohida sessiya kalitlari)."""

SESSION_KEY = "admin_content_lang"
SESSION_KEY_UI = "admin_ui_lang"
VALID = frozenset({"en", "uz", "ru"})


def get_content_lang(request) -> str:
    if not request:
        return "en"
    lang = request.session.get(SESSION_KEY, "en")
    return lang if lang in VALID else "en"


def get_ui_lang(request) -> str:
    """Panel tugmalari va sarlavhalar uz / en / ru."""
    if not request:
        return "uz"
    lang = request.session.get(SESSION_KEY_UI, "uz")
    return lang if lang in VALID else "uz"


def content_lang_label(code: str) -> str:
    return {"en": "English", "uz": "Oʻzbekcha", "ru": "Русский"}.get(code, code)
