from django.urls import path, include

from django.conf.urls.static import static

from unite_together_django_website import settings
from . import views

urlpatterns = [
    # ABOUT US
    path("about-us/who_we_are/", views.who_we_are, name="who_we_are"),
    path("<str:lang>/about-us/who_we_are/", views.who_we_are, name="who_we_are_en"),
    path("about-us/documents/", views.documents_view, name="documents"),
    path("<str:lang>/about-us/documents/", views.documents_view, name="documents_en"),
    path("about-us/partners/", views.partners, name="partners"),
    path("<str:lang>/about-us/partners/", views.partners, name="partners_en"),
    path("about-us/contact/", views.contact_view, name="contact"),
    path("<str:lang>/about-us/contact/", views.contact_view, name="contact_en"),
    path(
        "about-us/contact/success/", views.contact_success_view, name="contact_success"
    ),
    path(
        "<str:lang>/about-us//contact/success/",
        views.contact_success_view,
        name="contact_success_en",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
