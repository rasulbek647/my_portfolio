"""Tanlangan tilda professional CV PDF (WeasyPrint + ReportLab fallback)."""

from __future__ import annotations

import os
import re
from io import BytesIO
from typing import Any
from xml.sax.saxutils import escape

from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib import colors

from .i18n_field import localized_model_value
from .models import Certificate, Education, Interest, ResumeProfile, WorkExperience

try:
    from weasyprint import HTML as WeasyHTML
except Exception:  # noqa: BLE001
    WeasyHTML = None  # type: ignore[misc, assignment]


# ==============================================================
# UI LABELS - Tilga qarab
# ==============================================================
_LABELS: dict[str, dict[str, str]] = {
    "en": {
        "contact": "Contact",
        "email": "Email",
        "phone": "Phone",
        "location": "Location",
        "website": "Website",
        "skills": "Skills",
        "about": "About Me",
        "experience": "Work Experience",
        "education": "Education",
        "certificates": "Certificates",
        "interests": "Interests",
        "present": "Present",
        "generated": "Generated",
    },
    "uz": {
        "contact": "Aloqa",
        "email": "Email",
        "phone": "Telefon",
        "location": "Joylashuv",
        "website": "Sayt",
        "skills": "Ko'nikmalar",
        "about": "Men haqimda",
        "experience": "Ish tajribasi",
        "education": "Ta'lim",
        "certificates": "Sertifikatlar",
        "interests": "Qiziqishlar",
        "present": "Hozirgi",
        "generated": "Yaratildi",
    },
    "ru": {
        "contact": "Контакты",
        "email": "Email",
        "phone": "Телефон",
        "location": "Местоположение",
        "website": "Сайт",
        "skills": "Навыки",
        "about": "Обо мне",
        "experience": "Опыт работы",
        "education": "Образование",
        "certificates": "Сертификаты",
        "interests": "Интересы",
        "present": "Настоящее время",
        "generated": "Создано",
    },
}


def _get_labels(lang: str) -> dict[str, str]:
    return _LABELS.get(lang[:2].lower(), _LABELS["en"])


def _format_period(start_date: Any, end_date: Any, is_current: bool, lang: str) -> str:
    labels = _get_labels(lang)
    start_str = start_date.strftime("%b %Y") if start_date else ""
    if is_current:
        end_str = labels["present"]
    elif end_date:
        end_str = end_date.strftime("%b %Y")
    else:
        end_str = ""
    if start_str and end_str:
        return f"{start_str} — {end_str}"
    return start_str or end_str


def _parse_skills(skills_text: str) -> list[str]:
    if not skills_text:
        return []
    skills = re.split(r'[,;\n]+', skills_text)
    return [s.strip() for s in skills if s.strip()]


# ==============================================================
# REPORTLAB FALLBACK - Styled PDF
# ==============================================================
def _build_reportlab_pdf(lang: str, labels: dict, profile: ResumeProfile) -> bytes:
    """ReportLab bilan professional PDF yaratadi (fallback)."""
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=15 * mm,
        bottomMargin=15 * mm,
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=4,
    )
    
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#6C5CE7'),
        spaceAfter=10,
    )
    
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.HexColor('#1a1a2e'),
        spaceBefore=12,
        spaceAfter=4,
        borderPadding=3,
    )
    
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        spaceAfter=3,
    )
    
    item_title_style = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold',
        spaceAfter=1,
    )
    
    item_subtitle_style = ParagraphStyle(
        'ItemSubtitle',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#00a8a5'),
        spaceAfter=1,
    )
    
    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=7,
        textColor=colors.grey,
        alignment=2,
    )

    story: list = []

    # HEADER
    full_name = localized_model_value(profile, "full_name", lang) or "CV"
    story.append(Paragraph(escape(full_name), title_style))
    
    headline = localized_model_value(profile, "headline", lang)
    if headline:
        story.append(Paragraph(escape(headline), subtitle_style))
    
    contact_parts = []
    if profile.email:
        contact_parts.append(profile.email)
    if profile.phone:
        contact_parts.append(profile.phone)
    loc = localized_model_value(profile, "location", lang)
    if loc:
        contact_parts.append(loc)
    
    if contact_parts:
        story.append(Paragraph(escape(" | ".join(contact_parts)), body_style))
    
    story.append(Spacer(1, 8))

    # ABOUT
    about = localized_model_value(profile, "about", lang)
    if about:
        story.append(Paragraph(f"<b>{labels['about'].upper()}</b>", section_style))
        story.append(Paragraph(escape(about).replace("\n", "<br/>"), body_style))
        story.append(Spacer(1, 6))

    # SKILLS
    skills_raw = localized_model_value(profile, "skills", lang)
    skills = _parse_skills(skills_raw)
    if skills:
        story.append(Paragraph(f"<b>{labels['skills'].upper()}</b>", section_style))
        story.append(Paragraph(escape(" • ".join(skills)), body_style))
        story.append(Spacer(1, 6))

    # EXPERIENCE
    exps = WorkExperience.objects.all().order_by("sort_order", "-start_date")
    experiences_data = [e for e in exps if localized_model_value(e, "role", lang) or localized_model_value(e, "company", lang)]
    
    if experiences_data:
        story.append(Paragraph(f"<b>{labels['experience'].upper()}</b>", section_style))
        for exp in experiences_data:
            role = localized_model_value(exp, "role", lang) or ""
            company = localized_model_value(exp, "company", lang) or ""
            desc = localized_model_value(exp, "description", lang)
            period = _format_period(exp.start_date, exp.end_date, exp.is_current, lang)
            
            title_text = f"{role} — {company}".strip(" —")
            story.append(Paragraph(escape(title_text), item_title_style))
            if period:
                story.append(Paragraph(escape(period), item_subtitle_style))
            if desc:
                story.append(Paragraph(escape(desc).replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 3))

    # EDUCATION
    edus = Education.objects.all().order_by("sort_order", "-start_date")
    education_data = [e for e in edus if localized_model_value(e, "degree", lang) or localized_model_value(e, "institution", lang)]
    
    if education_data:
        story.append(Paragraph(f"<b>{labels['education'].upper()}</b>", section_style))
        for edu in education_data:
            degree = localized_model_value(edu, "degree", lang) or ""
            institution = localized_model_value(edu, "institution", lang) or ""
            desc = localized_model_value(edu, "description", lang)
            period = _format_period(edu.start_date, edu.end_date, False, lang)
            
            title_text = f"{degree} — {institution}".strip(" —")
            story.append(Paragraph(escape(title_text), item_title_style))
            if period:
                story.append(Paragraph(escape(period), item_subtitle_style))
            if desc:
                story.append(Paragraph(escape(desc).replace("\n", "<br/>"), body_style))
            story.append(Spacer(1, 3))
        story.append(Spacer(1, 3))

    # CERTIFICATES
    certs = Certificate.objects.all().order_by("sort_order")
    certificates_data = [c for c in certs if localized_model_value(c, "title", lang)]
    
    if certificates_data:
        story.append(Paragraph(f"<b>{labels['certificates'].upper()}</b>", section_style))
        for cert in certificates_data:
            title = localized_model_value(cert, "title", lang) or ""
            issuer = localized_model_value(cert, "issuer", lang)
            date_str = cert.issued_on.strftime("%b %Y") if cert.issued_on else None
            
            cert_line = f"• {title}"
            if issuer:
                cert_line += f" — {issuer}"
            if date_str:
                cert_line += f" ({date_str})"
            story.append(Paragraph(escape(cert_line), body_style))
        story.append(Spacer(1, 6))

    # INTERESTS
    ints = Interest.objects.all().order_by("sort_order")
    interests_data = [localized_model_value(i, "label", lang) for i in ints if localized_model_value(i, "label", lang)]
    
    if interests_data:
        story.append(Paragraph(f"<b>{labels['interests'].upper()}</b>", section_style))
        story.append(Paragraph(escape(" • ".join(interests_data)), body_style))
        story.append(Spacer(1, 6))

    # Footer
    story.append(Spacer(1, 15))
    story.append(Paragraph(f"{labels['generated']}: {timezone.now().strftime('%Y-%m-%d')}", small_style))

    doc.build(story)
    return buf.getvalue()


# ==============================================================
# WEASYPRINT PDF
# ==============================================================
def _get_photo_path(profile: ResumeProfile) -> str | None:
    if not profile.photo:
        return None
    try:
        return os.path.join(settings.MEDIA_ROOT, str(profile.photo))
    except Exception:
        return None


def _build_weasyprint_pdf(lang: str, labels: dict, profile: ResumeProfile) -> bytes | None:
    """WeasyPrint bilan PDF yaratadi."""
    if WeasyHTML is None:
        return None
    
    try:
        full_name = localized_model_value(profile, "full_name", lang) or "CV"
        headline = localized_model_value(profile, "headline", lang)
        about = localized_model_value(profile, "about", lang)
        location = localized_model_value(profile, "location", lang)
        skills = _parse_skills(localized_model_value(profile, "skills", lang) or "")
        photo_path = _get_photo_path(profile)
        
        has_contact = any([profile.email, profile.phone, location, profile.linkedin, profile.github, profile.website])
        
        experiences_data = []
        for exp in WorkExperience.objects.all().order_by("sort_order", "-start_date"):
            role = localized_model_value(exp, "role", lang)
            company = localized_model_value(exp, "company", lang)
            if role or company:
                experiences_data.append({
                    "role": role or "",
                    "company": company or "",
                    "description": localized_model_value(exp, "description", lang),
                    "period": _format_period(exp.start_date, exp.end_date, exp.is_current, lang),
                })
        
        education_data = []
        for edu in Education.objects.all().order_by("sort_order", "-start_date"):
            degree = localized_model_value(edu, "degree", lang)
            institution = localized_model_value(edu, "institution", lang)
            if degree or institution:
                education_data.append({
                    "degree": degree or "",
                    "institution": institution or "",
                    "description": localized_model_value(edu, "description", lang),
                    "period": _format_period(edu.start_date, edu.end_date, False, lang),
                })
        
        certificates_data = []
        for cert in Certificate.objects.all().order_by("sort_order"):
            title = localized_model_value(cert, "title", lang)
            if title:
                certificates_data.append({
                    "title": title,
                    "issuer": localized_model_value(cert, "issuer", lang),
                    "date": cert.issued_on.strftime("%b %Y") if cert.issued_on else None,
                })
        
        interests_data = [localized_model_value(i, "label", lang) for i in Interest.objects.all().order_by("sort_order") if localized_model_value(i, "label", lang)]
        
        context = {
            "lang": lang,
            "profile": profile,
            "full_name": full_name,
            "headline": headline,
            "about": about,
            "location": location,
            "skills": skills,
            "photo_path": photo_path,
            "has_contact": has_contact,
            "labels": labels,
            "experiences": experiences_data,
            "education": education_data,
            "certificates": certificates_data,
            "interests": interests_data,
            "generated_date": timezone.now().strftime("%Y-%m-%d"),
        }
        
        html_string = render_to_string("resume/cv_pdf_template.html", context)
        html = WeasyHTML(string=html_string, base_url=settings.BASE_DIR)
        return html.write_pdf()
    except Exception:
        return None


# ==============================================================
# MAIN FUNCTION
# ==============================================================
def build_cv_pdf_bytes(lang: str) -> bytes:
    """
    Professional CV PDF yaratadi.
    - Avval WeasyPrint urinib ko'riladi
    - Agar ishlamasa, ReportLab fallback ishlatiladi
    """
    lang = (lang or "en")[:2].lower()
    if lang not in ("en", "uz", "ru"):
        lang = "en"
    
    profile = ResumeProfile.load()
    labels = _get_labels(lang)
    
    # 1. WeasyPrint urinib ko'ramiz
    if WeasyHTML is not None:
        pdf = _build_weasyprint_pdf(lang, labels, profile)
        if pdf:
            return pdf
    
    # 2. Fallback: ReportLab
    return _build_reportlab_pdf(lang, labels, profile)
