from django.urls import path, include

from django.conf.urls.static import static

from unite_together_django_website import settings
from web_pages import views

urlpatterns = [

    path("aboutus/", views.about_us, name="about_us"),
    path("", views.home, name="home"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)