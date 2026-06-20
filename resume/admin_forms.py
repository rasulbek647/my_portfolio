from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Certificate, ContactLink, Education, Interest, Portfolio, ResumeProfile, WorkExperience
from .translate_service import sync_translations_from_source


class ResumeProfileForm(forms.ModelForm):
    remove_photo = forms.BooleanField(required=False, label=_("Remove current photo"))

    class Meta:
        model = ResumeProfile
        fields = (
            "full_name",
            "headline",
            "headline_en",
            "headline_uz",
            "headline_ru",
            "about",
            "location",
            "skills",
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
            "headline": _("Headline / role"),
            "headline_en": _("Headline (English)"),
            "headline_uz": _("Headline (O'zbekcha)"),
            "headline_ru": _("Headline (Русский)"),
            "about": _("About"),
            "location": _("Location"),
            "skills": _("Skills"),
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
        fields = ("title", "description", "url", "image", "sort_order")
        labels = {
            "title": _("Title (optional)"),
            "description": _("Description"),
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
            "title",
            "issuer",
            "description",
            "image",
            "document",
            "issued_on",
            "sort_order",
        )
        labels = {
            "title": _("Title"),
            "issuer": _("Issuer / organization"),
            "description": _("Description"),
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
        fields = ("label", "detail", "sort_order")
        labels = {
            "label": _("Interest"),
            "detail": _("Details"),
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
            "company",
            "role",
            "description",
            "start_date",
            "end_date",
            "is_current",
            "sort_order",
        )
        labels = {
            "company": _("Company / organization"),
            "role": _("Role / title"),
            "description": _("Description"),
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
            "institution",
            "degree",
            "description",
            "start_date",
            "end_date",
            "sort_order",
        )
        labels = {
            "institution": _("Institution"),
            "degree": _("Degree / program"),
            "description": _("Description"),
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
