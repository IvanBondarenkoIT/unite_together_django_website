from django.urls import path
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

from unite_together_django_website import settings
from . import views

urlpatterns = [
    # path("", RedirectView.as_view(pattern_name="home_en", permanent=True)),
    path("", views.HomeRedirectView.as_view(), name="home_redirect"),
    path("homepage/", views.homepage, name="home"),
    path("<str:lang>/homepage/", views.homepage, name="home_en"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
