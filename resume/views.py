from django.http import HttpResponse
from django.shortcuts import render
from django.utils import translation

from .models import Certificate, ContactLink, Education, Interest, Portfolio, ResumeProfile, WorkExperience
from .pdf_export import build_cv_pdf_bytes


def cv_home(request):
    # Har safar DB dan FRESH query -- hech qanday cache ishlatilmaydi
    profile = ResumeProfile.objects.filter(pk=1).first()
    certificates = Certificate.objects.all().order_by("sort_order", "pk")
    interests = Interest.objects.all().order_by("sort_order", "pk")
    experiences = WorkExperience.objects.all().order_by("sort_order", "-start_date", "pk")
    education_entries = Education.objects.all().order_by("sort_order", "-start_date", "pk")
    portfolios = Portfolio.objects.all().order_by("sort_order", "pk")
    extra_contact_links = ContactLink.objects.all().order_by("sort_order", "pk")
    return render(
        request,
        "resume/home.html",
        {
            "profile": profile,
            "certificates": certificates,
            "interests": interests,
            "experiences": experiences,
            "education_entries": education_entries,
            "portfolios": portfolios,
            "extra_contact_links": extra_contact_links,
        },
    )


def cv_pdf(request):
    """Joriy yoki ?lang= bo'yicha til — PDF yuklash."""
    lang = (request.GET.get("lang") or "")[:2]
    if lang not in ("en", "uz", "ru"):
        active = translation.get_language() or "en"
        lang = active.replace("-", "_").split("_")[0][:2]
    if lang not in ("en", "uz", "ru"):
        lang = "en"
    data = build_cv_pdf_bytes(lang)
    response = HttpResponse(data, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="cv-{lang}.pdf"'
    return response
