from django.urls import path
from . import views
from .views import create_person, person_list, create_participant, participant_list

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-person/', views.create_person, name='create_person'),
    path('persons-list/', views.person_list, name='person_list'),

    path('create-participant/', views.create_participant, name='create_participant'),
    path('participants-list/', views.participant_list, name='participant_list'),
    path('registered-events/', views.registered_events, name='registered_events'),

    path('settings/', views.settings, name='settings'),
]
