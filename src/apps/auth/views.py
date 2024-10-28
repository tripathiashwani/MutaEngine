from django.utils import timezone
from drf_spectacular.utils import extend_schema
from rest_framework import exceptions, generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from src.apps.auth.models import User
from src.apps.auth.serializers import (
    ChangePasswordSerializer,
    CreateUserSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PasswordResetVerifySerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserSerializer,
    UserUpdateSerializer,
)
from src.apps.common.types import Request

from .two_fa_handlers import OTPACTION, TwoFAHandler


class CreateUserView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CreateUserSerializer

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "msg": "User registration successful",
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"msg": "User registration successful"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class UserLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "refresh": "refresh_token",
                    "access": "access_token",
                    "msg": "User logged in successfully",
                    "two_fa": False,
                    "user_id": "uuid",
                    "is_tenant_master": "bool",
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user", None)

        user.is_active = True
        user.last_login = timezone.now()
        user.save()
        refresh_token = TokenObtainPairSerializer.get_token(user)

        access_token = refresh_token.access_token  # type:ignore

        return Response(
            {
                "msg": "User logged in successfully",
                "refresh": str(refresh_token),
                "access": str(access_token),
                "user_id": user.id
            },
            status=status.HTTP_200_OK,
        )


class UserLogoutView(generics.GenericAPIView):
    serializer_class = UserLogoutSerializer

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "msg": "logged out successfully",
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exceptions=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        refresh_token = serializer.validated_data.get("refresh")
        if refresh_token is None:
            raise exceptions.APIException(
                {"error": "Refresh token is required"}, code=status.HTTP_400_BAD_REQUEST
            )

        token = RefreshToken(refresh_token)
        try:
            token.blacklist()
            user = request.user
            user.save()
            return Response({"msg": "logged out successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            raise exceptions.APIException({"error": str(e)}, code=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(generics.UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs.get("pk")
        if pk == user.pk:
            return User.objects.filter(pk=pk)

        raise exceptions.PermissionDenied("You cannot update this user")


class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.none()  # to prevent swagger error messages

    def get_queryset(self):
        user = self.request.user
        pk = self.kwargs['pk']
        if pk is None:
            raise exceptions.ValidationError("User id is required")
        return User.objects.filter(pk=pk)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.none()
    request: Request

    def get_queryset(self):
        users = User.objects.all()
        return users


class PaswordResetRequestView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = PasswordResetRequestSerializer

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "msg": "string",
                }
            }
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user", None)

        if user is not None:
            two_fa_handler = TwoFAHandler(user=user, action=OTPACTION.RESET)
            message = two_fa_handler.send_otp()

            return Response({"msg": message, "user_email": user.email}, status=status.HTTP_200_OK)

        return Response({"msg": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerifyView(generics.GenericAPIView):
    serializer_class = PasswordResetVerifySerializer
    permission_classes = [permissions.AllowAny]
    request: Request

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "msg": "OTP Verified",
                    "id": "uuid"
                }
            }
        }
    )
    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get("user")

        return Response(
            {
                "msg": "OTP Verified",
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [permissions.AllowAny]
    request: Request

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "msg": "Password changed successfully",
                }
            }
        }
    )
    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data["user"]
        password = serializer.validated_data["password"]
        user.set_password(password)
        user.save()

        return Response({"msg": "Password changed successfully"}, status=status.HTTP_200_OK)


class PasswordChangeView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    request: Request

    @extend_schema(
        responses={
            "application/json": {
                "example": {
                    "msg": "Password changed successfully",
                }
            }
        }
    )
    def post(self, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data["user"]
        password = serializer.validated_data["new_password"]
        user.set_password(password)

        user.save()

        return Response({"msg": "Password changed successfully"}, status=status.HTTP_200_OK)
