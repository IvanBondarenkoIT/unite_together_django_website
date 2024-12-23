from django.urls import path, include

from django.conf.urls.static import static

from unite_together_django_website import settings
from web_pages import views
from web_pages.views import test_email_view

urlpatterns = [
    # path("", views.home, name="home"),
    # EVENTS
    path("events/", views.events, name="events"),
    path("events/<slug:group_slug>/", views.events, name="events_by_group"),
    path(
        "events/<slug:group_slug>/<slug:event_slug>",
        views.event_detail,
        name="event_detail",
    ),
    # PROJECTS
    path("projects/", views.projects, name="projects"),
    path("projects/<slug:group_slug>/", views.projects, name="projects_by_group"),
    path(
        "projects/<slug:group_slug>/<slug:project_slug>",
        views.projects_detail,
        name="projects_detail",
    ),
    path("", include("paypal.standard.ipn.urls")),
    path("test-email/", test_email_view, name="test_email"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
