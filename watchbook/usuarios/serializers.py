from rest_framework import serializers
from django.contrib.auth.models import User
from .models import RegistroAssistido, PerfilUsuario
from catalogo.models import Obra


class UsuarioSerializer(serializers.ModelSerializer):
    """Serializer básico do usuário"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UsuarioCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário"""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirmar senha')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']
    
    def validate(self, data):
        """Valida se as senhas conferem"""
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': 'As senhas não conferem.'})
        return data
    
    def create(self, validated_data):
        """Cria usuário com senha criptografada"""
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class PerfilUsuarioSerializer(serializers.Serializer):
    """Serializer do perfil com informações calculadas"""
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    total_obras = serializers.IntegerField(read_only=True)
    total_filmes = serializers.IntegerField(read_only=True)
    total_series = serializers.IntegerField(read_only=True)
    genero_favorito = serializers.CharField(read_only=True, allow_null=True)
    nota_media = serializers.FloatField(read_only=True, allow_null=True)
    total_amigos = serializers.IntegerField(read_only=True)


class ObraSimplificadaSerializer(serializers.ModelSerializer):
    """Serializer simplificado de obra para usar em registros"""
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Obra
        fields = ['id', 'titulo', 'poster', 'tipo', 'tipo_display', 'genero', 'ano_lancamento', 'diretor']


class RegistroAssistidoSerializer(serializers.ModelSerializer):
    """Serializer completo de registro para leitura"""
    obra = ObraSimplificadaSerializer(read_only=True)
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = RegistroAssistido
        fields = [
            'id', 'usuario', 'usuario_nome', 'obra',
            'nota', 'critica', 'data_assistido'
        ]
        read_only_fields = ['id', 'usuario', 'data_assistido']
    


class RegistroCreateSerializer(serializers.ModelSerializer):
    """Serializer específico para criação de registros"""
    class Meta:
        model = RegistroAssistido
        fields = ['obra', 'nota', 'critica']
    
    def validate(self, data):
        """Valida se o registro já existe"""
        usuario = self.context['request'].user
        obra = data.get('obra')
        
        if RegistroAssistido.objects.filter(usuario=usuario, obra=obra).exists():
            raise serializers.ValidationError({
                'obra': 'Você já registrou esta obra como assistida.'
            })
        
        return data
    
    def create(self, validated_data):
        """Adiciona o usuário automaticamente"""
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)


class RegistroUpdateSerializer(serializers.ModelSerializer):
    """Serializer para atualização de registros"""
    class Meta:
        model = RegistroAssistido
        fields = ['nota', 'critica']
