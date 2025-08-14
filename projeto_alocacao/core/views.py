from django.shortcuts import render, redirect
from .forms import UsuarioForm, PlataformaForm, AlocacaoForm
from .models import Alocacao, Plataforma
from django.utils import timezone

def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES) # Adicionar request.FILES para a foto
        if form.is_valid():
            form.save()
            return redirect('dashboard_geral')
    else:
        form = UsuarioForm()
    return render(request, 'core/form_generico.html', {'form': form, 'titulo': 'Cadastrar Usuário'})

def cadastrar_plataforma(request):
    if request.method == 'POST':
        form = PlataformaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_geral')
    else:
        form = PlataformaForm()
    return render(request, 'core/form_generico.html', {'form': form, 'titulo': 'Cadastrar Plataforma'})

def cadastrar_alocacao(request):
    if request.method == 'POST':
        form = AlocacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_geral')
    else:
        form = AlocacaoForm()
    return render(request, 'core/form_generico.html', {'form': form, 'titulo': 'Cadastrar Alocação'})

def dashboard_geral(request):
    alocacoes = Alocacao.objects.select_related('usuario', 'plataforma').order_by('plataforma__nome', 'data_entrada')
    contexto = {
        'alocacoes': alocacoes,
        'titulo': 'Dashboard Geral de Alocações'
    }
    return render(request, 'core/dashboard.html', contexto)

def dashboard_por_plataforma(request, plataforma_id):
    plataforma = Plataforma.objects.get(id=plataforma_id)
    alocacoes = Alocacao.objects.filter(plataforma=plataforma).select_related('usuario').order_by('data_entrada')
    contexto = {
        'alocacoes': alocacoes,
        'titulo': f'Dashboard da Plataforma: {plataforma.nome}'
    }
    return render(request, 'core/dashboard.html', contexto)

def dashboard_embarque_mes(request):
    hoje = timezone.now().date()
    alocacoes = Alocacao.objects.filter(
        data_entrada__year=hoje.year,
        data_entrada__month=hoje.month
    ).select_related('usuario', 'plataforma').order_by('data_entrada')
    contexto = {
        'alocacoes': alocacoes,
        'titulo': f'Dashboard de Embarques do Mês Atual ({hoje.strftime("%B/%Y")})'
    }
    return render(request, 'core/dashboard.html', contexto)

def dashboard_desembarque_mes(request):
    hoje = timezone.now().date()
    alocacoes = Alocacao.objects.filter(
        data_saida__year=hoje.year,
        data_saida__month=hoje.month
    ).select_related('usuario', 'plataforma').order_by('data_saida')
    contexto = {
        'alocacoes': alocacoes,
        'titulo': f'Dashboard de Desembarques do Mês Atual ({hoje.strftime("%B/%Y")})'
    }
    return render(request, 'core/dashboard.html', contexto)