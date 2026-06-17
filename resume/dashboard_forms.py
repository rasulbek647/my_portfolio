from django import forms
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ("theme",)
        labels = {"theme": _("Sayt mavzusi")}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["theme"].widget.attrs.setdefault(
            "class",
            "mt-0 block w-full rounded-xl border border-slate-600/70 bg-slate-900/50 px-4 py-3 "
            "text-[15px] text-slate-100 focus:border-primary focus:outline-none focus:ring-2 "
            "focus:ring-primary/35",
        )
