from django.urls import path
from .views import create_person

urlpatterns = [
    path('create-person/', create_person, name='create_person'),
]
