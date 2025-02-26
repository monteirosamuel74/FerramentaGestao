from django.contrib import admin
from django.utils.html import format_html
from .models import Metodologia, Ferramenta

@admin.register(Ferramenta)  # Registrar o modelo Ferramenta com a classe FerramentaAdmin
class FerramentaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'metodologia', 'imagem_preview')
    readonly_fields = ('imagem_preview',)

    def imagem_preview(self, obj):
        if obj.imagem:  # Verificar se a imagem existe
            return format_html('<img src="{}" style="width: 50px; height: auto;" />', obj.imagem.url)
        return "Nenhuma imagem disponível."

    imagem_preview.short_description = 'Imagem'

# Registrar o modelo Metodologia
admin.site.register(Metodologia)