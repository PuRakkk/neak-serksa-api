from rest_framework import serializers
from app.auth_user.models import User, UserProfile
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.validators import UniqueValidator


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = [
            "email",
            "first_name",
            "last_name",
            "username",
            "phone_number",
            "address",
            "status",
            "language"
        ]

class UserSerializer(WritableNestedModelSerializer):
    user_profile = UserProfileSerializer()
    email = serializers.CharField(
        validators = [UniqueValidator(User.objects.all(), message="old_user")]
    )
    class Meta:
        model = User
        fields = ["email" ,"user_profile"]