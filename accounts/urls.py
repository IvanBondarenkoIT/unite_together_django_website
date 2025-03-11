from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("<str:lang>/register/", views.register, name="register_en"),
    path("<str:lang>/login/", views.login, name="login_en"),
    path("<str:lang>/logout/", views.logout, name="logout_en"),
    path("<str:lang>/activate/<uidb64>/<token>/", views.activate, name="activate_en"),
    # path('dashboard/', views.dashboard, name='dashboard'),
    # path('', views.dashboard, name='dashboard'),
    path("forgotPassword/", views.forgot_password, name="forgot_password"),
    path(
        "reset_password_validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate",
    ),
    path("reset_password/", views.reset_password, name="reset_password"),
    path(
        "<str:lang>/forgotPassword/", views.forgot_password, name="forgot_password_en"
    ),
    path(
        "<str:lang>/reset_password_validate/<uidb64>/<token>/",
        views.reset_password_validate,
        name="reset_password_validate_en",
    ),
    path("<str:lang>/reset_password/", views.reset_password, name="reset_password_en"),
]
