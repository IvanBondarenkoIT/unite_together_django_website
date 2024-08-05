from django.urls import path
from . import views
from .views import create_person, person_list

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('associated_persons/', views.associated_person_list, name='associated_person_list'),
    path('associated_persons/create/', views.associated_person_create, name='associated_person_create'),
    path('associated_persons/<int:pk>/edit/', views.associated_person_edit, name='associated_person_edit'),


    path('dashboard/', views.dashboard, name='dashboard'),
    path('create-person/', views.create_person, name='create_person'),
    path('persons-list/', views.person_list, name='person_list'),

    # path('create-participant/', views.create_participant, name='create_participant'),
    # path('participants-list/', views.participant_list, name='participant_list'),
    path('registered-events/', views.registered_events, name='registered_events'),

    path('settings/', views.settings, name='settings'),

]
