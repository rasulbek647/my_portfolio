"""Foydalanuvchi kiritgan qisqa kontakt qiymatlarini havolaga aylantirish."""

from __future__ import annotations

import re


def ensure_url(raw: str | None) -> str:
    v = (raw or "").strip()
    if not v:
        return ""
    if v.startswith(("http://", "https://")):
        return v
    return f"https://{v.lstrip('/')}"


def telegram_href(raw: str | None) -> str:
    v = (raw or "").strip()
    if not v:
        return ""
    low = v.lower()
    if low.startswith("http://") or low.startswith("https://"):
        return v
    u = v.split("/")[-1].lstrip("@")
    if not u:
        return ""
    return f"https://t.me/{u}"


def instagram_href(raw: str | None) -> str:
    v = (raw or "").strip()
    if not v:
        return ""
    low = v.lower()
    if low.startswith("http://") or low.startswith("https://"):
        return v
    u = v.split("/")[-1].lstrip("@").rstrip("/")
    if not u:
        return ""
    return f"https://instagram.com/{u}"


def whatsapp_href(raw: str | None) -> str:
    v = (raw or "").strip()
    if not v:
        return ""
    low = v.lower()
    if low.startswith("http://") or low.startswith("https://"):
        return v
    digits = re.sub(r"\D", "", v)
    if not digits:
        return ""
    return f"https://wa.me/{digits}"


def telegram_label(raw: str | None) -> str:
    v = (raw or "").strip()
    if not v:
        return ""
    if v.lower().startswith("http"):
        return v
    return f"@{v.lstrip('@').split('/')[-1]}"


def instagram_label(raw: str | None) -> str:
    v = (raw or "").strip()
    if not v:
        return ""
    if v.lower().startswith("http"):
        return v
    return f"@{v.lstrip('@').split('/')[-1]}"


def phone_tel_href(raw: str | None) -> str:
    v = (raw or "").strip()
    if not v:
        return ""
    compact = re.sub(r"[\s\-().]+", "", v)
    return f"tel:{compact}" if compact else f"tel:{v}"
