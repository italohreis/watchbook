from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from datetime import datetime, date
from catalogo.models import Obra
from .models import RegistroAssistido
from .forms import RegistroAssistidoForm, FormularioCadastro

class TestesModelRegistroAssistido(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.obra = Obra.objects.create(
            titulo="Matrix",
            ano_lancamento=1999,
            genero="Ficção",
            tipo='filme'
        )
        self.registro = RegistroAssistido.objects.create(
            usuario=self.user,
            obra=self.obra,
            nota=5,
            critica="Excelente filme!"
        )
    
    def test_str(self):
        self.assertEqual(str(self.registro), "teste assistiu Matrix")
    
    def test_data_assistido_auto(self):
        self.assertEqual(self.registro.data_assistido, date.today())

class TestesViewRegistrarObraAssistida(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.login(username='teste', password='12345')
        self.obra = Obra.objects.create(
            titulo="Matrix",
            ano_lancamento=1999,
            genero="Ficção"
        )
        self.url = reverse('registrar-assistido', kwargs={'obra_id': self.obra.pk})
    
    def test_post_com_nota_e_critica(self):
        data = {
            'nota': 5,
            'critica': 'Excelente filme!'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meus-registros'))
        
        self.assertEqual(RegistroAssistido.objects.count(), 1)
        registro = RegistroAssistido.objects.first()
        self.assertEqual(registro.usuario, self.user)
        self.assertEqual(registro.obra, self.obra)
        self.assertEqual(registro.nota, 5)
        self.assertEqual(registro.critica, 'Excelente filme!')
    
    def test_post_apenas_nota(self):
        data = {'nota': 4}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        
        registro = RegistroAssistido.objects.first()
        self.assertEqual(registro.nota, 4)
        self.assertEqual(registro.critica, '')
    
    def test_obra_inexistente(self):
        url_invalida = reverse('registrar-assistido', kwargs={'obra_id': 9999})
        response = self.client.post(url_invalida, {'nota': 5})
        self.assertEqual(response.status_code, 404)


class TestesViewEditarRegistroAssistido(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.outro_user = User.objects.create_user(username='outro', password='12345')
        self.client.force_login(user=self.user)
        
        self.obra = Obra.objects.create(
            titulo="Matrix",
            ano_lancamento=1999,
            genero="Ficção"
        )
        self.registro = RegistroAssistido.objects.create(
            usuario=self.user,
            obra=self.obra,
            nota=3,
            critica="Bom"
        )
        self.url = reverse('editar-registro', kwargs={'pk': self.registro.pk})
    
    def test_post_edicao(self):
        data = {
            'nota': 5,
            'critica': 'Melhor filme de todos os tempos!'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meus-registros'))
        
        self.assertEqual(RegistroAssistido.objects.count(), 1)
        registro_atualizado = RegistroAssistido.objects.get(pk=self.registro.pk)
        self.assertEqual(registro_atualizado.nota, 5)
        self.assertEqual(registro_atualizado.critica, 'Melhor filme de todos os tempos!')
        self.assertEqual(registro_atualizado.pk, self.registro.pk)
    
    def test_usuario_nao_pode_editar_registro_de_outro(self):
        self.client.force_login(user=self.outro_user)
        response = self.client.post(self.url, {'nota': 1})
        # Deve retornar 404 porque o queryset filtra apenas registros do usuário logado
        self.assertEqual(response.status_code, 404)
        
        registro_original = RegistroAssistido.objects.get(pk=self.registro.pk)
        self.assertEqual(registro_original.nota, 3)


class TestesViewExcluirRegistroAssistido(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.outro_user = User.objects.create_user(username='outro', password='12345')
        self.client.force_login(user=self.user)
        
        self.obra = Obra.objects.create(
            titulo="Matrix",
            ano_lancamento=1999,
            genero="Ficção"
        )
        self.registro = RegistroAssistido.objects.create(
            usuario=self.user,
            obra=self.obra,
            nota=4
        )
        self.url = reverse('excluir-registro', kwargs={'pk': self.registro.pk})
    
    def test_get_redireciona(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meus-registros'))
        self.assertEqual(RegistroAssistido.objects.count(), 1)
    
    def test_post_exclui(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('meus-registros'))
        
        self.assertEqual(RegistroAssistido.objects.count(), 0)
    
    def test_usuario_nao_pode_excluir_registro_de_outro(self):
        self.client.force_login(user=self.outro_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 404)
        
        self.assertEqual(RegistroAssistido.objects.count(), 1)


class TestesViewMeusRegistros(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.outro_user = User.objects.create_user(username='outro', password='12345')
        self.client.force_login(user=self.user)
        self.url = reverse('meus-registros')
        
        self.filme = Obra.objects.create(
            titulo="Matrix",
            ano_lancamento=1999,
            genero="Ficção",
            tipo='filme'
        )
        self.serie = Obra.objects.create(
            titulo="Breaking Bad",
            ano_lancamento=2008,
            genero="Drama",
            tipo='serie'
        )
        
        RegistroAssistido.objects.create(usuario=self.user, obra=self.filme, nota=5)
        RegistroAssistido.objects.create(usuario=self.user, obra=self.serie, nota=4)
        
        RegistroAssistido.objects.create(
            usuario=self.outro_user,
            obra=self.filme,
            nota=3
        )
    
    
    def test_listar_apenas_registros_do_usuario(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        registros = response.context.get('registros')
        self.assertEqual(len(registros), 2)
        for registro in registros:
            self.assertEqual(registro.usuario, self.user)
    
    def test_filtrar_por_tipo_filme(self):
        response = self.client.get(self.url, {'tipo': 'filme'})
        self.assertEqual(response.status_code, 200)
        registros = response.context.get('registros')
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0].obra.tipo, 'filme')
    
    def test_filtrar_por_tipo_serie(self):
        response = self.client.get(self.url, {'tipo': 'serie'})
        self.assertEqual(response.status_code, 200)
        registros = response.context.get('registros')
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0].obra.tipo, 'serie')


class TestesViewCadastrarUsuario(TestCase):
    def setUp(self):
        self.url = reverse('cadastrar-usuario')
    
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context.get('form'), FormularioCadastro)
    
    def test_post_cadastro_valido(self):
        data = {
            'first_name': 'João Silva',
            'username': 'joaosilva',
            'password1': 'senhaforte123',
            'password2': 'senhaforte123'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()
        self.assertEqual(user.username, 'joaosilva')
        self.assertEqual(user.first_name, 'João Silva')
        self.assertTrue(user.check_password('senhaforte123'))

