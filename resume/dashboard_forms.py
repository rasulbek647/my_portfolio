from django import forms
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "theme", "work_bg_color", "work_bg_opacity", "hero_bg_color", "hero_text_color",
            "hero_greeting", "hero_greeting_en", "hero_greeting_uz", "hero_greeting_ru",
            "hero_stat1_value", "hero_stat1_value_en", "hero_stat1_value_uz", "hero_stat1_value_ru",
            "hero_stat1_label", "hero_stat1_label_en", "hero_stat1_label_uz", "hero_stat1_label_ru",
            "hero_stat2_value", "hero_stat2_value_en", "hero_stat2_value_uz", "hero_stat2_value_ru",
            "hero_stat2_label", "hero_stat2_label_en", "hero_stat2_label_uz", "hero_stat2_label_ru"
        )
        labels = {
            "theme": _("Sayt mavzusi"),
            "work_bg_color": _("WORK yozuvi rangi"),
            "work_bg_opacity": _("WORK yozuvi shaffofligi (%)"),
            "hero_bg_color": _("Hero fon rangi"),
            "hero_text_color": _("Hero matn rangi"),
            "hero_greeting": _("Salomlashish matni"),
            "hero_stat1_value": _("1-statistika qiymati"),
            "hero_stat1_label": _("1-statistika nomi"),
            "hero_stat2_value": _("2-statistika qiymati"),
            "hero_stat2_label": _("2-statistika nomi"),
        }

    def __init__(self, *args, **kwargs):
        lang = kwargs.pop("lang", "uz")
        super().__init__(*args, **kwargs)
        self.fields["theme"].widget.attrs.setdefault(
            "class",
            "mt-0 block w-full rounded-xl border border-slate-600/70 bg-slate-900/50 px-4 py-3 "
            "text-[15px] text-slate-100 focus:border-primary focus:outline-none focus:ring-2 "
            "focus:ring-primary/35",
        )
        # Color picker widgets
        for color_field in ("work_bg_color", "hero_bg_color", "hero_text_color"):
            self.fields[color_field].widget.attrs.setdefault(
                "class",
                "mt-0 block w-full rounded-xl border border-slate-600/70 bg-slate-900/50 px-1 py-1 "
                "h-[50px] text-[15px] text-slate-100 focus:border-primary focus:outline-none focus:ring-2 "
                "focus:ring-primary/35 cursor-pointer",
            )
            self.fields[color_field].widget.input_type = 'color'

        self.fields["work_bg_opacity"].widget.attrs.setdefault(
            "class",
            "mt-0 block w-full accent-primary",
        )
        self.fields["work_bg_opacity"].widget.input_type = 'range'
        self.fields["work_bg_opacity"].widget.attrs.update({"min": 0, "max": 100})
        
        for text_field in (
            "hero_greeting", "hero_greeting_en", "hero_greeting_uz", "hero_greeting_ru",
            "hero_stat1_value", "hero_stat1_value_en", "hero_stat1_value_uz", "hero_stat1_value_ru",
            "hero_stat1_label", "hero_stat1_label_en", "hero_stat1_label_uz", "hero_stat1_label_ru",
            "hero_stat2_value", "hero_stat2_value_en", "hero_stat2_value_uz", "hero_stat2_value_ru",
            "hero_stat2_label", "hero_stat2_label_en", "hero_stat2_label_uz", "hero_stat2_label_ru"
        ):
            self.fields[text_field].widget.attrs.setdefault(
                "class",
                "mt-0 block w-full rounded-xl border border-slate-600/70 bg-slate-900/50 px-4 py-3 "
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

    def save(self, commit=True):
        from .translate_service import sync_translations_from_source
        obj = super().save(commit=False)
        sync_translations_from_source(
            obj,
            ["hero_greeting", "hero_stat1_value", "hero_stat1_label", "hero_stat2_value", "hero_stat2_label"]
        )
        if commit:
            obj.save()
        return obj
