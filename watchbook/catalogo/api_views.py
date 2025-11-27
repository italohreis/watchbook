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
    - POST /api/catalogo/ - criar nova obra 
    - GET /api/catalogo/{id}/ - detalhe de uma obra
    - PUT/PATCH /api/catalogo/{id}/ - atualizar obra 
    - DELETE /api/catalogo/{id}/ - deletar obra 
    """
    queryset = Obra.objects.all()
    serializer_class = ObraSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['titulo', 'diretor', 'genero']
    ordering_fields = ['titulo']
    ordering = ['titulo']
    
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
