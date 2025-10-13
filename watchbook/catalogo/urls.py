from django.urls import path
from .views import ListarObras

urlpatterns = [
    path('', ListarObras.as_view(), name='buscar-obras'),
]