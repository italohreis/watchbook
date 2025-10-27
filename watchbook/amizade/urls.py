from django.urls import path
from .views import PaginaAmigos, EnviarPedidoAmizade, ResponderPedidoAmizade, RemoverAmizade

urlpatterns = [
    path('', PaginaAmigos.as_view(), name='pagina-amigos'),
    path('enviar-pedido/<int:user_id>/', EnviarPedidoAmizade.as_view(), name='enviar-pedido'),
    path('responder-pedido/<int:pedido_id>/<str:acao>/', ResponderPedidoAmizade.as_view(), name='responder-pedido'),
    path('remover-amizade/<int:user_id>/', RemoverAmizade.as_view(), name='remover-amizade'),
]