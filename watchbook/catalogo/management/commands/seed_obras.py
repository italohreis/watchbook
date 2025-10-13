# catalogo/management/commands/seed_obras.py
from django.core.management.base import BaseCommand
from catalogo.models import Obra

class Command(BaseCommand):
    help = 'Popula o banco de dados com uma lista inicial de obras'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando o seeding de obras...'))

        # Dados do seu protótipo
        obras_mock = [
            {'titulo': 'Interestelar', 'ano_lancamento': 2014, 'diretor': 'Christopher Nolan', 'genero': 'Ficção Científica'},
            {'titulo': 'O Poderoso Chefão', 'ano_lancamento': 1972, 'diretor': 'Francis Ford Coppola', 'genero': 'Crime'},
            {'titulo': 'Parasita', 'ano_lancamento': 2019, 'diretor': 'Bong Joon-ho', 'genero': 'Thriller'},
            {'titulo': 'Breaking Bad', 'ano_lancamento': 2008, 'diretor': 'Vince Gilligan', 'genero': 'Drama'},
            {'titulo': 'Dark', 'ano_lancamento': 2017, 'diretor': 'Baran bo Odar', 'genero': 'Sci-Fi'},
            {'titulo': 'A Origem', 'ano_lancamento': 2010, 'diretor': 'Christopher Nolan', 'genero': 'Ação'},
        ]

        # Limpa a tabela antes de inserir para evitar duplicatas
        Obra.objects.all().delete()
        self.stdout.write(self.style.WARNING('Obras existentes foram deletadas.'))

        for obra_data in obras_mock:
            Obra.objects.create(**obra_data)

        self.stdout.write(self.style.SUCCESS(f'{len(obras_mock)} obras foram criadas com sucesso!'))