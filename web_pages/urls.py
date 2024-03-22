from django.urls import path, include

from django.conf.urls.static import static

from unite_together_django_website import settings
from web_pages import views

urlpatterns = [

    path("AboutUs/", views.about_us, name="about_us"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)