from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .api_views import UsuarioViewSet, RegistroAssistidoViewSet

# Cria o router e registra os ViewSets
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'registros', RegistroAssistidoViewSet, basename='registro')

# URLs da API
urlpatterns = [
    # Endpoint de autenticação por token
    path('login/', obtain_auth_token, name='api_token_auth'),
    
    # URLs geradas automaticamente pelo router
    path('', include(router.urls)),
]
