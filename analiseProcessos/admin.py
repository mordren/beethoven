from django.contrib import admin

from .models import AnaliseProcesso
from .models import Semana
from .models import Empresa

# Register your models here.
admin.site.register(AnaliseProcesso)
admin.site.register(Semana)
admin.site.register(Empresa)