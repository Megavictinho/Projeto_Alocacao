# spie/urls.py

from django.urls import path
from . import views

app_name = 'spie'

urlpatterns = [
    path('', views.SpieDashboardView.as_view(), name='dashboard'),
    path('cadastros/modulo/', views.ModuloListView.as_view(), name='modulo_list'),
    path('cadastros/modulo/novo/', views.ModuloCreateView.as_view(), name='modulo_add'),
    path('cadastros/setor/', views.SetorListView.as_view(), name='setor_list'),
    path('cadastros/setor/novo/', views.SetorCreateView.as_view(), name='setor_add'),
    path('cadastros/tipo_equipamento/', views.TipoEquipamentoListView.as_view(), name='tipo_equipamento_list'),
    path('cadastros/tipo_equipamento/novo/', views.TipoEquipamentoCreateView.as_view(), name='tipo_equipamento_add'),
    path('cadastros/tag_equipamento/', views.TagEquipamentoListView.as_view(), name='tag_equipamento_list'),
    path('cadastros/tag_equipamento/novo/', views.TagEquipamentoCreateView.as_view(), name='tag_equipamento_add'),
    path('cadastros/causa/', views.CausaListView.as_view(), name='causa_list'),
    path('cadastros/causa/novo/', views.CausaCreateView.as_view(), name='causa_add'),
    path('inspecao/nova/', views.InspecaoCreateView.as_view(), name='inspecao_add'),
    path('ajax/tipos-equipamento/', views.get_tipos_equipamento_ajax, name='ajax_get_tipos_equipamento'),
    path('ajax/tags-equipamento/', views.get_tags_equipamento_ajax, name='ajax_get_tags_equipamento'),
    path('ajax/causas/', views.get_causas_ajax, name='ajax_get_causas'),
]