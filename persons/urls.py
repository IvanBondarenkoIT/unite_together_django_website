from django.urls import path
from . import views


urlpatterns = [
    path("persons/", views.associated_person_list, name="dashboard"),
    path("<str:lang>/persons/", views.associated_person_list, name="dashboard_en"),
    path(
        "persons/associated-persons/",
        views.associated_person_list,
        name="associated_person_list",
    ),
    path(
        "persons/associated-persons/create/",
        views.associated_person_create,
        name="associated_person_create",
    ),
    path(
        "persons/associated-persons/<int:pk>/edit/",
        views.associated_person_edit,
        name="associated_person_edit",
    ),
    path(
        "<str:lang>/persons/associated-persons/",
        views.associated_person_list,
        name="associated_person_list_en",
    ),
    path(
        "<str:lang>/persons/associated-persons/create/",
        views.associated_person_create,
        name="associated_person_create_en",
    ),
    path(
        "<str:lang>/persons/associated-persons/<int:pk>/edit/",
        views.associated_person_edit,
        name="associated_person_edit_en",
    ),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('create-person/', views.create_person, name='create_person'),
    # path('persons-list/', views.person_list, name='person_list'),
    # path('create-participant/', views.create_participant, name='create_participant'),
    # path('participants-list/', views.participant_list, name='participant_list'),
    path(
        "persons/registered-events/", views.registered_events, name="registered_events"
    ),
    path("persons/settings/", views.settings, name="settings"),
    path(
        "<str:lang>/persons/registered-events/",
        views.registered_events,
        name="registered_events_en",
    ),
    path("<str:lang>/persons/settings/", views.settings, name="settings_en"),
]
