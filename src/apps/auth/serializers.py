from django.core.cache import cache
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import Group

from .two_fa_handlers import TwoFAHandler, OTPACTION
from .models import User


class CreateUserSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "password","role_id")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data, is_active=False)
            role_id = validated_data.get("role_id")
            if role_id:
                group = Group.objects.get(id=role_id)
                user.groups.add(group)

            return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=255, write_only=True, required=True, allow_blank=False
    )
    
    def validate(self, attrs: dict):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        if email is None or password is None:
            raise serializers.ValidationError({"msg": "email or password missing"})

        try:
            user: User = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"msg": "Invalid email or password"})

        if user.check_password(password):
            attrs["user"] = user
        else:
            attrs["user"] = None
            raise serializers.ValidationError({"msg": "Invalid email or password"})

        return attrs


class UserLogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField(
        max_length=255 * 3, required=True, allow_blank=False
    )


class UserUpdateSerializer(serializers.ModelSerializer):
    role_id = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = "__all__"

    def update(self, instance, validated_data):
        role_id = validated_data.pop("role_id")
        for attr, value in validated_data.items():
            setattr(instance, attr, value)


        try:
            role = Group.objects.get(id=role_id)
            instance.groups.clear()
            instance.groups.add(role)

        except Group.DoesNotExist:
            raise serializers.ValidationError({"msg": "Invalid role id"})

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "otp",  
            "otp_created_at",
            "otp_tries",
            "password",
            "groups",
            "user_permissions",
            "is_superuser",
            "is_staff",
        )


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, required=True, allow_blank=False)

    def validate(self, attrs):
        email = attrs.get("email", None)

        if email is None:
            raise serializers.ValidationError({"msg": "Email is missing"})

        try:
            user: User = User.objects.get(email=email)
            attrs["user"] = user
        except User.DoesNotExist:
            attrs["user"] = None
            raise serializers.ValidationError(
                {"msg": "User with this email does not exist"}
            )

        return attrs


class PasswordResetVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(required=True, allow_blank=False)
    email = serializers.EmailField(required=True, allow_blank=False)

    def validate(self, attrs: dict) -> dict:
        otp = attrs.get("otp", None)

        try:
            user: User = User.objects.get(email=attrs.get("email", None))
            attrs["user"] = user
        except User.DoesNotExist:
            attrs["user"] = None
            raise serializers.ValidationError("User not found")

        handler = TwoFAHandler(user=user, action=OTPACTION.RESET)
        verified, message = handler.verify_otp(otp)
        if not verified:
            raise serializers.ValidationError(message)

        cache.set(f"{user.id}_otp", otp, timeout=180)
        return super().validate(attrs)


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(required=True, allow_blank=False)
    id = serializers.CharField(required=True, allow_blank=False)

    def validate(self, attrs: dict) -> dict:
        id = attrs.get("id", None)

        try:
            user: User = User.objects.get(id=id)
            attrs["user"] = user
        except User.DoesNotExist:
            attrs["user"] = None
            raise serializers.ValidationError("User not found")

        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True, allow_blank=False)
    new_password = serializers.CharField(required=True, allow_blank=False)

    def validate(self, attrs: dict) -> dict:
        current_password = attrs.get("current_password", None)
        user: User = self.context["request"].user

        if not user.check_password(current_password):
            attrs["user"] = None
            raise serializers.ValidationError("Invalid current password")
        else:
            attrs["user"] = user
        return super().validate(attrs)


class RoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["id", "name"]