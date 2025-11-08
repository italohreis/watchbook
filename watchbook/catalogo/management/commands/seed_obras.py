from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from pathlib import Path
from catalogo.models import Obra

obras = [
     # Séries
    {'titulo': 'Breaking Bad', 'ano_lancamento': 2008, 'diretor': 'Vince Gilligan', 'genero': 'Drama', 'tipo': 'serie', 'poster_nome': 'breaking-bad.jpg'},
    {'titulo': 'Dexter', 'ano_lancamento': 2006, 'diretor': 'James Manos Jr.', 'genero': 'Crime', 'tipo': 'serie', 'poster_nome': 'dexter.jpg'},
    {'titulo': 'Dexter: Resurrection', 'ano_lancamento': 2025, 'diretor': 'Marcos Siega', 'genero': 'Crime', 'tipo': 'serie', 'poster_nome': 'dexter-resurrection.jpg'},
    {'titulo': 'Mr. Robot', 'ano_lancamento': 2015, 'diretor': 'Sam Esmail', 'genero': 'Thriller', 'tipo': 'serie', 'poster_nome': 'mr-robot.jpg'},
    {'titulo': 'The Walking Dead', 'ano_lancamento': 2010, 'diretor': 'Frank Darabont', 'genero': 'Terror', 'tipo': 'serie', 'poster_nome': 'walking-dead.jpg'},
    {'titulo': 'Stranger Things', 'ano_lancamento': 2016, 'diretor': 'The Duffer Brothers', 'genero': 'Ficção Científica', 'tipo': 'serie', 'poster_nome': 'stranger-things.jpg'},
    {'titulo': 'Game of Thrones', 'ano_lancamento': 2011, 'diretor': 'David Benioff e D.B. Weiss', 'genero': 'Fantasia', 'tipo': 'serie', 'poster_nome': 'game-of-thrones.jpg'},
    {'titulo': 'The Boys', 'ano_lancamento': 2019, 'diretor': 'Eric Kripke', 'genero': 'Ação', 'tipo': 'serie', 'poster_nome': 'the-boys.jpg'},
    {'titulo': 'Ruptura', 'ano_lancamento': 2022, 'diretor': 'Ben Stiller', 'genero': 'Drama', 'tipo': 'serie', 'poster_nome': 'ruptura.jpg'},
    {'titulo': 'Prison Break', 'ano_lancamento': 2005, 'diretor': 'Paul Scheuring', 'genero': 'Ação', 'tipo': 'serie', 'poster_nome': 'prison-break.jpg'},
    {'titulo': 'La Casa de Papel', 'ano_lancamento': 2017, 'diretor': 'Álex Pina', 'genero': 'Crime', 'tipo': 'serie', 'poster_nome': 'la-casa-de-papel.jpg'},

    # Filmes
    {'titulo': 'Vingadores: Ultimato', 'ano_lancamento': 2019, 'diretor': 'Anthony e Joe Russo', 'genero': 'Ação', 'tipo': 'filme', 'poster_nome': 'vingadores-ultimato.jpg'},
    {'titulo': 'Homem-Aranha: Sem Volta Para Casa', 'ano_lancamento': 2021, 'diretor': 'Jon Watts', 'genero': 'Ação', 'tipo': 'filme', 'poster_nome': 'homem-aranha.jpg'},
    {'titulo': 'Batman: O Cavaleiro das Trevas', 'ano_lancamento': 2008, 'diretor': 'Christopher Nolan', 'genero': 'Ação', 'tipo': 'filme', 'poster_nome': 'batman.jpg'},
    {'titulo': 'Matrix', 'ano_lancamento': 1999, 'diretor': 'The Wachowskis', 'genero': 'Ficção Científica', 'tipo': 'filme', 'poster_nome': 'matrix.jpg'},
    {'titulo': 'O Senhor dos Anéis: O Retorno do Rei', 'ano_lancamento': 2003, 'diretor': 'Peter Jackson', 'genero': 'Fantasia', 'tipo': 'filme', 'poster_nome': 'senhor-dos-aneis.jpg'},
    {'titulo': 'Interestelar', 'ano_lancamento': 2014, 'diretor': 'Christopher Nolan', 'genero': 'Ficção Científica', 'tipo': 'filme', 'poster_nome': 'interestelar.jpg'},
    {'titulo': 'Avatar', 'ano_lancamento': 2009, 'diretor': 'James Cameron', 'genero': 'Ficção Científica', 'tipo': 'filme', 'poster_nome': 'avatar.jpg'},
    {'titulo': 'Gladiador', 'ano_lancamento': 2000, 'diretor': 'Ridley Scott', 'genero': 'Drama', 'tipo': 'filme', 'poster_nome': 'gladiador.jpg'},
]


class Command(BaseCommand):
    help = 'Popula o banco de dados com uma lista inicial de obras (filmes e séries).'

    def handle(self, *args, **options):
        # --- Limpeza dos arquivos de poster antigos ---
        poster_folder = settings.MEDIA_ROOT / 'posters'
        if poster_folder.exists():
            # Lista de nomes de arquivo que devem existir
            canonical_filenames = {obra.get("poster_nome") for obra in obras if obra.get("poster_nome")}
            
            for item in poster_folder.iterdir():
                if item.is_file() and item.name not in canonical_filenames:
                    self.stdout.write(self.style.WARNING(f'Deletando arquivo de poster antigo: {item.name}'))
                    item.unlink() 

        # Deleta todas as obras existentes para evitar duplicatas
        Obra.objects.all().delete()
        self.stdout.write(self.style.WARNING('Obras existentes foram deletadas.'))

        created_count = 0
        for obra_data in obras:
            filename = obra_data.get("poster_nome")
            
            # Primeiro, cria a obra no banco de dados
            obra, created = Obra.objects.get_or_create(
                titulo=obra_data["titulo"],
                defaults={
                    'tipo': obra_data["tipo"],
                    'ano_lancamento': obra_data.get("ano_lancamento"),
                    'genero': obra_data.get("genero", ""),
                    'diretor': obra_data.get("diretor", ""),
                }
            )

            if not created:
                self.stdout.write(self.style.WARNING(f'✓ {obra.titulo} - já existia.'))
                continue

            if not filename:
                self.stdout.write(self.style.WARNING(f'✓ {obra_data["titulo"]} - criada sem poster (não especificado)'))
                created_count += 1
                continue

            poster_path = poster_folder / filename
            
            if poster_path.exists():
                relative_path = Path('posters') / filename
                obra.poster.name = str(relative_path)
                obra.save()
                self.stdout.write(self.style.SUCCESS(f'✓ {obra.titulo} - criada e poster associado!'))
                created_count += 1
            else:
                self.stdout.write(self.style.ERROR(f'✗ {obra_data["titulo"]} - sem poster (arquivo não encontrado em {poster_path})'))
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n{created_count} obras foram criadas!'))
