from django.db import models
from django.utils.translation import gettext_lazy as _


class UserType(models.TextChoices):
    FRONT = 'front', _('Frontstage')
    BACK = 'back', _('Backstage')
