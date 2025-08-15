from django import forms
from .models import Inspecao
from .models import (
    Modulo, Setor, TipoEquipamento, TagEquipamento, Defeito, Causa,
    CategoriaRTI, Recomendacao, TipoObjeto, Acesso, Revestimento, Dano
)

class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['nome']

class SetorForm(forms.ModelForm):
    class Meta:
        model = Setor
        fields = ['nome']

class DefeitoForm(forms.ModelForm):
    class Meta:
        model = Defeito
        fields = ['nome']

class CategoriaRTIForm(forms.ModelForm):
    class Meta:
        model = CategoriaRTI
        fields = ['nome']

class RecomendacaoForm(forms.ModelForm):
    class Meta:
        model = Recomendacao
        fields = ['nome']

class TipoObjetoForm(forms.ModelForm):
    class Meta:
        model = TipoObjeto
        fields = ['nome']

class AcessoForm(forms.ModelForm):
    class Meta:
        model = Acesso
        fields = ['nome']

class RevestimentoForm(forms.ModelForm):
    class Meta:
        model = Revestimento
        fields = ['nome']

class DanoForm(forms.ModelForm):
    class Meta:
        model = Dano
        fields = ['nome']

class TipoEquipamentoForm(forms.ModelForm):
    class Meta:
        model = TipoEquipamento
        fields = ['nome', 'plataforma']

class TagEquipamentoForm(forms.ModelForm):
    class Meta:
        model = TagEquipamento
        fields = ['chave', 'tipo_equipamento']
        
class CausaForm(forms.ModelForm):
    class Meta:
        model = Causa
        fields = ['nome', 'defeito']

class InspecaoForm(forms.ModelForm):
    class Meta:
        model = Inspecao
        fields = [
            'nota_zr', 'plataforma', 'modulo', 'setor', 'localizacao',
            'tipo_equipamento', 'tag_equipamento', 'defeito', 'causa',
            'categoria_rti', 'recomendacao', 'objetos'
        ]

class InspecaoForm(forms.ModelForm):
    class Meta:
        model = Inspecao
        fields = [
            'nota_zr', 'plataforma', 'modulo', 'setor', 'localizacao',
            'tipo_equipamento', 'tag_equipamento', 'defeito', 'causa',
            'categoria_rti', 'recomendacao', 'objetos'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inicia os campos dependentes como vazios
        self.fields['tipo_equipamento'].queryset = TipoEquipamento.objects.none()
        self.fields['tag_equipamento'].queryset = TagEquipamento.objects.none()
        self.fields['causa'].queryset = Causa.objects.none()

class InspecaoForm(forms.ModelForm):
    class Meta:
        model = Inspecao
        fields = [
            'nota_zr', 'plataforma', 'modulo', 'setor', 'localizacao',
            'tipo_equipamento', 'tag_equipamento', 'defeito', 'causa',
            'categoria_rti', 'recomendacao', 'objetos'
        ]
        widgets = {
            'objetos': forms.CheckboxSelectMultiple,
        }

    # MÉTODO CORRIGIDO ABAIXO
    def __init__(self, *args, **kwargs):
        # 1. ESSA LINHA É FUNDAMENTAL E DEVE VIR PRIMEIRO!
        # Ela cria o self.fields e toda a estrutura do formulário.
        super().__init__(*args, **kwargs)

        # 2. SÓ DEPOIS de a linha de cima ser executada, nós podemos
        #    acessar self.fields para modificar os campos.
        self.fields['tipo_equipamento'].queryset = TipoEquipamento.objects.none()
        self.fields['tag_equipamento'].queryset = TagEquipamento.objects.none()
        self.fields['causa'].queryset = Causa.objects.none()

        # Lógica adicional para pré-popular os campos se o formulário já tiver dados (ex: em uma edição)
        if 'plataforma' in self.data:
            try:
                plataforma_id = int(self.data.get('plataforma'))
                self.fields['tipo_equipamento'].queryset = TipoEquipamento.objects.filter(plataforma_id=plataforma_id).order_by('nome')
            except (ValueError, TypeError):
                pass # Ignora se o valor não for um número
        
        if 'tipo_equipamento' in self.data:
            try:
                tipo_id = int(self.data.get('tipo_equipamento'))
                self.fields['tag_equipamento'].queryset = TagEquipamento.objects.filter(tipo_equipamento_id=tipo_id).order_by('chave')
            except (ValueError, TypeError):
                pass
        
        if 'defeito' in self.data:
            try:
                defeito_id = int(self.data.get('defeito'))
                self.fields['causa'].queryset = Causa.objects.filter(defeito_id=defeito_id).order_by('nome')
            except (ValueError, TypeError):
                pass