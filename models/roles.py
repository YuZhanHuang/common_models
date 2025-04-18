from django.db import models

from common_models.common.constant import UserType
from common_models.common.mixins import TimeStampedMixin
from common_models.models import User


class Role(TimeStampedMixin, models.Model):
    class Meta:
        app_label = "common_models"

    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(
        "common_models.Permission",
        related_name="roles",
    )
    level = models.PositiveIntegerField(
        help_text="角色層級，數字越小權限越高",
        null=True,
    )
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User,
        limit_choices_to={"user_type": UserType.BACK},
        related_name="roles_created",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name="創建者",
    )
    updated_by = models.ForeignKey(
        User,
        limit_choices_to={"user_type": UserType.BACK},
        related_name="roles_updated",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name="最後修改者",
    )

    def __str__(self):
        return self.name
