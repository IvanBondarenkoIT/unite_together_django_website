from django.urls import path, include

from django.conf.urls.static import static
from web_pages import views

urlpatterns = [

    path("AboutUs/", views.about_us, name="about_us"),

]