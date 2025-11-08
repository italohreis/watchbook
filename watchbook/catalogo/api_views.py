from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q

from .models import Obra
from .serializers import ObraSerializer


class ObraViewSet(viewsets.ModelViewSet):
    """
    ViewSet para obras do catálogo
    
    Endpoints:
    - GET /api/catalogo/ - listar obras (com busca e filtros)
    - POST /api/catalogo/ - criar nova obra (apenas admin)
    - GET /api/catalogo/{id}/ - detalhe de uma obra
    - PUT/PATCH /api/catalogo/{id}/ - atualizar obra (apenas admin)
    - DELETE /api/catalogo/{id}/ - deletar obra (apenas admin)
    """
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'diretor', 'genero']
    ordering_fields = ['titulo', 'ano_lancamento', 'id']
    ordering = ['-id']
    
    def get_permissions(self):
        """
        Leitura permite qualquer um autenticado
        Criação, atualização e deleção apenas para admin
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """
        Filtra obras por tipo se especificado
        Query params: tipo=filme ou tipo=serie
        """
        queryset = Obra.objects.all()
        tipo = self.request.query_params.get('tipo', None)
        
        if tipo:
            queryset = queryset.filter(tipo=tipo)

        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(Q(titulo__icontains=q))
        
        return queryset
