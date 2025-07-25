from rest_framework import serializers
from rest_framework import serializers
from app.base.models import BaseImageFile


class BaseImageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseImageFile
        fields = ["file_url"]