from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import UsuarioViewSet, RegistroAssistidoViewSet

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'registros', RegistroAssistidoViewSet, basename='registro')

urlpatterns = [
    path('', include(router.urls)),
]
