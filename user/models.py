from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import gettext_lazy as _
from atividades.models import Empresa

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE
    )
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)