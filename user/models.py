from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Empresa(models.Model):
    nome = models.CharField(max_length=60)
    SV = models.BooleanField(default=False)
    PP = models.BooleanField(default=False)
    OIVA = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class UserProfile(models.Model):
    user = models.OneToOneField(
        User, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE
    )
    empresa = models.ForeignKey(Empresa, on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
  
