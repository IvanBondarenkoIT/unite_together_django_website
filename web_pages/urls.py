from django.urls import path, include

from django.conf.urls.static import static

from unite_together_django_website import settings
from web_pages import views

urlpatterns = [
    path("", views.home, name="home"),
    # EVENTS
    path("events/", views.events, name="events"),
    path('events/<slug:group_slug>/', views.events, name='events_by_group'),
    path('events/<slug:group_slug>/<slug:event_slug>', views.event_detail, name='event_detail'),
    # PROJECTS
    path("projects/", views.projects, name="projects"),
    path('projects/<slug:group_slug>/', views.projects, name='projects_by_group'),
    path('projects/<slug:group_slug>/<slug:project_slug>', views.projects_detail, name='projects_detail'),
    # ABOUT US
    path("about-us/history", views.history, name="history"),
    path("about-us/documents", views.documents, name="documents"),
    path("about-us/partners", views.partners, name="partners"),
    path("about-us/contacts", views.contacts, name="contacts"),

    path("", include("paypal.standard.ipn.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)