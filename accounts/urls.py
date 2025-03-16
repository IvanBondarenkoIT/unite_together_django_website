from django.urls import path

from . import views

urlpatterns = [
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", views.login, name="login"),
    path("accounts/logout/", views.logout, name="logout"),
    path("accounts/activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("<str:lang>/accounts/register/", views.register, name="register_en"),
    path("<str:lang>/accounts/login/", views.login, name="login_en"),
    path("<str:lang>/accounts/logout/", views.logout, name="logout_en"),
    path(
        "<str:lang>/accounts/activate/<uidb64>/<token>/",
        views.activate,
        name="activate_en",
    ),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('', views.dashboard, name='dashboard'),
    path("accounts/forgotPassword/", views.forgot_password, name="forgot_password"),
    path(
        "accounts/reset_password_validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate",
    ),
    path("accounts/reset_password/", views.reset_password, name="reset_password"),
    path(
        "<str:lang>/accounts/forgotPassword/",
        views.forgot_password,
        name="forgot_password_en",
    ),
    path(
        "<str:lang>/accounts/reset_password_validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate_en",
    ),
    path(
        "<str:lang>/accounts/reset_password/",
        views.reset_password,
        name="reset_password_en",
    ),
]
