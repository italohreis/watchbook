from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Obra

class TestesModelObra(TestCase):
    def setUp(self):
        self.obra_filme = Obra.objects.create(
            titulo="Matrix",
            ano_lancamento=1999,
            diretor="Wachowski",
            genero="Ficção Científica",
            tipo='filme'
        )
        
        self.obra_serie = Obra.objects.create(
            titulo="Breaking Bad",
            ano_lancamento=2008,
            diretor="Vince Gilligan",
            genero="Drama",
            tipo='serie'
        )
    
    def test_str(self):
        self.assertEqual(str(self.obra_filme), "Matrix (1999)")
        self.assertEqual(str(self.obra_serie), "Breaking Bad (2008)")

class TestesViewListarObras(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='teste', password='12345')
        self.client.login(username='teste', password='12345')
        self.url = reverse('buscar-obras')
        
        Obra.objects.create(
            titulo="Matrix",
            ano_lancamento=1999,
            genero="Ficção",
            tipo='filme'
        )
        Obra.objects.create(
            titulo="Breaking Bad",
            ano_lancamento=2008,
            genero="Drama",
            tipo='serie'
        )
        Obra.objects.create(
            titulo="Inception",
            ano_lancamento=2010,
            genero="Ficção",
            tipo='filme'
        )
    
    def test_listar_todas_obras(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('lista_obras')), 3)
    
    def test_filtrar_por_tipo_filme(self):
        response = self.client.get(self.url, {'tipo': 'filme'})
        self.assertEqual(response.status_code, 200)
        obras = response.context.get('lista_obras')
        self.assertEqual(len(obras), 2)
        for obra in obras:
            self.assertEqual(obra.tipo, 'filme')
    
    def test_filtrar_por_tipo_serie(self):
        response = self.client.get(self.url, {'tipo': 'serie'})
        self.assertEqual(response.status_code, 200)
        obras = response.context.get('lista_obras')
        self.assertEqual(len(obras), 1)
        self.assertEqual(obras[0].tipo, 'serie')
