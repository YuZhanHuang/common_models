from django.db import models

from common_models.common.constant import UserType
from common_models.common.mixins import TimeStampedMixin
from common_models.models import User


class Permission(TimeStampedMixin, models.Model):
    class Meta:
        app_label = "common_models"
        ordering = ["category", "code"]

    code = models.CharField(max_length=100, unique=True)  # e.g. user:add
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=255, verbose_name="分類")
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(
        User,
        limit_choices_to={"user_type": UserType.BACK},
        related_name="permissions_created",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name="創建者",
    )
    updated_by = models.ForeignKey(
        User,
        limit_choices_to={"user_type": UserType.BACK},
        related_name="permissions_updated",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name="最後修改者",
    )

    def __str__(self):
        return self.code


class Rule(TimeStampedMixin, models.Model):
    class Meta:
        app_label = "common_models"

    name = models.CharField(max_length=100)
    condition = models.JSONField(
        help_text="權限規則的條件設定，例如 {'region': ['TW', 'JP']}"
    )
    permissions = models.ManyToManyField(
        "common_models.Permission",
        related_name="rules",
    )
    priority = models.IntegerField(default=0, help_text="數字越大優先度越高")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
