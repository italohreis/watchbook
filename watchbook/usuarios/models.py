from django.db import models
from django.contrib.auth.models import User
from catalogo.models import Obra 
from django.db.models import Count, Avg, Q
from amizade.models import Amizade

class RegistroAssistido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registros")
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="registros")
    data_assistido = models.DateTimeField(auto_now_add=True)
    nota = models.SmallIntegerField(blank=True, null=True)
    critica = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('usuario', 'obra')

    def __str__(self):
        return f"{self.usuario.username} assistiu {self.obra.titulo}"

# Extensão do modelo User
class PerfilUsuario(User):
    """
    Proxy model para adicionar métodos e properties ao User
    sem modificar a tabela do banco de dados
    """
    class Meta:
        proxy = True
    
    @property
    def total_obras(self):
        """Retorna o total de obras assistidas pelo usuário"""
        return self.registros.count()
    
    @property
    def total_filmes(self):
        """Retorna o total de filmes assistidos pelo usuário"""
        return self.registros.filter(obra__tipo='filme').count()
    
    @property
    def total_series(self):
        """Retorna o total de séries assistidas pelo usuário"""
        return self.registros.filter(obra__tipo='serie').count()
    
    @property
    def genero_favorito(self):
        """Retorna o gênero mais assistido pelo usuário"""
        generos = self.registros.values('obra__genero').annotate(
            total=Count('id')
        ).order_by('-total')
        return generos.first()['obra__genero'] if generos else None
    
    @property
    def nota_media(self):
        """Retorna a nota média das avaliações do usuário"""
        avaliacoes = self.registros.filter(nota__isnull=False)
        if avaliacoes.exists():
            return avaliacoes.aggregate(Avg('nota'))['nota__avg']
        return None
    
    @property
    def total_amigos(self):
        """Retorna o total de amigos do usuário"""
        return Amizade.objects.filter(
            Q(de_usuario=self, status='ACEITO') |
            Q(para_usuario=self, status='ACEITO')
        ).count()
    
    def get_registros_recentes(self, limit=5):
        """Retorna os registros mais recentes do usuário"""
        return self.registros.order_by('-data_assistido')[:limit]
    
    def sao_amigos(self, outro_usuario):
        """Verifica se este usuário é amigo de outro usuário"""
        return Amizade.objects.filter(
            Q(de_usuario=self, para_usuario=outro_usuario, status='ACEITO') |
            Q(de_usuario=outro_usuario, para_usuario=self, status='ACEITO')
        ).exists()