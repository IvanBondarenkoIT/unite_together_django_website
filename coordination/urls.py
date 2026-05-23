from django.urls import path
from .views import (
    event_list,
    event_create,
    event_update,
    event_delete,
    participant_list,
    participant_create,
    participant_update,
    participant_delete,
    person_list,
    person_create,
    person_update,
    person_delete,
    export_participants,
)

urlpatterns = [
    path("events-list/", event_list, name="event_list"),
    path("events/create/", event_create, name="event_create"),
    path("events/<int:pk>/update/", event_update, name="event_update"),
    # path('events/<int:pk>/delete/', event_delete, name='event_delete'),
    path("participants/<int:pk>", participant_list, name="participant_list"),
    path("participants/create/", participant_create, name="participant_create"),
    path(
        "participants/<int:pk>/update/", participant_update, name="participant_update"
    ),
    # path('participants/<int:event_pk>/<int:pk>/delete/', participant_delete, name='participant_delete'),
    path(
        "export-participants/<int:pk>", export_participants, name="export_participants"
    ),
    path("persons-list/", person_list, name="coordination_person_list"),
    path("persons/create/", person_create, name="person_create"),
    path("persons/<int:pk>/update/", person_update, name="person_update"),
    # path('persons/<int:pk>/delete/', person_delete, name='person_delete'),
]
