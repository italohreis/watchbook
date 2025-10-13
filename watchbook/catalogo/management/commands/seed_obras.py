# catalogo/management/commands/seed_obras.py
from django.core.management.base import BaseCommand
from catalogo.models import Obra

class Command(BaseCommand):
    help = 'Popula o banco de dados com uma lista inicial de séries e filmes'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Iniciando o seeding de obras...'))

        obras_mock = [
            # Séries
            {'titulo': 'Breaking Bad', 'ano_lancamento': 2008, 'diretor': 'Vince Gilligan', 'genero': 'Drama', 'tipo': 'serie'},
            {'titulo': 'Dexter', 'ano_lancamento': 2006, 'diretor': 'James Manos Jr.', 'genero': 'Crime', 'tipo': 'serie'},
            {'titulo': 'Mr. Robot', 'ano_lancamento': 2015, 'diretor': 'Sam Esmail', 'genero': 'Thriller', 'tipo': 'serie'},
            {'titulo': 'The Walking Dead', 'ano_lancamento': 2010, 'diretor': 'Frank Darabont', 'genero': 'Terror', 'tipo': 'serie'},
            {'titulo': 'Stranger Things', 'ano_lancamento': 2016, 'diretor': 'The Duffer Brothers', 'genero': 'Ficção Científica', 'tipo': 'serie'},
            {'titulo': 'Game of Thrones', 'ano_lancamento': 2011, 'diretor': 'David Benioff e D.B. Weiss', 'genero': 'Fantasia', 'tipo': 'serie'},
            {'titulo': 'The Boys', 'ano_lancamento': 2019, 'diretor': 'Eric Kripke', 'genero': 'Ação', 'tipo': 'serie'},

            # Filmes
            {'titulo': 'Vingadores: Ultimato', 'ano_lancamento': 2019, 'diretor': 'Anthony e Joe Russo', 'genero': 'Ação', 'tipo': 'filme'},
            {'titulo': 'Homem-Aranha: Sem Volta Para Casa', 'ano_lancamento': 2021, 'diretor': 'Jon Watts', 'genero': 'Ação', 'tipo': 'filme'},
            {'titulo': 'Batman: O Cavaleiro das Trevas', 'ano_lancamento': 2008, 'diretor': 'Christopher Nolan', 'genero': 'Ação', 'tipo': 'filme'},
            {'titulo': 'Matrix', 'ano_lancamento': 1999, 'diretor': 'The Wachowskis', 'genero': 'Ficção Científica', 'tipo': 'filme'},
            {'titulo': 'O Senhor dos Anéis: O Retorno do Rei', 'ano_lancamento': 2003, 'diretor': 'Peter Jackson', 'genero': 'Fantasia', 'tipo': 'filme'},
            {'titulo': 'Interestelar', 'ano_lancamento': 2014, 'diretor': 'Christopher Nolan', 'genero': 'Ficção Científica', 'tipo': 'filme'},
            {'titulo': 'Inception', 'ano_lancamento': 2010, 'diretor': 'Christopher Nolan', 'genero': 'Ação', 'tipo': 'filme'},
            {'titulo': 'Avatar', 'ano_lancamento': 2009, 'diretor': 'James Cameron', 'genero': 'Ficção Científica', 'tipo': 'filme'},
            {'titulo': 'Gladiador', 'ano_lancamento': 2000, 'diretor': 'Ridley Scott', 'genero': 'Drama', 'tipo': 'filme'},
            {'titulo': 'O Poderoso Chefão', 'ano_lancamento': 1972, 'diretor': 'Francis Ford Coppola', 'genero': 'Crime', 'tipo': 'filme'},
        ]

        # Limpa a tabela antes de inserir para evitar duplicatas
        Obra.objects.all().delete()
        self.stdout.write(self.style.WARNING('Obras existentes foram deletadas.'))

        # Insere os dados
        for obra_data in obras_mock:
            Obra.objects.create(**obra_data)

        self.stdout.write(self.style.SUCCESS(f'{len(obras_mock)} obras foram criadas com sucesso!'))