from django.urls import path
from .views import cadastrar_dados, ListaDadosView
from .views import gerar_relatorio_pdf, listar_dados, cadastrar_usuario
from . import views
from django.contrib.auth import views as auth_views

#importacoes para app movel
from django.urls import path
from .views import RegisterUserView, LoginUserView

urlpatterns = [
    path('cadastrar/', cadastrar_dados, name='cadastrar_dados'),
    path('listar/', ListaDadosView.as_view(), name='listar_dados'),
    path('relatorio_pdf/', gerar_relatorio_pdf, name='gerar_relatorio_pdf'),
    path('dados/', listar_dados, name='listar_dados'),

    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_usuario, name='login_usuario'),
    path('logout/', views.logout_usuario, name='logout_usuario'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('editar/<int:pk>/', views.editar_dados, name='editar_dados'),
    path('excluir/<int:pk>/', views.excluir_dados, name='excluir_dados'),

    #urls para app movel
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
]
