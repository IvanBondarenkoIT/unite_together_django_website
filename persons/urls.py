from django.urls import path
from .views import create_person, person_list, create_participant, participant_list

urlpatterns = [
    path('create-person/', create_person, name='create_person'),
    path('persons-list/', person_list, name='person_list'),

    path('create-participant/', create_participant, name='create_participant'),
    path('participants-list/', participant_list, name='participant_list'),
]
