from django.urls import path
from .views import CadastrarUsuario, RegistrarObraAssistida, MeusRegistrosView, EditarRegistroAssistido, ExcluirRegistroAssistido

urlpatterns = [
    path('cadastrar/', CadastrarUsuario.as_view(), name='cadastrar-usuario'),
    path('registrar-assistido/<int:obra_id>/', RegistrarObraAssistida.as_view(), name='registrar-assistido'),
    path('meus-registros/', MeusRegistrosView.as_view(), name='meus-registros'),
    path('editar-registro/<int:pk>/', EditarRegistroAssistido.as_view(), name='editar-registro'),
    path('excluir-registro/<int:pk>/', ExcluirRegistroAssistido.as_view(), name='excluir-registro'),
]