from django import forms
from .models import InstanciaFerramenta
from .models import PDCA, Ferramenta

class PDCAForm(forms.ModelForm):
    class Meta:
        model = PDCA
        fields = ['plano', 'execucao', 'verificacao', 'acao']

class EditarInstanciaForm(forms.ModelForm):
    class Meta:
        model = InstanciaFerramenta
        fields = ['ferramenta', 'dono', 'participantes', 'dados']
        widgets = {
            'plano': forms.TextInput(attrs={'class': 'form-control'}),
            'execucao': forms.TextInput(attrs={'class': 'form-control'}),
            'verificacao': forms.TextInput(attrs={'class': 'form-control'}),
            'acao': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
class AdicionarParticipanteForm(forms.ModelForm):
    class Meta:
        model = Ferramenta
        fields = ['participantes']