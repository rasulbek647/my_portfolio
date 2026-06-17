from django.urls import path

from . import dashboard_views as v

app_name = "dashboard"

urlpatterns = [
    path("login/", v.DashboardLoginView.as_view(), name="login"),
    path("ui-lang/", v.set_dashboard_ui_lang, name="set_ui_lang"),
    path("logout/", v.DashboardLogoutView.as_view(), name="logout"),
    path("", v.dashboard_index, name="index"),
    path("profile/", v.dashboard_profile, name="profile"),
    path("experience/", v.experience_list, name="experience"),
    path("experience/new/", v.experience_create, name="experience_create"),
    path("experience/<int:pk>/edit/", v.experience_edit, name="experience_edit"),
    path("experience/<int:pk>/delete/", v.experience_delete, name="experience_delete"),
    path("education/", v.education_list, name="education"),
    path("education/new/", v.education_create, name="education_create"),
    path("education/<int:pk>/edit/", v.education_edit, name="education_edit"),
    path("education/<int:pk>/delete/", v.education_delete, name="education_delete"),
    path("certificates/", v.certificate_list, name="certificates"),
    path("certificates/new/", v.certificate_create, name="certificate_create"),
    path("certificates/<int:pk>/edit/", v.certificate_edit, name="certificate_edit"),
    path("certificates/<int:pk>/delete/", v.certificate_delete, name="certificate_delete"),
    path("portfolio/", v.portfolio_list, name="portfolio"),
    path("portfolio/new/", v.portfolio_create, name="portfolio_create"),
    path("portfolio/<int:pk>/edit/", v.portfolio_edit, name="portfolio_edit"),
    path("portfolio/<int:pk>/delete/", v.portfolio_delete, name="portfolio_delete"),
    path("contact-links/", v.contact_link_list, name="contact_links"),
    path("contact-links/new/", v.contact_link_create, name="contact_link_create"),
    path("contact-links/<int:pk>/edit/", v.contact_link_edit, name="contact_link_edit"),
    path("contact-links/<int:pk>/delete/", v.contact_link_delete, name="contact_link_delete"),
    path("interests/", v.interest_list, name="interests"),
    path("interests/new/", v.interest_create, name="interest_create"),
    path("interests/<int:pk>/edit/", v.interest_edit, name="interest_edit"),
    path("interests/<int:pk>/delete/", v.interest_delete, name="interest_delete"),
    path("settings/", v.dashboard_settings, name="settings"),
    path("samples/list/", v.sample_list_page, name="samples_list"),
    path("samples/form/", v.sample_form_page, name="samples_form"),
]
