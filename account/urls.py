from django.urls import path
from .views import (
    ConfirmView,
    HomeView,
    LoginView,
    LogoutView,
    RecoveryPasswordConfirmView,
    RecoveryPasswordView,
    RegisterView,
    ExtractView,
    CompletedTransactionsView
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("confirm/<int:account_id>/", ConfirmView.as_view(), name="confirm"),
    path("login/", LoginView.as_view(), name="login"),
    path("home/", HomeView.as_view(), name="home"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "password/recovery/", RecoveryPasswordView.as_view(), name="password-recovery"
    ),
    path(
        "password/confirm/",
        RecoveryPasswordConfirmView.as_view(),
        name="password-confirm",
    ),
    path("extract/", ExtractView.as_view(), name="extract"),
    path("completed-transactions/", CompletedTransactionsView.as_view(), name="completed-transactions"),

    path("", HomeView.as_view()),
]
