from rest_framework import serializers
from .models import Obra


class ObraSerializer(serializers.ModelSerializer):
    """Serializer completo de obra"""
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Obra
        fields = [
            'id', 'titulo', 'ano_lancamento', 'diretor', 
            'genero', 'poster', 'tipo', 'tipo_display'
        ]
        read_only_fields = ['id']
