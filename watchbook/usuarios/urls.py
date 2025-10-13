from django.urls import path
from .views import CadastrarUsuario

urlpatterns = [
    path('cadastrar/', CadastrarUsuario.as_view(), name='cadastrar-usuario'),
]