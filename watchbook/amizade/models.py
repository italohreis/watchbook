from django.db import models
from django.contrib.auth.models import User
from .consts import STATUS_AMIZADE

class Amizade(models.Model):
    de_usuario = models.ForeignKey(User, related_name='amizade_enviada', on_delete=models.CASCADE)
    para_usuario = models.ForeignKey(User, related_name='amizade_recebida', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_AMIZADE, default='PENDENTE')
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('de_usuario', 'para_usuario')

    def __str__(self):
        return f"{self.de_usuario} -> {self.para_usuario} ({self.get_status_display()})"