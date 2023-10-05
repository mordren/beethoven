from django.contrib import admin

from .models import AnaliseProcessoSV
from .models import Semana
from .models import Empresa
from .models import AnaliseProcesso
from .models import AnaliseProcessoResposta
from .models import Questao

# Register your models here.
admin.site.register(AnaliseProcessoSV)
admin.site.register(Semana)
admin.site.register(AnaliseProcesso)
admin.site.register(AnaliseProcessoResposta)
admin.site.register(Questao)