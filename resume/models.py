from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Theme(models.TextChoices):
    GRAND_VINE = "grand_vine", _("Grand vine")
    WILD_CANOPY = "wild_canopy", _("Wild canopy")
    WARM_EARTH = "warm_earth", _("Warm earth")
    AVANT_HALL = "avant_hall", _("Avant hall")
    ART_STAGE = "art_stage", _("Art stage")
    BOLD_VIEW = "bold_view", _("Bold view")
    PURE_CRAFT = "pure_craft", _("Pure craft")
    DARK_LENS = "dark_lens", _("Dark lens")
    NEON_BEAT = "neon_beat", _("Neon beat")


class SiteSettings(models.Model):
    """Singleton: faqat bitta qator (sayt ko‘rinishi)."""

    theme = models.CharField(
        max_length=32,
        choices=Theme.choices,
        default=Theme.GRAND_VINE,
        verbose_name=_("Site theme"),
    )

    class Meta:
        verbose_name = _("Site settings")
        verbose_name_plural = _("Site settings")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(_("Cannot delete site settings."))

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class ResumeProfile(models.Model):
    photo = models.ImageField(upload_to="profile/", blank=True, null=True, verbose_name=_("Photo"))

    full_name = models.CharField(
        max_length=200, blank=True, default="", verbose_name=_("Full name (source / default)")
    )
    headline = models.CharField(
        max_length=300, blank=True, default="", verbose_name=_("Headline (source / default)")
    )
    about = models.TextField(blank=True, default="", verbose_name=_("About (source / default)"))
    location = models.CharField(
        max_length=200, blank=True, default="", verbose_name=_("Location (source / default)")
    )
    skills = models.TextField(blank=True, default="", verbose_name=_("Skills (source / default)"))

    full_name_en = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Full name (English)"))
    full_name_uz = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Full name (Uzbek)"))
    full_name_ru = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Full name (Russian)"))

    headline_en = models.CharField(max_length=300, blank=True, verbose_name=_("Headline (English)"))
    headline_uz = models.CharField(max_length=300, blank=True, verbose_name=_("Headline (Uzbek)"))
    headline_ru = models.CharField(max_length=300, blank=True, verbose_name=_("Headline (Russian)"))

    about_en = models.TextField(blank=True, verbose_name=_("About (English)"))
    about_uz = models.TextField(blank=True, verbose_name=_("About (Uzbek)"))
    about_ru = models.TextField(blank=True, verbose_name=_("About (Russian)"))

    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=64, blank=True, null=True, verbose_name=_("Phone"))
    location_en = models.CharField(max_length=200, blank=True, verbose_name=_("Location (English)"))
    location_uz = models.CharField(max_length=200, blank=True, verbose_name=_("Location (Uzbek)"))
    location_ru = models.CharField(max_length=200, blank=True, verbose_name=_("Location (Russian)"))

    skills_en = models.TextField(blank=True, default="", verbose_name=_("Skills (English)"))
    skills_uz = models.TextField(blank=True, default="", verbose_name=_("Skills (Uzbek)"))
    skills_ru = models.TextField(blank=True, default="", verbose_name=_("Skills (Russian)"))

    telegram = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Telegram (username or link)"))
    instagram = models.CharField(max_length=200, blank=True, null=True, verbose_name=_("Instagram (username or link)"))
    whatsapp = models.CharField(max_length=64, blank=True, null=True, verbose_name=_("WhatsApp (phone number)"))

    website = models.URLField(blank=True, null=True, verbose_name=_("Website"))
    linkedin = models.URLField(blank=True, null=True, verbose_name=_("LinkedIn"))
    github = models.URLField(blank=True, null=True, verbose_name=_("GitHub"))

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Resume profile")
        verbose_name_plural = _("Resume profile")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError(_("Cannot delete resume profile."))

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class WorkExperience(models.Model):
    company = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Company (source)"))
    role = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Role (source)"))
    description = models.TextField(blank=True, default="", verbose_name=_("Description (source)"))

    company_en = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Company (English)"))
    company_uz = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Company (Uzbek)"))
    company_ru = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Company (Russian)"))

    role_en = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Role (English)"))
    role_uz = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Role (Uzbek)"))
    role_ru = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Role (Russian)"))

    description_en = models.TextField(blank=True, verbose_name=_("Description (English)"))
    description_uz = models.TextField(blank=True, verbose_name=_("Description (Uzbek)"))
    description_ru = models.TextField(blank=True, verbose_name=_("Description (Russian)"))

    start_date = models.DateField(blank=True, null=True, verbose_name=_("Start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("End date"))
    is_current = models.BooleanField(default=False, verbose_name=_("Current role"))

    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

    class Meta:
        ordering = ["sort_order", "-start_date", "pk"]
        verbose_name = _("Work experience")
        verbose_name_plural = _("Work experience")


class Education(models.Model):
    institution = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Institution (source)"))
    degree = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Degree (source)"))
    description = models.TextField(blank=True, default="", verbose_name=_("Description (source)"))

    institution_en = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Institution (English)"))
    institution_uz = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Institution (Uzbek)"))
    institution_ru = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Institution (Russian)"))

    degree_en = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Degree (English)"))
    degree_uz = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Degree (Uzbek)"))
    degree_ru = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Degree (Russian)"))

    description_en = models.TextField(blank=True, verbose_name=_("Description (English)"))
    description_uz = models.TextField(blank=True, verbose_name=_("Description (Uzbek)"))
    description_ru = models.TextField(blank=True, verbose_name=_("Description (Russian)"))

    start_date = models.DateField(blank=True, null=True, verbose_name=_("Start date"))
    end_date = models.DateField(blank=True, null=True, verbose_name=_("End date"))

    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

    class Meta:
        ordering = ["sort_order", "-start_date", "pk"]
        verbose_name = _("Education")
        verbose_name_plural = _("Education")


class Certificate(models.Model):
    title = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Title (source)"))
    issuer = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Issuer (source)"))
    description = models.TextField(blank=True, default="", verbose_name=_("Description (source)"))

    title_en = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Title (English)"))
    title_uz = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Title (Uzbek)"))
    title_ru = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Title (Russian)"))

    issuer_en = models.CharField(max_length=200, blank=True, verbose_name=_("Issuer (English)"))
    issuer_uz = models.CharField(max_length=200, blank=True, verbose_name=_("Issuer (Uzbek)"))
    issuer_ru = models.CharField(max_length=200, blank=True, verbose_name=_("Issuer (Russian)"))

    description_en = models.TextField(blank=True, verbose_name=_("Description (English)"))
    description_uz = models.TextField(blank=True, verbose_name=_("Description (Uzbek)"))
    description_ru = models.TextField(blank=True, verbose_name=_("Description (Russian)"))

    image = models.ImageField(upload_to="certificates/", blank=True, null=True, verbose_name=_("Image"))
    document = models.FileField(upload_to="certificates/docs/", blank=True, null=True, verbose_name=_("Document (PDF)"))
    issued_on = models.DateField(blank=True, null=True, verbose_name=_("Issued on"))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = _("Certificate")
        verbose_name_plural = _("Certificates")


class Interest(models.Model):
    label = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Interest (source)"))
    detail = models.TextField(blank=True, default="", verbose_name=_("Detail (source)"))

    label_en = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Interest (English)"))
    label_uz = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Interest (Uzbek)"))
    label_ru = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Interest (Russian)"))

    detail_en = models.TextField(blank=True, verbose_name=_("Detail (English)"))
    detail_uz = models.TextField(blank=True, verbose_name=_("Detail (Uzbek)"))
    detail_ru = models.TextField(blank=True, verbose_name=_("Detail (Russian)"))

    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = _("Interest")
        verbose_name_plural = _("Interests")


class Portfolio(models.Model):
    title = models.CharField(max_length=300, blank=True, default="", verbose_name=_("Title (optional)"))
    url = models.URLField(verbose_name=_("Project URL"))
    image = models.ImageField(upload_to="portfolio/", blank=True, null=True, verbose_name=_("Preview image"))
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = _("Portfolio item")
        verbose_name_plural = _("Portfolio")


class ContactLinkIcon(models.TextChoices):
    LINK = "link", _("Link (default)")
    GLOBE = "globe", _("Globe / website")
    CHAT = "chat", _("Chat / messenger")
    USERS = "users", _("Community / team")
    VIDEO = "video", _("Video / stream")
    CODE = "code", _("Code / dev")
    DEVICE = "device", _("Mobile app")
    MUSICAL = "musical", _("Music / audio")
    SPARKLES = "sparkles", _("Other highlights")
    HASHTAG = "hashtag", _("Social / topics")


class ContactLink(models.Model):
    """Profildan keyin Contact bo‘limida ko‘rinadigan qo‘shimcha havolalar (Discord, custom sayt, …)."""

    name = models.CharField(max_length=120, blank=True, null=True, verbose_name=_("Label (e.g. Discord)"))
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name=_("URL"))
    icon = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        choices=ContactLinkIcon.choices,
        verbose_name=_("Icon (optional)"),
    )
    sort_order = models.PositiveIntegerField(default=0, verbose_name=_("Sort order"))

    class Meta:
        ordering = ["sort_order", "pk"]
        verbose_name = _("Extra contact link")
        verbose_name_plural = _("Extra contact links")
