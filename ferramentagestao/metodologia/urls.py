from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('minhas-instancias/', views.minhas_instancias, name='minhas_instancias'),
    path('criar-instancia/<int:ferramenta_id>/', views.criar_instancia, name='criar_instancia'),
    path('detalhes-instancia/<int:instancia_id>/', views.detalhes_instancia, name='detalhes_instancia'),
    path('editar-instancia/<int:instancia_id>/', views.editar_instancia, name='editar_instancia'),
    path('excluir-instancia/<int:instancia_id>/', views.excluir_instancia, name='excluir_instancia'),
    path('adicionar-participante/<int:instancia_id>/', views.adicionar_participante, name='adicionar_participante'),
    path('metodologia/<int:metodologia_id>/', views.detalhes_metodologia, name='detalhes_metodologia'),
    path('ferramenta/<int:ferramenta_id>/', views.detalhes_ferramenta, name='detalhes_ferramenta'),
    path('ferramenta/<int:ferramenta_id>/adicionar-participante/', views.adicionar_participante, name='adicionar_participante'),
]