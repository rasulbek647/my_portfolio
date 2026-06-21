from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from urllib.parse import quote

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods

from .admin_content_lang import SESSION_KEY_UI, VALID, get_ui_lang
from .i18n_field import localized_model_value
from .dashboard_i18n import get_dashboard_strings
from .admin_forms import (
    CertificateForm,
    ContactLinkForm,
    EducationForm,
    InterestForm,
    PortfolioForm,
    ResumeProfileForm,
    ServiceForm,
    WorkExperienceForm,
)
from .dashboard_forms import SiteSettingsForm
from .dashboard_style import apply_dashboard_field_styles, field_placeholder
from .models import Certificate, ContactLink, Education, Interest, Portfolio, ResumeProfile, SiteSettings, WorkExperience, UiString, Service
from .ui_strings import invalidate_ui_cache, get_default, get_all_keys


def staff_required(view_func):
    """Login + is_staff."""

    def _wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f"{reverse('dashboard:login')}?next={quote(request.path)}")
        if not request.user.is_staff:
            messages.error(request, "Kirish huquqi yo‘q. Faqat xodimlar.")
            return redirect("dashboard:login")
        return view_func(request, *args, **kwargs)

    return _wrap


def _dash_msg(request, key: str) -> str:
    return get_dashboard_strings(get_ui_lang(request)).get(key, key)


@require_http_methods(["POST"])
def set_dashboard_ui_lang(request):
    """Panel UI tili — POST (sessiya barqaror saqlanadi)."""
    lang = request.POST.get("lang", "")
    if lang in VALID:
        request.session[SESSION_KEY_UI] = lang
        request.session.modified = True
    next_url = request.POST.get("next") or reverse("dashboard:index")
    if not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = reverse("dashboard:index")
    return redirect(next_url)


@staff_required
def dashboard_index(request):
    profile = ResumeProfile.load()
    return render(
        request,
        "dashboard/index.html",
        {
            "section": "dashboard",
            "cert_count": Certificate.objects.count(),
            "interest_count": Interest.objects.count(),
            "experience_count": WorkExperience.objects.count(),
            "education_count": Education.objects.count(),
            "portfolio_count": Portfolio.objects.count(),
            "contact_extra_count": ContactLink.objects.count(),
            "profile": profile,
        },
    )


@staff_required
def dashboard_profile(request):
    profile = ResumeProfile.load()
    if request.method == "POST":
        form = ResumeProfileForm(request.POST, request.FILES, instance=profile)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_profile_saved"))
            return redirect("dashboard:profile")
    else:
        form = ResumeProfileForm(instance=profile)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "full_name": "Masalan: Ali Valiyev",
            "headline": "Masalan: Senior Python dasturchi",
            "about": "O‘zingiz, tajriba va maqsadlaringiz haqida qisqa yozing…",
            "skills": "Python\nDjango\nREST API",
            "location": "Masalan: Toshkent, O‘zbekiston",
            "email": "you@example.com",
            "phone": "+998 90 123 45 67",
            "telegram": "@username yoki https://t.me/username",
            "instagram": "@username",
            "whatsapp": "+998901234567",
            "linkedin": "https://linkedin.com/in/…",
            "github": "https://github.com/…",
            "kwork": "https://kwork.ru/user/…",
            "website": "https://…",
        },
    )

    return render(
        request,
        "dashboard/profile.html",
        {
            "section": "profile",
            "form": form,
        },
    )


@staff_required
def certificate_list(request):
    lang = get_ui_lang(request)
    certificates = Certificate.objects.all()
    return render(
        request,
        "dashboard/certificates/list.html",
        {
            "section": "certificates",
            "certificates": certificates,
            "list_lang": lang,
        },
    )


@staff_required
def certificate_create(request):
    obj = Certificate()
    if request.method == "POST":
        form = CertificateForm(request.POST, request.FILES, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_cert_added"))
            return redirect("dashboard:certificates")
    else:
        form = CertificateForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "title": "Sertifikat nomi",
            "issuer": "Kim tomonidan berilgan (masalan, Coursera)",
            "description": "Qisqa tavsif…",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/certificates/form.html",
        {
            "section": "certificates",
            "form": form,
            "is_edit": False,
        },
    )


@staff_required
def certificate_edit(request, pk):
    obj = get_object_or_404(Certificate, pk=pk)
    if request.method == "POST":
        form = CertificateForm(request.POST, request.FILES, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_saved"))
            return redirect("dashboard:certificates")
    else:
        form = CertificateForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "title": "Sertifikat nomi",
            "issuer": "Beruvchi tashkilot",
            "description": "Tavsif…",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/certificates/form.html",
        {
            "section": "certificates",
            "form": form,
            "is_edit": True,
            "object": obj,
        },
    )


@staff_required
@require_http_methods(["GET", "POST"])
def certificate_delete(request, pk):
    obj = get_object_or_404(Certificate, pk=pk)
    lang = get_ui_lang(request)
    display_title = localized_model_value(obj, "title", lang) or f"#{obj.pk}"

    if request.method == "POST":
        obj.delete()
        messages.success(request, _dash_msg(request, "msg_deleted"))
        return redirect("dashboard:certificates")

    return render(
        request,
        "dashboard/certificates/confirm_delete.html",
        {
            "section": "certificates",
            "object": obj,
            "display_title": display_title,
        },
    )


@staff_required
def portfolio_list(request):
    items = Portfolio.objects.all()
    return render(
        request,
        "dashboard/portfolio/list.html",
        {
            "section": "portfolio",
            "portfolio_items": items,
        },
    )


@staff_required
def portfolio_create(request):
    obj = Portfolio()
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_portfolio_added"))
            return redirect("dashboard:portfolio")
    else:
        form = PortfolioForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "title": "Masalan: E-commerce loyiha",
            "url": "https://",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/portfolio/form.html",
        {
            "section": "portfolio",
            "form": form,
            "is_edit": False,
        },
    )


@staff_required
def portfolio_edit(request, pk):
    obj = get_object_or_404(Portfolio, pk=pk)
    if request.method == "POST":
        form = PortfolioForm(request.POST, request.FILES, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_saved"))
            return redirect("dashboard:portfolio")
    else:
        form = PortfolioForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "title": "Loyiha nomi (ixtiyoriy)",
            "url": "https://",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/portfolio/form.html",
        {
            "section": "portfolio",
            "form": form,
            "is_edit": True,
            "object": obj,
        },
    )


@staff_required
@require_http_methods(["GET", "POST"])
def portfolio_delete(request, pk):
    obj = get_object_or_404(Portfolio, pk=pk)
    display_title = (obj.title or "").strip() or obj.url or f"#{obj.pk}"

    if request.method == "POST":
        obj.delete()
        messages.success(request, _dash_msg(request, "msg_deleted"))
        return redirect("dashboard:portfolio")

    return render(
        request,
        "dashboard/portfolio/confirm_delete.html",
        {
            "section": "portfolio",
            "object": obj,
            "display_title": display_title,
        },
    )


@staff_required
def contact_link_list(request):
    items = ContactLink.objects.all()
    return render(
        request,
        "dashboard/contact_links/list.html",
        {
            "section": "contact_links",
            "contact_link_items": items,
        },
    )


@staff_required
def contact_link_create(request):
    obj = ContactLink()
    if request.method == "POST":
        form = ContactLinkForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_contact_link_added"))
            return redirect("dashboard:contact_links")
    else:
        form = ContactLinkForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "name": "Discord, Behance, …",
            "url": "https://discord.gg/… yoki mysite.com",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/contact_links/form.html",
        {
            "section": "contact_links",
            "form": form,
            "is_edit": False,
        },
    )


@staff_required
def contact_link_edit(request, pk):
    obj = get_object_or_404(ContactLink, pk=pk)
    if request.method == "POST":
        form = ContactLinkForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_saved"))
            return redirect("dashboard:contact_links")
    else:
        form = ContactLinkForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "name": "Platforma nomi",
            "url": "https://",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/contact_links/form.html",
        {
            "section": "contact_links",
            "form": form,
            "is_edit": True,
            "object": obj,
        },
    )


@staff_required
@require_http_methods(["GET", "POST"])
def contact_link_delete(request, pk):
    obj = get_object_or_404(ContactLink, pk=pk)
    display_title = (obj.name or "").strip() or (obj.url or "").strip() or f"#{obj.pk}"

    if request.method == "POST":
        obj.delete()
        messages.success(request, _dash_msg(request, "msg_deleted"))
        return redirect("dashboard:contact_links")

    return render(
        request,
        "dashboard/contact_links/confirm_delete.html",
        {
            "section": "contact_links",
            "object": obj,
            "display_title": display_title,
        },
    )


@staff_required
def interest_list(request):
    lang = get_ui_lang(request)
    interests = Interest.objects.all()
    return render(
        request,
        "dashboard/interests/list.html",
        {
            "section": "interests",
            "interests": interests,
            "list_lang": lang,
        },
    )


@staff_required
def interest_create(request):
    obj = Interest()
    if request.method == "POST":
        form = InterestForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_int_added"))
            return redirect("dashboard:interests")
    else:
        form = InterestForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "label": "Masalan: Fotografiya, o‘qish…",
            "detail": "Batafsil (ixtiyoriy)",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/interests/form.html",
        {
            "section": "interests",
            "form": form,
            "is_edit": False,
        },
    )


@staff_required
def interest_edit(request, pk):
    obj = get_object_or_404(Interest, pk=pk)
    if request.method == "POST":
        form = InterestForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_saved"))
            return redirect("dashboard:interests")
    else:
        form = InterestForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "label": "Qiziqish nomi",
            "detail": "Batafsil",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/interests/form.html",
        {
            "section": "interests",
            "form": form,
            "is_edit": True,
            "object": obj,
        },
    )


@staff_required
@require_http_methods(["GET", "POST"])
def interest_delete(request, pk):
    obj = get_object_or_404(Interest, pk=pk)
    lang = get_ui_lang(request)
    display_label = localized_model_value(obj, "label", lang) or f"#{obj.pk}"

    if request.method == "POST":
        obj.delete()
        messages.success(request, _dash_msg(request, "msg_deleted"))
        return redirect("dashboard:interests")

    return render(
        request,
        "dashboard/interests/confirm_delete.html",
        {
            "section": "interests",
            "object": obj,
            "display_label": display_label,
        },
    )


@staff_required
def experience_list(request):
    lang = get_ui_lang(request)
    items = WorkExperience.objects.all()
    return render(
        request,
        "dashboard/experience/list.html",
        {
            "section": "experience",
            "items": items,
            "list_lang": lang,
        },
    )


@staff_required
def experience_create(request):
    obj = WorkExperience()
    if request.method == "POST":
        form = WorkExperienceForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_exp_added"))
            return redirect("dashboard:experience")
    else:
        form = WorkExperienceForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "company": "ACME Inc.",
            "role": "Senior Developer",
            "description": "Responsibilities…",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/experience/form.html",
        {
            "section": "experience",
            "form": form,
            "is_edit": False,
        },
    )


@staff_required
def experience_edit(request, pk):
    obj = get_object_or_404(WorkExperience, pk=pk)
    if request.method == "POST":
        form = WorkExperienceForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_saved"))
            return redirect("dashboard:experience")
    else:
        form = WorkExperienceForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "company": "",
            "role": "",
            "description": "",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/experience/form.html",
        {
            "section": "experience",
            "form": form,
            "is_edit": True,
            "object": obj,
        },
    )


@staff_required
@require_http_methods(["GET", "POST"])
def experience_delete(request, pk):
    obj = get_object_or_404(WorkExperience, pk=pk)
    lang = get_ui_lang(request)
    role = localized_model_value(obj, "role", lang)
    company = localized_model_value(obj, "company", lang)
    display_title = " — ".join(p for p in (role, company) if p).strip() or f"#{obj.pk}"

    if request.method == "POST":
        obj.delete()
        messages.success(request, _dash_msg(request, "msg_deleted"))
        return redirect("dashboard:experience")

    return render(
        request,
        "dashboard/experience/confirm_delete.html",
        {
            "section": "experience",
            "object": obj,
            "display_title": display_title,
        },
    )


@staff_required
def education_list(request):
    lang = get_ui_lang(request)
    items = Education.objects.all()
    return render(
        request,
        "dashboard/education/list.html",
        {
            "section": "education",
            "items": items,
            "list_lang": lang,
        },
    )


@staff_required
def education_create(request):
    obj = Education()
    if request.method == "POST":
        form = EducationForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_edu_added"))
            return redirect("dashboard:education")
    else:
        form = EducationForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "institution": "MIT",
            "degree": "B.Sc. Computer Science",
            "description": "",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/education/form.html",
        {
            "section": "education",
            "form": form,
            "is_edit": False,
        },
    )


@staff_required
def education_edit(request, pk):
    obj = get_object_or_404(Education, pk=pk)
    if request.method == "POST":
        form = EducationForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_saved"))
            return redirect("dashboard:education")
    else:
        form = EducationForm(instance=obj)
        apply_dashboard_field_styles(form)

    field_placeholder(
        form,
        {
            "institution": "",
            "degree": "",
            "description": "",
            "sort_order": "0",
        },
    )

    return render(
        request,
        "dashboard/education/form.html",
        {
            "section": "education",
            "form": form,
            "is_edit": True,
            "object": obj,
        },
    )


@staff_required
@require_http_methods(["GET", "POST"])
def education_delete(request, pk):
    obj = get_object_or_404(Education, pk=pk)
    lang = get_ui_lang(request)
    inst = localized_model_value(obj, "institution", lang)
    deg = localized_model_value(obj, "degree", lang)
    display_title = " — ".join(p for p in (deg, inst) if p).strip() or f"#{obj.pk}"

    if request.method == "POST":
        obj.delete()
        messages.success(request, _dash_msg(request, "msg_deleted"))
        return redirect("dashboard:education")

    return render(
        request,
        "dashboard/education/confirm_delete.html",
        {
            "section": "education",
            "object": obj,
            "display_title": display_title,
        },
    )


@staff_required
def dashboard_settings(request):
    settings_obj = SiteSettings.load()
    lang = get_ui_lang(request)
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, instance=settings_obj, lang=lang)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, _dash_msg(request, "msg_settings_saved"))
            return redirect("dashboard:settings")
    else:
        form = SiteSettingsForm(instance=settings_obj, lang=lang)
        apply_dashboard_field_styles(form)

    return render(
        request,
        "dashboard/settings.html",
        {
            "section": "settings",
            "form": form,
        },
    )


class DashboardLoginView(LoginView):
    template_name = "dashboard/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        n = self.request.GET.get("next") or self.request.POST.get("next")
        if n and url_has_allowed_host_and_scheme(
            n,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return n
        return reverse("dashboard:index")

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_staff:
            messages.error(self.request, _dash_msg(self.request, "login_staff_only"))
            return self.form_invalid(form)
        return super().form_valid(form)


class DashboardLogoutView(LogoutView):
    next_page = reverse_lazy("dashboard:login")


@staff_required
def sample_list_page(request):
    return render(
        request,
        "dashboard/samples/list.html",
        {"section": "dashboard"},
    )


@staff_required
def sample_form_page(request):
    return render(
        request,
        "dashboard/samples/form.html",
        {"section": "dashboard"},
    )


# ─── UI Strings ───────────────────────────────────────────────────────────────

@staff_required
def ui_strings_list(request):
    """Barcha UI matnlari ro'yxati."""
    strings = UiString.objects.all().order_by("key")
    lang = get_ui_lang(request)
    dash = get_dashboard_strings(lang)
    return render(request, "dashboard/ui_strings/list.html", {
        "strings": strings,
        "section": "ui_strings",
        "dash": dash,
    })


@staff_required
def ui_string_edit(request, pk):
    """Bitta UI matni tahrirlash."""
    obj = get_object_or_404(UiString, pk=pk)
    lang = get_ui_lang(request)
    dash = get_dashboard_strings(lang)
    error = None

    if request.method == "POST":
        obj.text_uz = request.POST.get("text_uz", "").strip()
        obj.text_en = request.POST.get("text_en", "").strip()
        obj.text_ru = request.POST.get("text_ru", "").strip()
        obj.save()
        invalidate_ui_cache()
        messages.success(request, f"'{obj.key}' saqlandi.")
        return redirect("dashboard:ui_strings")

    defaults = {
        "uz": get_default(obj.key, "uz"),
        "en": get_default(obj.key, "en"),
        "ru": get_default(obj.key, "ru"),
    }
    return render(request, "dashboard/ui_strings/edit.html", {
        "obj": obj,
        "defaults": defaults,
        "section": "ui_strings",
        "dash": dash,
        "error": error,
    })


@staff_required
@require_http_methods(["POST"])
def ui_string_reset(request, pk):
    """Standart qiymatga qaytarish."""
    obj = get_object_or_404(UiString, pk=pk)
    obj.text_uz = get_default(obj.key, "uz")
    obj.text_en = get_default(obj.key, "en")
    obj.text_ru = get_default(obj.key, "ru")
    obj.save()
    invalidate_ui_cache()
    messages.success(request, f"'{obj.key}' standartga qaytarildi.")
    return redirect("dashboard:ui_strings")


# ==============================================================================
# 9. SERVICES
# ==============================================================================

@staff_required
def service_list(request):
    lang = get_ui_lang(request)
    dash = get_dashboard_strings(lang)
    items = Service.objects.all()
    
    localized_items = []
    for item in items:
        localized_items.append({
            "id": item.id,
            "title": localized_model_value(item, "title", lang),
            "sort_order": item.sort_order,
        })

    return render(
        request,
        "dashboard/services/list.html",
        {"items": localized_items, "section": "services", "dash": dash},
    )


@staff_required
def service_create(request):
    lang = get_ui_lang(request)
    dash = get_dashboard_strings(lang)
    if request.method == "POST":
        form = ServiceForm(request.POST)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, dash.get("msg_service_added", "Muvaffaqiyatli qo'shildi"))
            return redirect("dashboard:services")
    else:
        form = ServiceForm()
        apply_dashboard_field_styles(form)

    return render(
        request,
        "dashboard/services/form.html",
        {"form": form, "section": "services", "dash": dash, "is_new": True},
    )


@staff_required
def service_edit(request, pk):
    lang = get_ui_lang(request)
    dash = get_dashboard_strings(lang)
    obj = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        form = ServiceForm(request.POST, instance=obj)
        apply_dashboard_field_styles(form)
        if form.is_valid():
            form.save()
            messages.success(request, dash.get("msg_service_updated", "Muvaffaqiyatli yangilandi"))
            return redirect("dashboard:services")
    else:
        form = ServiceForm(instance=obj)
        apply_dashboard_field_styles(form)

    return render(
        request,
        "dashboard/services/form.html",
        {"form": form, "section": "services", "dash": dash, "is_new": False, "obj": obj},
    )


@staff_required
@require_http_methods(["POST"])
def service_delete(request, pk):
    lang = get_ui_lang(request)
    dash = get_dashboard_strings(lang)
    obj = get_object_or_404(Service, pk=pk)
    obj.delete()
    messages.success(request, dash.get("msg_service_deleted", "Muvaffaqiyatli o'chirildi"))
    return redirect("dashboard:services")
