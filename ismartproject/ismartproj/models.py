from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    fName = models.CharField(max_length=100)
    mName = models.CharField(max_length=100)
    lName = models.CharField(max_length=100)
    sName = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    # Add other fields as needed

    # Add a related_name argument to prevent clashes
    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='customuser_set')
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_set'
    )