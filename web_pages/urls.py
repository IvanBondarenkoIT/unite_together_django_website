from django.urls import path, include

from django.conf.urls.static import static

from unite_together_django_website import settings
from web_pages import views

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.projects, name="projects"),
    path("events/", views.events, name="events"),
    path('events/<slug:group_slug>/', views.events, name='events_by_group'),
    path("about-us/", views.about_us, name="about-us"),



    path("", include("paypal.standard.ipn.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)