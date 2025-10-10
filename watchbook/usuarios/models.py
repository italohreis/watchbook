from django.db import models
from django.contrib.auth.models import User
from catalogo.models import Obra 

class RegistroAssistido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="registros")
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name="registros")
    data_assistido = models.DateField()
    nota = models.SmallIntegerField(blank=True, null=True)
    critica = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('usuario', 'obra')

    def __str__(self):
        return f"{self.usuario.username} assistiu {self.obra.titulo}"