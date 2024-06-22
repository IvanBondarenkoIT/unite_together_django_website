"""
URL configuration for unite_together_django_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from unite_together_django_website import views
from unite_together_django_website import settings

urlpatterns = [

    # ADMIN
    path("secure/", admin.site.urls),
    # Home
    path("", include("homepage.urls")),
    # ABOUT US
    path("about-us/", include("about_us.urls")),
    # ACCOUNTS
    path("accounts/", include("accounts.urls")),
    # PERSONS
    path("persons/", include("persons.urls")),
    # COORDINATION
    path("coordination/", include("coordination.urls")),

    path("", include("web_pages.urls")),
    path("", include("donate.urls")),
    path("", include("paypal.standard.ipn.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
