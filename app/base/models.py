from django.db import models
from app.core.models import AbstractModel
from app.auth_user.models import UserProfile

class BaseImageFile(AbstractModel):
    ref_type = models.CharField(max_length=250, null=True, blank=True)
    file_url = models.ImageField(upload_to="app/storage/user", null=True, blank=True)
    file_type = models.CharField(max_length=100, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
    user_profile = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="image_files",
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "base_image"