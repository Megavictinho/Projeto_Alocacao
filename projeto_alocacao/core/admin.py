from django.contrib import admin
from .models import Usuario, Plataforma, Alocacao, LogAlocacao

admin.site.register(Usuario)
admin.site.register(Plataforma)
admin.site.register(Alocacao)
admin.site.register(LogAlocacao)