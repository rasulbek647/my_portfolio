"""Gettext bo'lmasa ham ishlaydigan UI qatorlari (en / uz / ru).

Ustuvorlik tartibi:
  1. UiString bazadagi qiymat (agar mavjud va bo'sh bo'lmasa)
  2. _TEXTS ichidagi standart qiymat
"""

from django.utils.translation import get_language

_TEXTS: dict[str, dict[str, str]] = {
    "en": {
        "resume": "Resume",
        "language": "Language",
        "about_me": "About me",
        "certificates": "Certificates",
        "portfolio": "Work",
        "interests": "Interests",
        "website": "Website",
        "view_document": "View document",
        "built_with_django": "Built with Django",
        "nav_hero": "Home",
        "nav_about": "About",
        "nav_services": "Services",
        "services": "Services",
        "nav_portfolio": "Work",
        "nav_experience": "Experience",
        "nav_education": "Education",
        "nav_certificates": "Certificates",
        "nav_interests": "Interests",
        "nav_contact": "Contact",
        "skills": "Skills",
        "experience": "Experience",
        "education": "Education",
        "contact": "Contact",
        "get_in_touch": "Get in touch",
        "contact_lead": "Open to opportunities and collaborations.",
        "cta_resume": "Contact",
        "period_present": "Present",
        "document": "Document",
        "download_cv": "Download CV (PDF)",
        "open_project_link": "Open project",
        "contact_email_label": "Email",
        "contact_phone_label": "Phone",
        "social_telegram": "Telegram",
        "social_instagram": "Instagram",
        "social_whatsapp": "WhatsApp",
        "social_linkedin": "LinkedIn",
        "social_github": "GitHub",
        "social_website": "Website",
        "social_kwork": "Kwork",
        "hire_on_kwork": "Hire me on Kwork",
        "contact_me": "Contact me",
        "contact_link_fallback_label": "Link",
        "admin_title": "CV resume administration",
        "admin_site": "CV Admin",
        "admin_dashboard": "Dashboard",
        "cv_content_lang": "CV content language",
        "cv_content_lang_hint": "Fields below show text for the selected language only. Switch language, then Save.",
        "featured_certificate": "Featured Achievement",
    },
    "uz": {
        "resume": "Rezyume",
        "language": "Til",
        "about_me": "O'zim haqimda",
        "certificates": "Sertifikatlar",
        "portfolio": "Loyihalar",
        "interests": "Qiziqishlar",
        "website": "Veb-sayt",
        "view_document": "Hujjatni ko'rish",
        "built_with_django": "Django yordamida yig'ilgan",
        "nav_hero": "Bosh",
        "nav_about": "Men haqimda",
        "nav_services": "Xizmatlar",
        "services": "Xizmatlar",
        "nav_portfolio": "Loyihalar",
        "nav_experience": "Tajriba",
        "nav_education": "Ta'lim",
        "nav_certificates": "Sertifikatlar",
        "nav_interests": "Qiziqishlar",
        "nav_contact": "Aloqa",
        "skills": "Ko'nikmalar",
        "experience": "Tajriba",
        "education": "Ta'lim",
        "contact": "Aloqa",
        "get_in_touch": "Bog'lanish",
        "contact_lead": "Taklif va hamkorlik uchun ochiqman.",
        "cta_resume": "Aloqa",
        "period_present": "Hozirgi vaqt",
        "document": "Hujjat",
        "download_cv": "CV yuklab olish (PDF)",
        "open_project_link": "Loyihani ochish",
        "contact_email_label": "Email",
        "contact_phone_label": "Telefon",
        "social_telegram": "Telegram",
        "social_instagram": "Instagram",
        "social_whatsapp": "WhatsApp",
        "social_linkedin": "LinkedIn",
        "social_github": "GitHub",
        "social_website": "Veb-sayt",
        "social_kwork": "Kwork",
        "hire_on_kwork": "Kworkda buyurtma berish",
        "contact_me": "Bog'lanish",
        "contact_link_fallback_label": "Havola",
        "admin_title": "CV rezyume boshqaruvi",
        "admin_site": "CV admin",
        "admin_dashboard": "Boshqaruv paneli",
        "cv_content_lang": "CV matni tili",
        "cv_content_lang_hint": "Quyidagi maydonlar faqat tanlangan til uchun. Tilni almashtiring, keyin Saqlash.",
        "featured_certificate": "Asosiy Yutuq",
    },
    "ru": {
        "resume": "Резюме",
        "language": "Язык",
        "about_me": "Обо мне",
        "certificates": "Сертификаты",
        "portfolio": "Проекты",
        "interests": "Интересы",
        "website": "Сайт",
        "view_document": "Открыть документ",
        "built_with_django": "Сделано на Django",
        "nav_hero": "Главная",
        "nav_about": "Обо мне",
        "nav_services": "Услуги",
        "services": "Услуги",
        "nav_portfolio": "Проекты",
        "nav_experience": "Опыт",
        "nav_education": "Образование",
        "nav_certificates": "Сертификаты",
        "nav_interests": "Интересы",
        "nav_contact": "Контакты",
        "skills": "Навыки",
        "experience": "Опыт",
        "education": "Образование",
        "contact": "Контакты",
        "get_in_touch": "Связаться",
        "contact_lead": "Открыт к предложениям и сотрудничеству.",
        "cta_resume": "Написать",
        "period_present": "Настоящее время",
        "document": "Документ",
        "download_cv": "Скачать резюме (PDF)",
        "open_project_link": "Открыть проект",
        "contact_email_label": "Email",
        "contact_phone_label": "Телефон",
        "social_telegram": "Telegram",
        "social_instagram": "Instagram",
        "social_whatsapp": "WhatsApp",
        "social_linkedin": "LinkedIn",
        "social_github": "GitHub",
        "social_website": "Сайт",
        "social_kwork": "Kwork",
        "hire_on_kwork": "Заказать на Kwork",
        "contact_me": "Написать",
        "contact_link_fallback_label": "Ссылка",
        "admin_title": "Администрирование резюме",
        "admin_site": "CV Админ",
        "admin_dashboard": "Панель управления",
        "cv_content_lang": "Язык текста резюме",
        "cv_content_lang_hint": "Поля ниже — только для выбранного языка. Смените язык и нажмите «Сохранить».",
        "featured_certificate": "Главное достижение",
    },
}

# Yangi dizayn (video uslubi) uchun qatorlar
_TEXTS["en"].update({
    "menu": "Menu",
    "close": "Close",
    "download_cv_short": "Download CV",
    "order_kwork": "Order on Kwork",
    "hero_scroll": "Scroll",
    "hero_sub": "I build fast, modern websites with Python and Django — from the backend to an easy admin panel.",
    "available": "Open to new projects",
    "hero_tagline": "Fast, modern websites built to grow your business",
    "view_projects": "View projects",
    "years_experience": "Years of learning & building",
    "works_big": "Works",
    "works_bg": "Works",
    "discover_projects": "Discover my projects",
    "selected_works": "Selected works",
    "tech_stack": "Tech stack",
    "tech_stack_title": "Tools I build with",
    "lets_create": "Let's create something meaningful",
    "write_telegram": "Message on Telegram",
    "send_email": "Send an email",
    "quick_links": "Quick links",
    "back_to_top": "Back to top",
    "all_rights": "All rights reserved",
})
_TEXTS["uz"].update({
    "menu": "Menyu",
    "close": "Yopish",
    "download_cv_short": "CV yuklab olish",
    "order_kwork": "Kwork'da buyurtma berish",
    "hero_scroll": "Pastga",
    "hero_sub": "Python va Django bilan tez va zamonaviy saytlar yarataman — serverdan tortib qulay admin panelgacha.",
    "available": "Yangi loyihalarga ochiqman",
    "hero_tagline": "Biznesingizni o'stiradigan tez va zamonaviy saytlar",
    "view_projects": "Loyihalarni ko'rish",
    "years_experience": "Yillik o'qish va amaliyot",
    "works_big": "Ishlar",
    "works_bg": "Works",
    "discover_projects": "Loyihalarim bilan tanishing",
    "selected_works": "Tanlangan ishlar",
    "tech_stack": "Texnologiyalar",
    "tech_stack_title": "Men ishlaydigan texnologiyalar",
    "lets_create": "Keling, birga zo'r narsa yaratamiz",
    "write_telegram": "Telegram'da yozish",
    "send_email": "Email yozish",
    "quick_links": "Tezkor havolalar",
    "back_to_top": "Tepaga",
    "all_rights": "Barcha huquqlar himoyalangan",
})
_TEXTS["ru"].update({
    "menu": "Меню",
    "close": "Закрыть",
    "download_cv_short": "Скачать CV",
    "order_kwork": "Заказать на Kwork",
    "hero_scroll": "Листайте",
    "hero_sub": "Создаю быстрые и современные сайты на Python и Django — от серверной части до удобной админ-панели.",
    "available": "Открыт для новых проектов",
    "hero_tagline": "Быстрые и современные сайты, которые помогают бизнесу расти",
    "view_projects": "Смотреть проекты",
    "years_experience": "Лет учёбы и практики",
    "works_big": "Работы",
    "works_bg": "Works",
    "discover_projects": "Посмотрите мои проекты",
    "selected_works": "Избранные работы",
    "tech_stack": "Технологии",
    "tech_stack_title": "С чем я работаю",
    "lets_create": "Давайте создадим что-то стоящее",
    "write_telegram": "Написать в Telegram",
    "send_email": "Написать на почту",
    "quick_links": "Быстрые ссылки",
    "back_to_top": "Наверх",
    "all_rights": "Все права защищены",
})


# ─── Baza keshi (per-process) ─────────────────────────────────────────────────
_db_cache: dict[str, dict[str, str]] | None = None


def _load_db_overrides() -> dict[str, dict[str, str]]:
    """UiString bazadan o'qib, {lang: {key: text}} qaytaradi."""
    global _db_cache
    if _db_cache is not None:
        return _db_cache
    try:
        from .models import UiString  # noqa: PLC0415
        result: dict[str, dict[str, str]] = {"uz": {}, "en": {}, "ru": {}}
        for obj in UiString.objects.all():
            for lang, field in (("uz", obj.text_uz), ("en", obj.text_en), ("ru", obj.text_ru)):
                if field.strip():
                    result[lang][obj.key] = field.strip()
        _db_cache = result
    except Exception:  # migrations, tests, setup
        _db_cache = {"uz": {}, "en": {}, "ru": {}}
    return _db_cache


def invalidate_ui_cache() -> None:
    """Baza o'zgarsa keshni tozalash."""
    global _db_cache
    _db_cache = None


def ui_text(key: str) -> str:
    lang = (get_language() or "en")[:2]
    db = _load_db_overrides()
    # 1. Baza ustuvor
    val = db.get(lang, {}).get(key) or db.get("en", {}).get(key)
    if val:
        return val
    # 2. Zaxira: kod ichidagi qiymat
    bucket = _TEXTS.get(lang) or _TEXTS["en"]
    return bucket.get(key) or _TEXTS["en"].get(key, key)


def get_all_keys() -> list[str]:
    """Barcha mavjud UI kalit nomlarini qaytaradi."""
    return sorted(_TEXTS["en"].keys())


def get_default(key: str, lang: str) -> str:
    """Kod ichidagi standart qiymatni qaytaradi."""
    return (_TEXTS.get(lang) or _TEXTS["en"]).get(key, "")
