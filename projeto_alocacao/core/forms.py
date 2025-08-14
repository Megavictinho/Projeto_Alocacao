# core/forms.py

from django import forms
from django.db.models import Q 
from .models import Usuario, Plataforma, Alocacao

class UsuarioChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.nome} ({obj.chave})"

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'chave', 'foto']

class PlataformaForm(forms.ModelForm):
    class Meta:
        model = Plataforma
        fields = ['nome']


class AlocacaoForm(forms.ModelForm):
    usuario = UsuarioChoiceField(
        queryset=Usuario.objects.order_by('nome'),
        label="Usuário"
    )

    class Meta:
        model = Alocacao
        fields = ['usuario', 'plataforma', 'data_entrada', 'data_saida']
        widgets = {
            'data_entrada': forms.DateInput(attrs={'type': 'date'}),
            'data_saida': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        usuario = cleaned_data.get("usuario")
        data_entrada = cleaned_data.get("data_entrada")
        data_saida = cleaned_data.get("data_saida")

        if not usuario or not data_entrada or not data_saida:
            return cleaned_data 

        if data_saida < data_entrada:
            self.add_error('data_saida', "A data de saída não pode ser anterior à data de entrada.")
        
        alocacoes_conflitantes = Alocacao.objects.filter(
            usuario=usuario,
            data_entrada__lte=data_saida,
            data_saida__gte=data_entrada
        )

        if self.instance and self.instance.pk:
            alocacoes_conflitantes = alocacoes_conflitantes.exclude(pk=self.instance.pk)

        if alocacoes_conflitantes.exists():
            conflito = alocacoes_conflitantes.first()
            raise forms.ValidationError(
                f"Conflito de alocação! O usuário já está alocado na plataforma '{conflito.plataforma.nome}' "
                f"entre {conflito.data_entrada.strftime('%d/%m/%Y')} e {conflito.data_saida.strftime('%d/%m/%Y')}."
            )
        
        return cleaned_data