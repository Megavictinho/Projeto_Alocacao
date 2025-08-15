from django.contrib import admin
from .models import (
    Modulo, Setor, TipoEquipamento, TagEquipamento, Defeito, Causa,
    CategoriaRTI, Recomendacao, TipoObjeto, Acesso, Revestimento,
    Dano, Objeto, ImagemObjeto, Inspecao
)

class ImagemObjetoInline(admin.TabularInline):
    model = ImagemObjeto
    extra = 1 

@admin.register(Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    inlines = [ImagemObjetoInline]
    
admin.site.register(Modulo)
admin.site.register(Setor)
admin.site.register(TipoEquipamento)
admin.site.register(TagEquipamento)
admin.site.register(Defeito)
admin.site.register(Causa)
admin.site.register(CategoriaRTI)
admin.site.register(Recomendacao)
admin.site.register(TipoObjeto)
admin.site.register(Acesso)
admin.site.register(Revestimento)
admin.site.register(Dano)
admin.site.register(Inspecao)