from django.urls import path
from . import views

urlpatterns = [
    path('alocacoes', views.dashboard_geral, name='dashboard_geral'),
    path('usuario/novo/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('plataforma/nova/', views.cadastrar_plataforma, name='cadastrar_plataforma'),
    path('alocacao/nova/', views.cadastrar_alocacao, name='cadastrar_alocacao'),
    path('plataforma/<int:plataforma_id>/', views.dashboard_por_plataforma, name='dashboard_por_plataforma'),
    path('embarques/', views.dashboard_embarque_mes, name='dashboard_embarque_mes'),
    path('desembarques/', views.dashboard_desembarque_mes, name='dashboard_desembarque_mes'),
    path('alocacao/<int:alocacao_id>/editar/', views.editar_alocacao, name='editar_alocacao'),
]