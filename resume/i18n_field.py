"""Ko'p tilli maydonlar: _lang maydon → manba maydon → boshqa til (fallback zanjiri)."""

from __future__ import annotations

from typing import Any


def localized_model_value(obj: Any, base_name: str, lang_code: str) -> str:
    """
    Til ketma-ketligi:
      1) {base}_{lang}        -- joriy til (masalan: full_name_en)
      2) {base}               -- manba maydon (faqat _lang bo'sh EMAS bo'lsa ishlaydi)
      3) bo'sh qaytaradi      -- agar hamma joy bo'sh bo'lsa

    MUHIM: Agar {base}_{lang} bo'sh bo'lsa va boshqa tillarda ham bo'sh bo'lsa,
    bu field uchun bo'sh string qaytadi. Template {% if %} bilan boshqaradi.
    """
    code = (lang_code or "en")[:2]
    suf_map = {"en": "_en", "uz": "_uz", "ru": "_ru"}
    suf = suf_map.get(code, "_en")

    # 1. Joriy til maydonini tekshir
    v = getattr(obj, f"{base_name}{suf}", None)
    if v is not None and str(v).strip():
        return str(v).strip()

    # 2. Boshqa til maydonlari ham bo'sh bo'lsa -> manba maydon qaytmas
    #    (chunki sync_translations_from_source endi _lang ni source bilan sinxronlashtiradi)
    #    Faqat boshqa tillarda ma'lumot bor bo'lsa fallback qil
    for fb_suf in ("_en", "_uz", "_ru"):
        if fb_suf == suf:
            continue
        fb_v = getattr(obj, f"{base_name}{fb_suf}", None)
        if fb_v is not None and str(fb_v).strip():
            return str(fb_v).strip()

    # 3. Hamma _lang bo'sh bo'lsa -> manba maydonni qaytarma, bo'sh qaytar
    return ""
