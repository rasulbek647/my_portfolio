from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from django.views.static import serve

"""
Boshqaruv: faqat yangi panel — /admin/ ostida (dashboard URLconf).
Eski django.contrib.admin olib tashlangan.
/dashboard/ → /admin/ ga yo‘naltiriladi.
"""

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("admin/", include("resume.dashboard_urls", namespace="dashboard")),
    path(
        "dashboard/",
        RedirectView.as_view(pattern_name="dashboard:index", permanent=False),
    ),
    path("", include("resume.urls")),
]

# DEBUG=False bo‘lsa ham Render’da yuklangan rasmlar ishlashi kerak.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif getattr(settings, "SERVE_MEDIA", False):
    urlpatterns += [
        re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
