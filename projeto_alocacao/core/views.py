from django.shortcuts import render, redirect
from .forms import UsuarioForm, PlataformaForm, AlocacaoForm
from .models import Alocacao, Plataforma, LogAlocacao
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard_geral')
    else:
        form = UsuarioForm()
    return render(request, 'core/form_generico.html', {'form': form, 'titulo': 'Cadastrar Usuário'})

@login_required
def cadastrar_plataforma(request):
    if request.method == 'POST':
        form = PlataformaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard_geral')
    else:
        form = PlataformaForm()
    return render(request, 'core/form_generico.html', {'form': form, 'titulo': 'Cadastrar Plataforma'})

@login_required
def cadastrar_alocacao(request):
    if request.method == 'POST':
        form = AlocacaoForm(request.POST)
        if form.is_valid():
            nova_alocacao = form.save()
            LogAlocacao.objects.create(
                usuario=request.user,
                acao='Criação',
                alocacao=nova_alocacao,
                detalhes=f"Usuário '{nova_alocacao.usuario.nome}' alocado na plataforma '{nova_alocacao.plataforma.nome}' de {nova_alocacao.data_entrada.strftime('%d/%m/%Y')} a {nova_alocacao.data_saida.strftime('%d/%m/%Y')}."
            )
            return redirect('dashboard_geral')
    else:
        form = AlocacaoForm()
    return render(request, 'core/form_generico.html', {'form': form, 'titulo': 'Cadastrar Alocação'})

@login_required
def dashboard_geral(request):
    alocacoes = Alocacao.objects.select_related('usuario', 'plataforma').order_by('plataforma__nome', 'data_entrada')
    contexto = {
        'alocacoes': alocacoes,
        'titulo': 'Dashboard'
    }
    return render(request, 'core/dashboard.html', contexto)

@login_required
def dashboard_por_plataforma(request, plataforma_id):
    plataforma = Plataforma.objects.get(id=plataforma_id)
    alocacoes = Alocacao.objects.filter(plataforma=plataforma).select_related('usuario').order_by('data_entrada')
    contexto = {
        'alocacoes': alocacoes,
        'titulo': f'Dashboard da Plataforma: {plataforma.nome}'
    }
    return render(request, 'core/dashboard.html', contexto)

@login_required
def dashboard_embarque_mes(request):
    hoje = timezone.now().date()
    alocacoes = Alocacao.objects.filter(
        data_entrada__year=hoje.year,
        data_entrada__month=hoje.month
    ).select_related('usuario', 'plataforma').order_by('data_entrada')
    contexto = {
        'alocacoes': alocacoes,
        'titulo': f'Embarque do Mês ({hoje.strftime("%B/%Y")})'
    }
    return render(request, 'core/dashboard.html', contexto)

@login_required
def dashboard_desembarque_mes(request):
    hoje = timezone.now().date()
    alocacoes = Alocacao.objects.filter(
        data_saida__year=hoje.year,
        data_saida__month=hoje.month
    ).select_related('usuario', 'plataforma').order_by('data_saida')
    contexto = {
        'alocacoes': alocacoes,
        'titulo': f'Desembarque do Mês ({hoje.strftime("%B/%Y")})'
    }
    return render(request, 'core/dashboard.html', contexto)

@login_required
def editar_alocacao(request, alocacao_id):
    alocacao = get_object_or_404(Alocacao, pk=alocacao_id)
    if request.method == 'POST':
        form = AlocacaoForm(request.POST, instance=alocacao)
        if form.is_valid():
            alocacao_editada = form.save()
            LogAlocacao.objects.create(
                usuario=request.user,
                acao='Atualização',
                alocacao=alocacao_editada,
                detalhes=f"Alocação atualizada para o período de {alocacao_editada.data_entrada.strftime('%d/%m/%Y')} a {alocacao_editada.data_saida.strftime('%d/%m/%Y')}."
            )

            return redirect('dashboard_geral')
    else:
        form = AlocacaoForm(instance=alocacao)

    return render(request, 'core/form_generico.html', {'form': form, 'titulo': f'Editar Alocação de {alocacao.usuario.nome}'})