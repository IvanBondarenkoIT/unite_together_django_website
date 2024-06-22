from django.urls import path
from django.conf.urls.static import static

from unite_together_django_website import settings
from . import views

urlpatterns = [
    path("", views.homepage, name="home"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)