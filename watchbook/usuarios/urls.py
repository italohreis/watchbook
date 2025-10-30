from django.urls import path
from .views import CadastrarUsuario, RegistrarObraAssistida, MeusRegistros, EditarRegistroAssistido, ExcluirRegistroAssistido, PerfilUsuarioView, RegistrosUsuario

urlpatterns = [
    path('cadastrar/', CadastrarUsuario.as_view(), name='cadastrar-usuario'),
    path('registrar-assistido/<int:obra_id>/', RegistrarObraAssistida.as_view(), name='registrar-assistido'),
    path('meus-registros/', MeusRegistros.as_view(), name='meus-registros'),
    path('editar-registro/<int:pk>/', EditarRegistroAssistido.as_view(), name='editar-registro'),
    path('excluir-registro/<int:pk>/', ExcluirRegistroAssistido.as_view(), name='excluir-registro'),
    path('perfil/', PerfilUsuarioView.as_view(), name='perfil-usuario'),
    path('perfil/<int:user_id>/', PerfilUsuarioView.as_view(), name='perfil-usuario-visitante'),
    path('registros/<int:user_id>/', RegistrosUsuario.as_view(), name='registros-usuario'),
]