from django.contrib import admin

from .models import AnaliseProcessoSV
from .models import Semana
from .models import Empresa

# Register your models here.
admin.site.register(AnaliseProcessoSV)
admin.site.register(Semana)
admin.site.register(Empresa)