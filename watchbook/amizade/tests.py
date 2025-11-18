from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from .models import Amizade

class TestesModelAmizade(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='12345')
        self.user2 = User.objects.create_user(username='user2', password='12345')
        self.user3 = User.objects.create_user(username='user3', password='12345')
        
        self.amizade_pendente = Amizade.objects.create(
            de_usuario=self.user1,
            para_usuario=self.user2,
            status='PENDENTE'
        )
        
        self.amizade_aceita = Amizade.objects.create(
            de_usuario=self.user1,
            para_usuario=self.user3,
            status='ACEITO'
        )
    
    def test_str(self):
        self.assertEqual(str(self.amizade_pendente), "user1 -> user2 (Pendente)")
        self.assertIn("user1", str(self.amizade_aceita))
        self.assertIn("Aceito", str(self.amizade_aceita))

class TestesViewPaginaAmigos(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.amigo = User.objects.create_user(username='amigo', first_name='Amigo Silva', password='12345')
        self.outro = User.objects.create_user(username='outro', first_name='Outro Usuário', password='12345')
        self.client.force_login(user=self.user)
        self.url = reverse('pagina-amigos')
    
    def test_get_sem_query(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        resultados = response.context.get('resultados')
        self.assertEqual(len(resultados), 0)
    
    def test_buscar_por_username(self):
        response = self.client.get(self.url, {'q': 'amigo'})
        self.assertEqual(response.status_code, 200)
        resultados = response.context.get('resultados')
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].username, 'amigo')
    
    def test_buscar_por_nome(self):
        response = self.client.get(self.url, {'q': 'Outro'})
        self.assertEqual(response.status_code, 200)
        resultados = response.context.get('resultados')
        self.assertEqual(len(resultados), 1)
        self.assertEqual(resultados[0].first_name, 'Outro Usuário')
    
    
    def test_pedidos_pendentes_no_context(self):
        Amizade.objects.create(
            de_usuario=self.amigo,
            para_usuario=self.user,
            status='PENDENTE'
        )
        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        pedidos = response.context.get('pedidos_pendentes')
        self.assertEqual(len(pedidos), 1)
        self.assertEqual(pedidos[0].de_usuario, self.amigo)


class TestesViewEnviarPedidoAmizade(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.outro_user = User.objects.create_user(username='outro', password='12345')
        self.client.force_login(user=self.user)
        self.url = reverse('enviar-pedido', kwargs={'user_id': self.outro_user.pk})
    
    
    def test_post_cria_pedido(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pagina-amigos'))
        
        self.assertEqual(Amizade.objects.count(), 1)
        amizade = Amizade.objects.first()
        self.assertEqual(amizade.de_usuario, self.user)
        self.assertEqual(amizade.para_usuario, self.outro_user)
        self.assertEqual(amizade.status, 'PENDENTE')
    
    def test_post_pedido_duplicado_nao_cria_novo(self):
        self.client.post(self.url)
        self.assertEqual(Amizade.objects.count(), 1)
        
        # Tentar enviar novamente (get_or_create não duplica)
        self.client.post(self.url)
        self.assertEqual(Amizade.objects.count(), 1)
    
    def test_usuario_inexistente(self):
        url_invalida = reverse('enviar-pedido', kwargs={'user_id': 9999})
        response = self.client.post(url_invalida)
        self.assertEqual(response.status_code, 404)


class TestesViewResponderPedidoAmizade(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.outro_user = User.objects.create_user(username='outro', password='12345')
        self.client.force_login(user=self.user)
        
        self.pedido = Amizade.objects.create(
            de_usuario=self.outro_user,
            para_usuario=self.user,
            status='PENDENTE'
        )
        self.url_aceitar = reverse('responder-pedido', kwargs={
            'pedido_id': self.pedido.pk,
            'acao': 'aceitar'
        })
        self.url_recusar = reverse('responder-pedido', kwargs={
            'pedido_id': self.pedido.pk,
            'acao': 'recusar'
        })
    
    def test_aceitar_pedido(self):
        response = self.client.post(self.url_aceitar)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pagina-amigos'))
        
        pedido_atualizado = Amizade.objects.get(pk=self.pedido.pk)
        self.assertEqual(pedido_atualizado.status, 'ACEITO')
    
    def test_recusar_pedido(self):
        response = self.client.post(self.url_recusar)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('pagina-amigos'))
        
        self.assertEqual(Amizade.objects.count(), 0)

    
    def test_pedido_inexistente(self):
        url_invalida = reverse('responder-pedido', kwargs={
            'pedido_id': 9999,
            'acao': 'aceitar'
        })
        response = self.client.post(url_invalida)
        self.assertEqual(response.status_code, 404)
