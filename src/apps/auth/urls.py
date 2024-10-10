from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from src.apps.auth.views import (
    CreateUserView,
    PasswordChangeView,
    PasswordResetConfirmView,
    PasswordResetVerifyView,
    PaswordResetRequestView,
    RetrieveUserView,
    UserListView,
    UserLoginView,
    UserLogoutView,
    UserUpdateView,
)


urlpatterns = [
    path("user/register/", CreateUserView.as_view(), name="user-creatation-api-endpoint"),
    path("user/login/", UserLoginView.as_view(), name="user-login-api-endpoint"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh-api-endpoint"),
    path("user/logout/", UserLogoutView.as_view(), name="user-logout-api-endpoint"),
    path("user/<uuid:pk>/update/", UserUpdateView.as_view(), name="user-update-api-endpoint"),
    path("user/list/", UserListView.as_view(), name="user-list-api-endpoint"),
    path("user/<uuid:pk>/", RetrieveUserView.as_view(), name="retrieve-user-api-endpoint"),
    path(
        "user/password/reset/request/",
        PaswordResetRequestView.as_view(),
        name="reset-user-password-api-endpoint",
    ),
    path(
        "user/password/reset/verify/",
        PasswordResetVerifyView.as_view(),
        name="verify-reset-password-otp-api-endpoint",
    ),
    path(
        "user/password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="confirm-reset-password-api-endpoint",
    ),
    path(
        "user/password/change/",
        PasswordChangeView.as_view(),
        name="change-user-password-api-endpoint",
    ),
]
