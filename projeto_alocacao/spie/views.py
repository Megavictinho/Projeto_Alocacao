from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import *
from .forms import *


def get_tipos_equipamento_ajax(request):
    plataforma_id = request.GET.get('plataforma_id')
    tipos = TipoEquipamento.objects.filter(plataforma_id=plataforma_id).order_by('nome')
    return JsonResponse(list(tipos.values('id', 'nome')), safe=False)


def get_tags_equipamento_ajax(request):
    tipo_id = request.GET.get('tipo_equipamento_id')
    tags = TagEquipamento.objects.filter(tipo_equipamento_id=tipo_id).order_by('chave')
    return JsonResponse(list(tags.values('id', 'chave')), safe=False)


def get_causas_ajax(request):
    defeito_id = request.GET.get('defeito_id')
    causas = Causa.objects.filter(defeito_id=defeito_id).order_by('nome')
    return JsonResponse(list(causas.values('id', 'nome')), safe=False)


class SpieDashboardView(LoginRequiredMixin, ListView):
    model = Modulo
    template_name = 'spie/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Dashboard de Inspeção (SPIE)"
        return context


class ModuloListView(LoginRequiredMixin, ListView):
    model = Modulo
    template_name = 'spie/cadastro_list_generic.html'
    context_object_name = 'itens'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Módulos"
        context['url_adicionar'] = reverse_lazy('spie:modulo_add')
        return context


class ModuloCreateView(LoginRequiredMixin, CreateView):
    model = Modulo
    form_class = ModuloForm
    template_name = 'spie/cadastro_form_generic.html'
    success_url = reverse_lazy('spie:modulo_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Módulo"
        return context


class SetorListView(LoginRequiredMixin, ListView):
    model = Setor
    template_name = 'spie/cadastro_list_generic.html'
    context_object_name = 'itens'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Setores"
        context['url_adicionar'] = reverse_lazy('spie:setor_add')
        return context


class SetorCreateView(LoginRequiredMixin, CreateView):
    model = Setor
    form_class = SetorForm
    template_name = 'spie/cadastro_form_generic.html'
    success_url = reverse_lazy('spie:setor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Setor"
        return context
    

class TipoEquipamentoListView(LoginRequiredMixin, ListView):
    model = TipoEquipamento
    template_name = 'spie/cadastro_list_generic.html'
    context_object_name = 'itens'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Tipos de Equipamento"
        context['url_adicionar'] = reverse_lazy('spie:tipo_equipamento_add')
        return context


class TipoEquipamentoCreateView(LoginRequiredMixin, CreateView):
    model = TipoEquipamento
    form_class = TipoEquipamentoForm
    template_name = 'spie/cadastro_form_generic.html'
    success_url = reverse_lazy('spie:tipo_equipamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Novo Tipo de Equipamento"
        return context


class TagEquipamentoListView(LoginRequiredMixin, ListView):
    model = TagEquipamento
    template_name = 'spie/cadastro_list_generic.html'
    context_object_name = 'itens'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "TAGs de Equipamento"
        context['url_adicionar'] = reverse_lazy('spie:tag_equipamento_add')
        return context


class TagEquipamentoCreateView(LoginRequiredMixin, CreateView):
    model = TagEquipamento
    form_class = TagEquipamentoForm
    template_name = 'spie/cadastro_form_generic.html'
    success_url = reverse_lazy('spie:tag_equipamento_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Nova TAG de Equipamento"
        return context


class CausaListView(LoginRequiredMixin, ListView):
    model = Causa
    template_name = 'spie/cadastro_list_generic.html'
    context_object_name = 'itens'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Causas de Defeito"
        context['url_adicionar'] = reverse_lazy('spie:causa_add')
        return context


class CausaCreateView(LoginRequiredMixin, CreateView):
    model = Causa
    form_class = CausaForm
    template_name = 'spie/cadastro_form_generic.html'
    success_url = reverse_lazy('spie:causa_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Nova Causa"
        return context
    

class InspecaoCreateView(LoginRequiredMixin, CreateView):
    model = Inspecao
    form_class = InspecaoForm
    template_name = 'spie/inspecao_form.html'
    success_url = reverse_lazy('spie:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Criar Nova Inspeção"
        return context
    
    def form_valid(self, form):
        form.instance.usuario = self.request.user
        
    