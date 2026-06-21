from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Certificate, ContactLink, Education, Interest, Portfolio, ResumeProfile, Service, WorkExperience
from .translate_service import sync_translations_from_source


class ResumeProfileForm(forms.ModelForm):
    remove_photo = forms.BooleanField(required=False, label=_("Remove current photo"))

    class Meta:
        model = ResumeProfile
        fields = (
            "full_name",
            "full_name_en",
            "full_name_uz",
            "full_name_ru",
            "headline",
            "headline_en",
            "headline_uz",
            "headline_ru",
            "about",
            "about_en",
            "about_uz",
            "about_ru",
            "location",
            "location_en",
            "location_uz",
            "location_ru",
            "skills",
            "skills_en",
            "skills_uz",
            "skills_ru",
            "photo",
            "email",
            "phone",
            "telegram",
            "instagram",
            "whatsapp",
            "linkedin",
            "github",
            "kwork",
            "website",
        )
        labels = {
            "full_name": _("Full name"),
            "full_name_en": _("Full name (EN)"),
            "full_name_uz": _("Full name (UZ)"),
            "full_name_ru": _("Full name (RU)"),
            "headline": _("Headline / role"),
            "headline_en": _("Headline (English)"),
            "headline_uz": _("Headline (O'zbekcha)"),
            "headline_ru": _("Headline (Русский)"),
            "about": _("About"),
            "about_en": _("About (EN)"),
            "about_uz": _("About (UZ)"),
            "about_ru": _("About (RU)"),
            "location": _("Location"),
            "location_en": _("Location (EN)"),
            "location_uz": _("Location (UZ)"),
            "location_ru": _("Location (RU)"),
            "skills": _("Skills"),
            "skills_en": _("Skills (EN)"),
            "skills_uz": _("Skills (UZ)"),
            "skills_ru": _("Skills (RU)"),
        }
        widgets = {
            "photo": forms.FileInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["photo"].required = False
        if not (self.instance and self.instance.photo):
            del self.fields["remove_photo"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("photo") and cleaned.get("remove_photo"):
            cleaned["remove_photo"] = False
        return cleaned

    def save(self, commit=True):
        obj = super().save(commit=False)
        if self.cleaned_data.get("remove_photo") and not self.cleaned_data.get("photo"):
            obj.photo = None
        sync_translations_from_source(
            obj,
            ["full_name", "headline", "about", "location", "skills"],
        )
        if commit:
            obj.save()
        return obj


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = (
            "title", "title_en", "title_uz", "title_ru",
            "description", "description_en", "description_uz", "description_ru",
            "url", "image", "sort_order"
        )
        labels = {
            "title": _("Title (optional)"),
            "title_en": _("Title (EN)"),
            "title_uz": _("Title (UZ)"),
            "title_ru": _("Title (RU)"),
            "description": _("Description"),
            "description_en": _("Description (EN)"),
            "description_uz": _("Description (UZ)"),
            "description_ru": _("Description (RU)"),
            "url": _("Project URL"),
            "image": _("Preview image"),
        }
        widgets = {
            "image": forms.FileInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False

    def save(self, commit=True):
        obj = super().save(commit=False)
        sync_translations_from_source(obj, ["title", "description"])
        if commit:
            obj.save()
        return obj


class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = (
            "title", "title_en", "title_uz", "title_ru",
            "issuer", "issuer_en", "issuer_uz", "issuer_ru",
            "description", "description_en", "description_uz", "description_ru",
            "image", "document", "issued_on", "sort_order",
        )
        labels = {
            "title": _("Title"),
            "title_en": _("Title (EN)"),
            "title_uz": _("Title (UZ)"),
            "title_ru": _("Title (RU)"),
            "issuer": _("Issuer / organization"),
            "issuer_en": _("Issuer (EN)"),
            "issuer_uz": _("Issuer (UZ)"),
            "issuer_ru": _("Issuer (RU)"),
            "description": _("Description"),
            "description_en": _("Description (EN)"),
            "description_uz": _("Description (UZ)"),
            "description_ru": _("Description (RU)"),
        }
        widgets = {
            "image": forms.FileInput,
            "document": forms.FileInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False
        self.fields["document"].required = False

    def save(self, commit=True):
        obj = super().save(commit=False)
        sync_translations_from_source(obj, ["title", "issuer", "description"])
        if commit:
            obj.save()
        return obj


class InterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        fields = (
            "label", "label_en", "label_uz", "label_ru",
            "detail", "detail_en", "detail_uz", "detail_ru",
            "sort_order"
        )
        labels = {
            "label": _("Interest"),
            "label_en": _("Interest (EN)"),
            "label_uz": _("Interest (UZ)"),
            "label_ru": _("Interest (RU)"),
            "detail": _("Details"),
            "detail_en": _("Details (EN)"),
            "detail_uz": _("Details (UZ)"),
            "detail_ru": _("Details (RU)"),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        sync_translations_from_source(obj, ["label", "detail"])
        if commit:
            obj.save()
        return obj


class WorkExperienceForm(forms.ModelForm):
    class Meta:
        model = WorkExperience
        fields = (
            "company", "company_en", "company_uz", "company_ru",
            "role", "role_en", "role_uz", "role_ru",
            "description", "description_en", "description_uz", "description_ru",
            "start_date", "end_date", "is_current", "sort_order",
        )
        labels = {
            "company": _("Company / organization"),
            "company_en": _("Company (EN)"),
            "company_uz": _("Company (UZ)"),
            "company_ru": _("Company (RU)"),
            "role": _("Role / title"),
            "role_en": _("Role (EN)"),
            "role_uz": _("Role (UZ)"),
            "role_ru": _("Role (RU)"),
            "description": _("Description"),
            "description_en": _("Description (EN)"),
            "description_uz": _("Description (UZ)"),
            "description_ru": _("Description (RU)"),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        sync_translations_from_source(obj, ["company", "role", "description"])
        if commit:
            obj.save()
        return obj


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = (
            "institution", "institution_en", "institution_uz", "institution_ru",
            "degree", "degree_en", "degree_uz", "degree_ru",
            "description", "description_en", "description_uz", "description_ru",
            "start_date", "end_date", "sort_order",
        )
        labels = {
            "institution": _("Institution"),
            "institution_en": _("Institution (EN)"),
            "institution_uz": _("Institution (UZ)"),
            "institution_ru": _("Institution (RU)"),
            "degree": _("Degree / program"),
            "degree_en": _("Degree (EN)"),
            "degree_uz": _("Degree (UZ)"),
            "degree_ru": _("Degree (RU)"),
            "description": _("Description"),
            "description_en": _("Description (EN)"),
            "description_uz": _("Description (UZ)"),
            "description_ru": _("Description (RU)"),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        sync_translations_from_source(obj, ["institution", "degree", "description"])
        if commit:
            obj.save()
        return obj


class ContactLinkForm(forms.ModelForm):
    class Meta:
        model = ContactLink
        fields = ("name", "url", "icon", "sort_order")
        labels = {
            "name": _("Label"),
            "url": _("URL"),
            "icon": _("Icon"),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = (
            "title",
            "title_en",
            "title_uz",
            "title_ru",
            "description",
            "description_en",
            "description_uz",
            "description_ru",
            "tags",
            "image",
            "sort_order",
        )
        labels = {
            "title": _("Title"),
            "title_en": _("Title (EN)"),
            "title_uz": _("Title (UZ)"),
            "title_ru": _("Title (RU)"),
            "description": _("Description"),
            "description_en": _("Description (EN)"),
            "description_uz": _("Description (UZ)"),
            "description_ru": _("Description (RU)"),
            "tags": _("Tags"),
        }

    def save(self, commit=True):
        obj = super().save(commit=False)
        sync_translations_from_source(obj, ["title", "description"])
        if commit:
            obj.save()
        return obj
