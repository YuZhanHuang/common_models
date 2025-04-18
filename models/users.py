from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone

from common_models.common.constant import UserType


class UserManager(BaseUserManager):
    def _create_user(self, username, email, user_type, **extra):
        if not username:
            raise ValueError("The username must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, user_type=user_type, **extra)
        user.set_password(extra.get('password'))
        user.save(using=self._db)
        return user

    def create_user(self, username, email, **extra):
        return self._create_user(username, email, user_type=User.USER_TYPE_FRONT, **extra)

    def create_backstage(self, username, email, **extra):
        return self._create_user(username, email, user_type=User.USER_TYPE_BACK, **extra)

    def create_superuser(self, username, email, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self._create_user(username, email, user_type=User.USER_TYPE_BACK, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        app_label = "common_models"
        verbose_name = "User"
        verbose_name_plural = "Users"

    # 1) Distinguish front vs back
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.FRONT,
        verbose_name="user type",
        help_text="Distinguish front‑end vs admin users",
    )

    # 2) Shared fields
    username = models.CharField(max_length=255, unique=True, verbose_name="帳號")
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="信箱")
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="名")
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="姓")
    address = models.TextField(blank=True, null=True, verbose_name="通訊地址")
    birthday = models.DateField(blank=True, null=True, verbose_name="生日日期")
    # avatar = models.ForeignKey(
    #     "common_models.File",
    #     null=True, blank=True,
    #     on_delete=models.SET_NULL,
    #     related_name="user_avatars",
    #     verbose_name="大頭貼",
    # )
    is_active = models.BooleanField(default=True, verbose_name="是否啟用")
    is_staff = models.BooleanField(default=False, verbose_name="是否為員工或管理員")
    is_deleted = models.BooleanField(default=False, verbose_name="軟刪除")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="註冊時間")

    # 3) Front‑only
    nickname = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="暱稱")
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True, verbose_name="手機")
    mcoin = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    member_level = models.CharField(
        max_length=10,
        choices=[("一般", "一般"), ("VIP", "VIP")],
        default="一般",
    )
    member_type = models.CharField(
        max_length=10,
        choices=[("會員", "會員"), ("創作者", "創作者")],
        default="會員",
    )
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    # 4) Back‑only
    failed_attempts = models.PositiveIntegerField(default=0, verbose_name="累計登入失敗次數")
    created_by = models.ForeignKey(
        "self",
        limit_choices_to={"user_type": UserType.BACK},
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="created_users",
        verbose_name="創建者",
    )
    updated_by = models.ForeignKey(
        "self",
        limit_choices_to={"user_type": UserType.BACK},
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="updated_users",
        verbose_name="最後修改者",
    )

    # 5) Shared relations
    roles = models.ManyToManyField(
        "common_models.Role",
        related_name="users",
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
