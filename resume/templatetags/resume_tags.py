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
def dynamic_contact_icon(icon_key: str | None, name: str = "", url: str = "") -> str:
    """Qaytaradigan narsa - SVG kontent (string)."""
    return mark_safe(svg_for_icon(icon_key, name, url))


@register.filter
def split_skill_tags(value):
    """Ko‘nikmalar matnini qatorlar va vergul bo‘yicha ajratadi.

    Qavs ichidagi vergul ajratmaydi: «Serverga joylash (Railway, Render)» — bitta element.
    """
    if not value:
        return []
    out: list[str] = []
    buf: list[str] = []
    depth = 0

    def flush():
        item = "".join(buf).strip()
        if item:
            out.append(item)
        buf.clear()

    for ch in str(value):
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth = max(depth - 1, 0)
        if ch == "\n" or (ch == "," and depth == 0):
            flush()
            if ch == "\n":
                depth = 0
            continue
        buf.append(ch)
    flush()
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


@register.simple_tag
def get_social_color(name: str, url: str) -> str:
    """Return a brand hex color based on the link name or URL."""
    name_str = (name or "").lower()
    url_str = (url or "").lower()
    
    if "facebook" in name_str or "facebook.com" in url_str: return "#1877F2"
    if "twitter" in name_str or "x.com" in url_str or "twitter.com" in url_str: return "#000000"
    if "youtube" in name_str or "youtube.com" in url_str or "youtu.be" in url_str: return "#FF0000"
    if "discord" in name_str or "discord" in url_str: return "#5865F2"
    if "tiktok" in name_str or "tiktok.com" in url_str: return "#000000"
    if "behance" in name_str or "behance.net" in url_str: return "#1769FF"
    if "dribbble" in name_str or "dribbble.com" in url_str: return "#EA4C89"
    if "snapchat" in name_str or "snapchat.com" in url_str: return "#FFFC00"
    if "pinterest" in name_str or "pinterest.com" in url_str: return "#E60023"
    if "reddit" in name_str or "reddit.com" in url_str: return "#FF4500"
    if "twitch" in name_str or "twitch.tv" in url_str: return "#9146FF"
    if "medium" in name_str or "medium.com" in url_str: return "#000000"
    if "spotify" in name_str or "spotify.com" in url_str: return "#1DB954"
    if "steam" in name_str or "steampowered" in url_str: return "#000000"
    if "vk" in name_str or "vk.com" in url_str: return "#0077FF"
    if "vimeo" in name_str or "vimeo.com" in url_str: return "#1AB7EA"
    if "patreon" in name_str or "patreon.com" in url_str: return "#FF424D"
    if "figma" in name_str or "figma.com" in url_str: return "#F24E1E"
    
    return "#8B5CF6"  # Default violet



_BULLET_CHARS = "•·▪◦‣-–—*"


@register.filter
def split_lines(value):
    """Tavsifni punktlarga ajratadi: har bir qator (yoki «•» belgisi) alohida punkt."""
    if not value:
        return []
    text = str(value).replace("\r", "")
    out: list[str] = []
    for line in text.split("\n"):
        for chunk in line.split("•"):
            s = chunk.strip().lstrip(_BULLET_CHARS).strip()
            if s:
                out.append(s)
    return out


def _plural_ru(n: int, one: str, few: str, many: str) -> str:
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


@register.simple_tag
def job_duration(start, end=None, current=False):
    """Ish davomiyligi: «2 yil 3 oy» / «2 yrs 3 mos» / «2 года 3 месяца»."""
    if not start:
        return ""
    from django.utils import timezone

    if current:
        end = timezone.localdate()
    elif not end:
        return ""
    months = (end.year - start.year) * 12 + (end.month - start.month) + 1
    months = max(months, 1)
    years, rest = divmod(months, 12)
    lang = (get_language() or "en")[:2]
    parts = []
    if lang == "uz":
        if years:
            parts.append(f"{years} yil")
        if rest:
            parts.append(f"{rest} oy")
    elif lang == "ru":
        if years:
            parts.append(f"{years} {_plural_ru(years, 'год', 'года', 'лет')}")
        if rest:
            parts.append(f"{rest} {_plural_ru(rest, 'месяц', 'месяца', 'месяцев')}")
    else:
        if years:
            parts.append(f"{years} {'yr' if years == 1 else 'yrs'}")
        if rest:
            parts.append(f"{rest} {'mo' if rest == 1 else 'mos'}")
    return " ".join(parts)


@register.filter
def initials(value):
    """«Matyoqubov Rasulbek» → «MR» (logotip belgisi uchun)."""
    words = [w for w in str(value or "").replace("-", " ").split() if w[:1].isalpha()]
    return "".join(w[0] for w in words[:2]).upper()


@register.filter
def split_paragraphs(value):
    """Matnni xatboshilarga ajratadi (bo'sh qator yoki yangi qator bo'yicha)."""
    if not value:
        return []
    text = str(value).replace("\r", "").strip()
    parts = [p.strip() for p in text.split("\n\n")] if "\n\n" in text else [p.strip() for p in text.split("\n")]
    return [p for p in parts if p]


@register.simple_tag
def years_since(*querysets):
    """Ta'lim/tajriba yozuvlaridagi eng erta boshlanish sanasidan beri o'tgan yillar."""
    from django.utils import timezone

    starts = []
    for qs in querysets:
        for obj in qs or []:
            d = getattr(obj, "start_date", None)
            if d:
                starts.append(d)
    if not starts:
        return ""
    today = timezone.localdate()
    first = min(starts)
    years = today.year - first.year - ((today.month, today.day) < (first.month, first.day))
    return max(years, 1)


_TECH_SLUGS = {
    "python": "python", "django": "django", "javascript": "javascript", "js": "javascript",
    "typescript": "typescript", "ts": "typescript", "html": "html5", "html5": "html5",
    "css": "css", "css3": "css", "tailwind": "tailwindcss", "tailwind css": "tailwindcss",
    "tailwindcss": "tailwindcss", "bootstrap": "bootstrap", "postgresql": "postgresql",
    "postgres": "postgresql", "mysql": "mysql", "sqlite": "sqlite", "redis": "redis",
    "git": "git", "github": "github", "git & github": "github", "git va github": "github",
    "git и github": "github", "docker": "docker", "react": "react", "next.js": "nextdotjs",
    "nextjs": "nextdotjs", "node.js": "nodedotjs", "nodejs": "nodedotjs", "vue": "vuedotjs",
    "jquery": "jquery", "php": "php", "laravel": "laravel", "figma": "figma", "linux": "linux",
    "nginx": "nginx", "telegram": "telegram", "telegram bot": "telegram", "prisma": "prisma",
    "fastapi": "fastapi", "flask": "flask", "sass": "sass",
    "railway": "railway", "render": "render", "vercel": "vercel", "cloudinary": "cloudinary",
}


@register.filter
def tech_icon_slug(value):
    """Ko'nikma nomidan Simple Icons belgisi (topilmasa — bo'sh)."""
    key = str(value or "").strip().lower()
    if key in _TECH_SLUGS:
        return _TECH_SLUGS[key]
    import re

    for name, slug in _TECH_SLUGS.items():
        if len(name) > 2 and re.search(r"(?<![\w.])" + re.escape(name) + r"(?![\w.])", key):
            return slug
    return ""


_TECH_GLYPHS = (
    ("api", ("api", "rest", "graphql", "endpoint")),
    ("responsive", ("adaptiv", "adaptive", "responsive", "адаптив", "mobil", "mobile")),
    ("admin", ("admin", "админ", "panel", "панел", "dashboard", "crm")),
    ("lang", ("tilli", " til", "language", "multilingual", "i18n", "язык", "мультияз")),
    ("deploy", ("server", "сервер", "deploy", "деплой", "hosting", "хостинг", "joylash")),
    ("db", ("sql", "database", "baza", "база", "orm")),
    ("bot", ("bot", "бот")),
    ("design", ("dizayn", "design", "дизайн", " ui", " ux")),
)


@register.filter
def tech_glyph(value):
    """Logotipi yo'q ko'nikma uchun oddiy belgi nomi (api, responsive, admin, lang, deploy, ...)."""
    key = " " + str(value or "").strip().lower()
    for glyph, words in _TECH_GLYPHS:
        if any(w in key for w in words):
            return glyph
    return "code"


@register.filter
def url_domain(value):
    """«https://kelajakuylar.uz/uy/5» → «kelajakuylar.uz»."""
    from urllib.parse import urlparse

    if not value:
        return ""
    raw = str(value).strip()
    host = urlparse(raw if "://" in raw else "https://" + raw).netloc
    return host[4:] if host.startswith("www.") else host


_THEME_PALETTE_CACHE: dict[str, dict[str, str]] = {}


@register.simple_tag
def theme_palette(slug):
    """Mavzu CSS faylidan asosiy ranglarni o'qiydi (admin paneldagi mavzu kartalari uchun)."""
    slug = str(slug or "")
    if slug in _THEME_PALETTE_CACHE:
        return _THEME_PALETTE_CACHE[slug]
    import re as _re
    from django.contrib.staticfiles import finders
    pal = {"bg": "#f4f4f4", "surface": "#ffffff", "text": "#222222", "heading": "#111111", "accent": "#6c5ce7", "accent2": "#a29bfe"}
    path = finders.find(f"css/themes/{slug}.css") if _re.fullmatch(r"[a-z0-9_]+", slug) else None
    if path:
        try:
            with open(path, encoding="utf-8") as fh:
                css = fh.read()
        except OSError:
            css = ""
        found = dict(_re.findall(r"--color-([a-z0-9-]+)\s*:\s*([^;]+);", css))
        for key, var in (("bg", "bg"), ("surface", "surface"), ("text", "text"), ("heading", "heading"), ("accent", "accent"), ("accent2", "accent-2")):
            val = found.get(var, "").strip().lower()
            if _re.fullmatch(r"#[0-9a-f]{3}", val):
                val = "#" + "".join(ch * 2 for ch in val[1:])
            if _re.fullmatch(r"#[0-9a-f]{6}", val):
                pal[key] = val
    _THEME_PALETTE_CACHE[slug] = pal
    return pal



# ----------------------------------------------------------------------------
# Admin panel ranglari sayt mavzusidan olinadi (Sozlamalar → «Admin panel ham mavzu ranglarida»)
def _hex_rgb(h):
    h = (h or "").lstrip("#")
    if len(h) != 6:
        return None
    try:
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return None


def _rgb_hex(rgb):
    return "#%02x%02x%02x" % tuple(max(0, min(255, round(v))) for v in rgb)


def _mix(a, b, t):
    """a dan b ga t ulushda aralashtirish (t=0 → a, t=1 → b)."""
    ra, rb = _hex_rgb(a), _hex_rgb(b)
    if not ra or not rb:
        return a
    return _rgb_hex(tuple(x + (y - x) * t for x, y in zip(ra, rb)))


def _lum(h):
    rgb = _hex_rgb(h) or (128, 128, 128)
    r, g, b = (v / 255 for v in rgb)
    return 0.299 * r + 0.587 * g + 0.114 * b


@register.simple_tag(takes_context=True)
def admin_theme(context):
    """Admin panel uchun ranglar: {'mode': 'light'|'dark', 'css': ':root{...}'}; o'chiq bo'lsa — bo'sh."""
    st = context.get("site_settings")
    if not st or not getattr(st, "admin_follow_theme", False):
        return {"mode": "dark", "css": ""}
    if st.theme == "custom":
        pal = {"bg": st.custom_bg, "surface": st.custom_surface, "text": st.custom_text, "heading": st.custom_heading,
               "accent": st.custom_accent, "accent2": st.custom_accent_2}
    else:
        pal = theme_palette(st.theme)
    bg, surface, text, heading = pal["bg"], pal["surface"], pal["text"], pal["heading"]
    accent, accent2 = pal["accent"], pal["accent2"]
    if not all(_hex_rgb(x) for x in (bg, surface, text, heading, accent, accent2)):
        return {"mode": "dark", "css": ""}
    light = _lum(bg) > 0.5
    if light:
        # Kartalar fondan sezilarli ajralib tursin
        if abs(_lum(surface) - _lum(bg)) < 0.02:
            surface = _mix(bg, "#ffffff", 0.6)
        v = {
            "bg-base": bg, "text-base": text, "ink": text, "strong": heading,
            "bg": bg, "surface": surface, "surface-2": _mix(surface, text, 0.045),
            "field": _mix(surface, "#ffffff", 0.5), "field-focus": _mix(surface, "#ffffff", 0.8), "menu": _mix(surface, "#ffffff", 0.6),
            "accent": accent,
            "accent-light": _mix(accent, "#000000", 0.35) if _lum(accent) > 0.55 else accent,
            "accent-dark": _mix(accent, "#000000", 0.15),
            "teal": _mix(accent2, "#000000", 0.3) if _lum(accent2) > 0.6 else accent2,
            "teal-dark": _mix(accent2, "#000000", 0.25),
        }
    else:
        if abs(_lum(surface) - _lum(bg)) < 0.015:
            surface = _mix(bg, text, 0.05)
        v = {
            "bg-base": bg, "text-base": text, "ink": "#ffffff", "strong": heading,
            "bg": bg, "surface": surface, "surface-2": _mix(surface, text, 0.04),
            "field": _mix(bg, surface, 0.5), "field-focus": surface, "menu": _mix(surface, text, 0.03),
            "accent": accent,
            "accent-light": _mix(accent, "#ffffff", 0.3) if _lum(accent) < 0.75 else accent,
            "accent-dark": _mix(accent, "#000000", 0.12),
            "teal": accent2 if _lum(accent2) > 0.3 else _mix(accent2, "#ffffff", 0.35),
            "teal-dark": _mix(accent2, "#000000", 0.15),
        }
    v["on-accent"] = "#141414" if _lum(accent) > 0.62 else "#ffffff"
    css = ":root{" + ";".join(f"--d-{k}:{val}" for k, val in v.items()) + "}"
    return {"mode": "light" if light else "dark", "css": mark_safe(css)}
