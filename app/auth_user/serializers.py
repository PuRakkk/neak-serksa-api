from rest_framework import serializers
from app.auth_user.models import User, UserProfile
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.validators import UniqueValidator
from app.base.serializers import BaseImageFileSerializer
from app.base.models import BaseImageFile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=False)
    profile_image_info = serializers.SerializerMethodField()
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
            "language",
            "profile_image_info"
        ]

    def get_profile_image_info(self, instance):
        image = BaseImageFile.objects.filter(
            user_profile_id=instance,
            ref_type="user_profile",
            is_delete=False
        ).first()
        return BaseImageFileSerializer(image, many=False).data if image else None


class UserSerializer(WritableNestedModelSerializer):
    user_profile = UserProfileSerializer()
    email = serializers.CharField(
        validators = [UniqueValidator(User.objects.all(), message="old_user")]
    )
    class Meta:
        model = User
        fields = ["email" ,"user_profile"]