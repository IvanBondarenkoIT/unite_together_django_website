from django.urls import path, include, re_path
from django.conf.urls.static import static
from unite_together_django_website import settings
from web_pages import views
from web_pages.views import test_email_view

urlpatterns = [
    # Украинская версия (по умолчанию)
    path("events/", views.events, name="events"),
    path(
        "events/<slug:group_slug>/",
        views.events,
        name="events_by_group",
    ),
    path(
        "events/<slug:group_slug>/<slug:event_slug>",
        views.event_detail,
        name="event_detail",
    ),
    path("projects/", views.projects, {"lang": "uk"}, name="projects"),
    path(
        "projects/<slug:group_slug>/",
        views.projects,
        name="projects_by_group",
    ),
    path(
        "projects/<slug:group_slug>/<slug:project_slug>",
        views.projects_detail,
        name="projects_detail",
    ),
    path("test-email/", test_email_view, name="test_email"),
    # Английская версия
    path("<str:lang>/events/", views.events, name="events_en"),
    path(
        "<str:lang>/events/<slug:group_slug>",
        views.events,
        name="events_by_group_en",
    ),
    path(
        "<str:lang>/events/<slug:group_slug>/<slug:event_slug>",
        views.event_detail,
        name="event_detail_en",
    ),
    path("<str:lang>/projects/", views.projects, name="projects_en"),
    path(
        "<str:lang>/projects/<slug:group_slug>",
        views.projects,
        name="projects_by_group_en",
    ),
    path(
        "<str:lang>/projects/<slug:group_slug>/<slug:project_slug>/",
        views.projects_detail,
        name="projects_detail_en",
    ),
    # PayPal URLs
    path("", include("paypal.standard.ipn.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
