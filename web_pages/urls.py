from django.urls import path, include

from django.conf.urls.static import static


urlpatterns = [

    path("", views.about_us, name="about_us"),

]