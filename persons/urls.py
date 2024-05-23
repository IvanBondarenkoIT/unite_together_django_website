from django.urls import path
from .views import create_person, person_list

urlpatterns = [
    path('create-person/', create_person, name='create_person'),
    path('persons-list/', person_list, name='person_list'),
]
