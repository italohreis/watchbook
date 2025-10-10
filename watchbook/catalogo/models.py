from django.db import models

class Obra(models.Model):
    titulo = models.CharField(max_length=200)
    ano_lancamento = models.IntegerField()
    diretor = models.CharField(max_length=150, blank=True)
    genero = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

    def __str__(self):
        return f"{self.titulo} ({self.ano_lancamento})"