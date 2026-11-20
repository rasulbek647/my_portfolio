import re

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import SiteSettings


_HEX = re.compile(r"#[0-9a-fA-F]{6}")
COLOR_FIELDS = (
    "work_bg_color", "hero_bg_color", "hero_text_color",
    "custom_bg", "custom_surface", "custom_text", "custom_heading", "custom_accent", "custom_accent_2",
)


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = (
            "theme", "work_bg_color", "work_bg_opacity", "hero_bg_color", "hero_text_color",
            "hero_use_custom", "work_use_custom", "admin_follow_theme",
            "about_anim", "about_anim_cols", "about_anim_rows", "about_anim_from", "about_anim_order",
            "about_anim_speed", "about_anim_rotate", "about_anim_flip", "about_anim_alternate", "about_anim_ease",
            "tech_anim", "tech_anim_from", "tech_anim_order", "tech_anim_speed", "tech_anim_ease",
            "tech_anim_rotate", "tech_anim_flip", "tech_anim_alternate",
            "custom_bg", "custom_surface", "custom_text", "custom_heading", "custom_accent", "custom_accent_2",
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
        for color_field in COLOR_FIELDS:
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

    def clean(self):
        data = super().clean()
        for name in COLOR_FIELDS:
            val = (data.get(name) or "").strip()
            if val and not _HEX.fullmatch(val):
                self.add_error(name, _("Rang #RRGGBB ko'rinishida bo'lishi kerak."))
            elif val:
                data[name] = val.lower()
        for name, lo, hi in (("about_anim_cols", 1, 10), ("about_anim_rows", 1, 10)):
            v = data.get(name)
            if v is not None:
                data[name] = max(lo, min(hi, int(v)))
        op = data.get("work_bg_opacity")
        if op is not None:
            data["work_bg_opacity"] = max(0, min(100, int(op)))
        return data

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
