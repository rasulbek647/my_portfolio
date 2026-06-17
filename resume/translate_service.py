"""Matnni avtomatik tarjima qilish va manba maydonlardan _en/_uz/_ru to'ldirish."""

from __future__ import annotations

import re
from typing import Any

try:
    from deep_translator import GoogleTranslator
except ImportError:  # pragma: no cover
    GoogleTranslator = None  # type: ignore[misc, assignment]

_MAX_LEN: dict[str, int] = {
    "full_name": 200,
    "headline": 300,
    "location": 200,
    "title": 300,
    "issuer": 200,
    "company": 200,
    "role": 300,
    "institution": 300,
    "degree": 300,
    "label": 200,
}

# ==============================================================
# DO NOT TRANSLATE — bu so'zlar hech qachon tarjima qilinmaydi
# (tartib muhim: uzunroq so'zlar oldin — "Fullstack" "Full"dan oldin)
# ==============================================================
PROTECTED_TERMS: list[str] = [
    # Frameworks & languages
    "JavaScript",
    "TypeScript",
    "Python",
    "Django",
    "FastAPI",
    "Flask",
    "Node.js",
    "Node",
    "React",
    "React Native",
    "Next.js",
    "Next",
    "Vue.js",
    "Vue",
    "Angular",
    "Svelte",
    "Express.js",
    "Express",
    "Spring Boot",
    "Spring",
    "Laravel",
    "Ruby on Rails",
    "Rails",
    "Ruby",
    "Kotlin",
    "Swift",
    "Rust",
    "Go",
    "PHP",
    "Java",
    "Scala",
    "Haskell",
    "Elixir",
    "Erlang",
    "Dart",
    "Flutter",
    # Web tech
    "HTML",
    "CSS",
    "SASS",
    "SCSS",
    "GraphQL",
    "REST",
    "gRPC",
    "WebSocket",
    "OAuth",
    "JWT",
    # Roles & stack
    "Fullstack",
    "Full-stack",
    "Frontend",
    "Front-end",
    "Backend",
    "Back-end",
    "DevOps",
    "MLOps",
    # Databases & infra
    "PostgreSQL",
    "MySQL",
    "SQLite",
    "MongoDB",
    "Redis",
    "Elasticsearch",
    "Cassandra",
    "Firebase",
    "Supabase",
    "SQL",
    "NoSQL",
    "Docker",
    "Kubernetes",
    "Nginx",
    "Apache",
    "Linux",
    "Ubuntu",
    "Git",
    "GitHub",
    "GitLab",
    "CI/CD",
    "AWS",
    "GCP",
    "Azure",
    # Data / AI
    "TensorFlow",
    "PyTorch",
    "Keras",
    "Pandas",
    "NumPy",
    "Jupyter",
    "Celery",
    "RabbitMQ",
    "Kafka",
    # Other
    "API",
    "SDK",
    "UI",
    "UX",
    "UI/UX",
    "SaaS",
    "CRM",
    "ERP",
    "MVP",
    "SEO",
    "CMS",
]


def _build_placeholder_map(text: str) -> tuple[str, dict[str, str]]:
    """
    Himoyalangan so'zlarni placeholder bilan almashtiradi.

    Qaytaradi:
        modified_text  — placeholder kiritilgan matn
        restore_map    — {placeholder: original_term}
    """
    restore_map: dict[str, str] = {}
    counter = 0

    # Uzunroqdan qisqaga tartiblangan so'zlar (noto'g'ri match oldini olish uchun)
    sorted_terms = sorted(PROTECTED_TERMS, key=len, reverse=True)

    for term in sorted_terms:
        # So'z chegarasiga mos (case-sensitive: Python != python)
        pattern = re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)")
        if pattern.search(text):
            placeholder = f"__TECH{counter}__"
            restore_map[placeholder] = term
            text = pattern.sub(placeholder, text)
            counter += 1

    return text, restore_map


def _restore_placeholders(text: str, restore_map: dict[str, str]) -> str:
    """Placeholder larni asl texnik so'zlar bilan qaytaradi."""
    for placeholder, term in restore_map.items():
        text = text.replace(placeholder, term)
    return text


def _clip(base: str, text: str) -> str:
    text = (text or "").strip()
    m = _MAX_LEN.get(base)
    if m and len(text) > m:
        return text[:m]
    return text


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    text = (text or "").strip()
    if not text or source_lang == target_lang:
        return text
    if GoogleTranslator is None:
        return ""
    try:
        # 1. Himoyalangan so'zlarni placeholder bilan almashtir
        protected_text, restore_map = _build_placeholder_map(text)

        tr = GoogleTranslator(
            source=source_lang if source_lang != "auto" else "auto",
            target=target_lang,
        )

        if len(protected_text) <= 4500:
            translated = (tr.translate(protected_text) or "").strip()
        else:
            chunks: list[str] = []
            for part in protected_text.split("\n\n"):
                p = part.strip()
                if not p:
                    chunks.append("")
                    continue
                piece = p[:4500] if len(p) > 4500 else p
                chunks.append((tr.translate(piece) or "").strip())
            translated = "\n\n".join(chunks).strip()

        # 2. Placeholder larni qaytarish
        return _restore_placeholders(translated, restore_map)
    except Exception:
        return ""


def translate_text_auto(text: str, target_lang: str) -> str:
    text = (text or "").strip()
    if not text or GoogleTranslator is None:
        return ""
    if target_lang not in ("en", "uz", "ru"):
        return ""
    try:
        # 1. Himoyalangan so'zlarni placeholder bilan almashtir
        protected_text, restore_map = _build_placeholder_map(text)

        tr = GoogleTranslator(source="auto", target=target_lang)

        if len(protected_text) <= 4500:
            translated = (tr.translate(protected_text) or "").strip()
        else:
            out: list[str] = []
            for part in protected_text.split("\n\n"):
                p = part.strip()
                if not p:
                    out.append("")
                    continue
                piece = p[:4500] if len(p) > 4500 else p
                out.append((tr.translate(piece) or "").strip())
            translated = "\n\n".join(out).strip()

        # 2. Placeholder larni qaytarish
        return _restore_placeholders(translated, restore_map)
    except Exception:
        return ""


def sync_translations_from_source(obj: Any, bases: list[str]) -> None:
    """
    Manba maydon o'zgarganda _en/_uz/_ru slotlarini yangilaydi yoki tozalaydi.

    QOIDALAR:
    - Source (base) TO'LDIRILGANda  -> _en/_uz/_ru ni YANGI qiymat bilan YANGILAT
      (eski qiymatlarga QARAMAY -- doim ustiga yoz)
    - Source (base) BO'SH bo'lganda  -> _en/_uz/_ru ni ham TOZALA ("")
    """
    for base in bases:
        # 1. Manba maydonni o'qi
        src = ""
        raw_base = getattr(obj, base, None)
        if raw_base is not None and str(raw_base).strip():
            src = str(raw_base).strip()

        # 2. Manba BO'SH bo'lsa -> barcha til maydonlarini tozala va keyingisiga o't
        if not src:
            for lang in ("en", "uz", "ru"):
                key = f"{base}_{lang}"
                if hasattr(obj, key):
                    setattr(obj, key, "")
            continue

        # 3. Manba maydonni kesilgan holda saqlat
        if base in _MAX_LEN:
            src = _clip(base, src)
            setattr(obj, base, src)

        # 4. BARCHA til slotlarini yangilat (eski qiymatga QARAMAY -- doim ustiga yoz)
        for lang in ("en", "uz", "ru"):
            key = f"{base}_{lang}"
            if not hasattr(obj, key):
                continue
            tr = translate_text_auto(src, lang)
            final = tr if tr else src
            if base in _MAX_LEN:
                final = _clip(base, final)
            setattr(obj, key, final)


def fill_empty_language_fields(obj: Any, source_lang: str, bases: list[str]) -> None:
    sync_translations_from_source(obj, bases)
