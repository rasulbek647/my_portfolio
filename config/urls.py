from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import RedirectView

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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
