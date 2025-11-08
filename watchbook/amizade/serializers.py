from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Amizade


class UsuarioSimplificadoSerializer(serializers.ModelSerializer):
    """Serializer simplificado de usuário para usar em amizades"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
        read_only_fields = ['id', 'username', 'first_name', 'last_name']


class AmizadeSerializer(serializers.ModelSerializer):
    """Serializer completo de amizade para leitura"""
    de_usuario = UsuarioSimplificadoSerializer(read_only=True)
    para_usuario = UsuarioSimplificadoSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Amizade
        fields = [
            'id', 'de_usuario', 'para_usuario', 
            'status', 'status_display', 'data_criacao'
        ]
        read_only_fields = ['id', 'de_usuario', 'status', 'data_criacao']


class AmizadeCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de solicitação de amizade"""
    para_usuario = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all()
    )
    
    class Meta:
        model = Amizade
        fields = ['para_usuario']
    
    def validate_para_usuario(self, value):
        """Valida se não está tentando adicionar a si mesmo"""
        usuario = self.context['request'].user
        
        if value == usuario:
            raise serializers.ValidationError('Você não pode adicionar a si mesmo como amigo.')
        
        # Verifica se já existe amizade em qualquer direção
        if Amizade.objects.filter(
            de_usuario=usuario, para_usuario=value
        ).exists():
            raise serializers.ValidationError('Você já enviou uma solicitação para este usuário.')
        
        if Amizade.objects.filter(
            de_usuario=value, para_usuario=usuario
        ).exists():
            raise serializers.ValidationError('Este usuário já enviou uma solicitação para você.')
        
        return value
    
    def create(self, validated_data):
        """Cria a solicitação de amizade"""
        validated_data['de_usuario'] = self.context['request'].user
        validated_data['status'] = 'PENDENTE'
        return super().create(validated_data)
