from django.urls import path
from .views import CadastrarUsuario, RegistrarObraAssistida, MeusRegistrosView

urlpatterns = [
    path('cadastrar/', CadastrarUsuario.as_view(), name='cadastrar-usuario'),
    path('registrar-assistido/<int:obra_id>/', RegistrarObraAssistida.as_view(), name='registrar-assistido'),
    path('meus-registros/', MeusRegistrosView.as_view(), name='meus-registros'),
]