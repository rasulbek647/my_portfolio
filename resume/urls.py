from django.urls import path

from . import views

app_name = "resume"

urlpatterns = [
    path("", views.cv_home, name="home"),
    path("cv.pdf", views.cv_pdf, name="cv_pdf"),
]
