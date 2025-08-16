from django import forms
from .models import Inspecao, Objeto
from .models import (Modulo, Setor, TipoEquipamento, TagEquipamento, Defeito, Causa, CategoriaRTI, Recomendacao, TipoObjeto, Acesso, Revestimento, Dano, ImagemObjeto)

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


class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        fields = ['tipo_objeto', 'acesso', 'revestimento', 'dano', 'ex_dano', 'complemento']


ImagemObjetoFormset = forms.inlineformset_factory(
    Objeto,
    ImagemObjeto,
    fields=('imagem',),
    extra=4,
    can_delete=False
)


class InspecaoForm(forms.ModelForm):
    class Meta:
        model = Inspecao
        fields = [
            'nota_zr', 'plataforma', 'modulo', 'setor', 'localizacao',
            'tipo_equipamento', 'tag_equipamento', 'defeito', 'causa',
            'categoria_rti', 'recomendacao', 'objetos'
        ]
        widgets = {
            'objetos': forms.SelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tipo_equipamento'].queryset = TipoEquipamento.objects.none()
        self.fields['tag_equipamento'].queryset = TagEquipamento.objects.none()
        self.fields['causa'].queryset = Causa.objects.none()
        self.fields['objetos'].queryset = Objeto.objects.none()

        if self.is_bound or self.instance.pk:
            if self.is_bound:
                data = self.data
                instance_plataforma = data.get('plataforma')
                instance_tipo_equipamento = data.get('tipo_equipamento')
                instance_defeito = data.get('defeito')
            else:
                instance_plataforma = self.instance.plataforma.pk
                instance_tipo_equipamento = self.instance.tipo_equipamento.pk
                instance_defeito = self.instance.defeito.pk

            try:
                plataforma_id = int(instance_plataforma)
                self.fields['tipo_equipamento'].queryset = TipoEquipamento.objects.filter(plataforma_id=plataforma_id).order_by('nome')
            except (ValueError, TypeError):
                pass 

            try:
                tipo_equipamento_id = int(instance_tipo_equipamento)
                self.fields['tag_equipamento'].queryset = TagEquipamento.objects.filter(tipo_equipamento_id=tipo_equipamento_id).order_by('chave')
            except (ValueError, TypeError):
                pass

            try:
                defeito_id = int(instance_defeito)
                self.fields['causa'].queryset = Causa.objects.filter(defeito_id=defeito_id).order_by('nome')
            except (ValueError, TypeError):
                pass
            
            if self.instance.pk:
                self.fields['objetos'].queryset = Objeto.objects.all()