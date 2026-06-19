from django import forms
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = ("theme",)
        labels = {"theme": _("Sayt mavzusi")}

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop("lang", "uz")
        super().__init__(*args, **kwargs)
        self.fields["theme"].widget.attrs.setdefault(
            "class",
            "mt-0 block w-full rounded-xl border border-slate-600/70 bg-themeSurface px-4 py-3 "
            "text-[15px] text-slate-100 focus:border-primary focus:outline-none focus:ring-2 "
            "focus:ring-primary/35",
        )
        
        from .dashboard_i18n import get_dashboard_strings
        dash_strings = get_dashboard_strings(lang)
        new_choices = []
        for k, original_label in self.fields["theme"].choices:
            theme_key = f"theme_name_{k}"
            label = dash_strings.get(theme_key, original_label)
            new_choices.append((k, label))
        self.fields["theme"].choices = new_choices
