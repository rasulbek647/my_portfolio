"""Dashboard formalariga Tailwind sinflarini qo‘llash (qo'shimcha paketlarsiz)."""

from django import forms

# 8px grid asosida
TW_LABEL = "block text-sm font-medium text-slate-300 mb-2"
TW_HELP = "mt-1.5 text-xs text-slate-500"
TW_ERROR = "mt-1.5 text-sm text-red-400"

TW_CONTROL = (
    "mt-0 block w-full rounded-xl border border-slate-600/70 bg-slate-900/50 px-4 py-3 "
    "text-[15px] leading-snug text-slate-100 placeholder:text-slate-500 shadow-sm "
    "transition duration-150 ease-out "
    "focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/35 "
    "disabled:cursor-not-allowed disabled:opacity-50"
)

TW_CONTROL_ERROR = " border-red-400/70 focus:border-red-400 focus:ring-red-400/30"

TW_TEXTAREA = TW_CONTROL + " min-h-[140px] resize-y"

TW_FILE = (
    "mt-0 block w-full cursor-pointer rounded-xl border border-dashed border-slate-600/80 "
    "bg-slate-900/40 px-4 py-3 text-sm text-slate-300 file:mr-4 file:cursor-pointer "
    "file:rounded-lg file:border-0 file:bg-slate-800 file:px-4 file:py-2 file:text-sm "
    "file:font-medium file:text-primary-light hover:file:bg-slate-700"
)

TW_SELECT = TW_CONTROL + " pr-10"


def apply_dashboard_field_styles(form: forms.BaseForm) -> None:
    """Formadagi barcha maydonlarga dashboard uslubi."""
    for name, field in form.fields.items():
        w = field.widget
        if isinstance(w, forms.Textarea):
            cls = TW_TEXTAREA
        elif isinstance(w, (forms.ClearableFileInput, forms.FileInput)):
            cls = TW_FILE
        elif isinstance(w, forms.Select):
            cls = TW_SELECT
        elif isinstance(w, forms.CheckboxInput):
            w.attrs.setdefault(
                "class",
                "h-4 w-4 rounded border-slate-600 bg-slate-900 text-primary focus:ring-primary/40",
            )
            continue
        else:
            cls = TW_CONTROL

        err = bool(form.errors.get(name))
        if err:
            cls += TW_CONTROL_ERROR

        existing = w.attrs.get("class", "")
        w.attrs["class"] = f"{existing} {cls}".strip()


def field_placeholder(form: forms.BaseForm, mapping: dict[str, str]) -> None:
    for name, ph in mapping.items():
        if name in form.fields:
            form.fields[name].widget.attrs.setdefault("placeholder", ph)
