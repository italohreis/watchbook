from django.db import models
from django.contrib.auth.models import User

class Amizade(models.Model):
    class StatusAmizade(models.TextChoices):
        PENDENTE = 'PENDENTE', 'Pendente'
        ACEITO = 'ACEITO', 'Aceito'

    de_usuario = models.ForeignKey(User, related_name='amizade_enviada', on_delete=models.CASCADE)
    para_usuario = models.ForeignKey(User, related_name='amizade_recebida', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=StatusAmizade.choices, default=StatusAmizade.PENDENTE)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('de_usuario', 'para_usuario')

    def __str__(self):
        return f"{self.de_usuario} -> {self.para_usuario} ({self.get_status_display()})"