from django.urls import path, include

from django.conf.urls.static import static

from unite_together_django_website import settings
from . import views

urlpatterns = [

    # ABOUT US
    path("", views.who_we_are, name="who_we_are"),
    # path("about-us/history", views.history, name="history"),
    # path("about-us/documents", views.documents, name="documents"),
    # path("about-us/partners", views.partners, name="partners"),
    # path("about-us/contacts", views.contacts, name="contacts"),


    path("", include("paypal.standard.ipn.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)