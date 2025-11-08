-- Script SQL para PostgreSQL - Inserir obras no banco de dados WatchBook
-- Execute este script no PostgreSQL

-- Limpar tabela de obras 
-- TRUNCATE TABLE catalogo_obra RESTART IDENTITY CASCADE;

-- Inserir Séries
INSERT INTO catalogo_obra (titulo, ano_lancamento, diretor, genero, tipo, poster) VALUES
('Breaking Bad', 2008, 'Vince Gilligan', 'Drama', 'serie', 'posters/breaking-bad.jpg'),
('Dexter', 2006, 'James Manos Jr.', 'Crime', 'serie', 'posters/dexter.jpg'),
('Dexter: Resurrection', 2025, 'Marcos Siega', 'Crime', 'serie', 'posters/dexter-resurrection.jpg'),
('Mr. Robot', 2015, 'Sam Esmail', 'Thriller', 'serie', 'posters/mr-robot.jpg'),
('The Walking Dead', 2010, 'Frank Darabont', 'Terror', 'serie', 'posters/walking-dead.jpg'),
('Stranger Things', 2016, 'The Duffer Brothers', 'Ficção Científica', 'serie', 'posters/stranger-things.jpg'),
('Game of Thrones', 2011, 'David Benioff e D.B. Weiss', 'Fantasia', 'serie', 'posters/game-of-thrones.jpg'),
('The Boys', 2019, 'Eric Kripke', 'Ação', 'serie', 'posters/the-boys.jpg'),
('Ruptura', 2022, 'Ben Stiller', 'Drama', 'serie', 'posters/ruptura.jpg'),
('Prison Break', 2005, 'Paul Scheuring', 'Ação', 'serie', 'posters/prison-break.jpg'),
('La Casa de Papel', 2017, 'Álex Pina', 'Crime', 'serie', 'posters/la-casa-de-papel.jpg')
ON CONFLICT (titulo) DO NOTHING;

-- Inserir Filmes
INSERT INTO catalogo_obra (titulo, ano_lancamento, diretor, genero, tipo, poster) VALUES
('Vingadores: Ultimato', 2019, 'Anthony e Joe Russo', 'Ação', 'filme', 'posters/vingadores-ultimato.jpg'),
('Homem-Aranha: Sem Volta Para Casa', 2021, 'Jon Watts', 'Ação', 'filme', 'posters/homem-aranha.jpg'),
('Batman: O Cavaleiro das Trevas', 2008, 'Christopher Nolan', 'Ação', 'filme', 'posters/batman.jpg'),
('Matrix', 1999, 'The Wachowskis', 'Ficção Científica', 'filme', 'posters/matrix.jpg'),
('O Senhor dos Anéis: O Retorno do Rei', 2003, 'Peter Jackson', 'Fantasia', 'filme', 'posters/senhor-dos-aneis.jpg'),
('Interestelar', 2014, 'Christopher Nolan', 'Ficção Científica', 'filme', 'posters/interestelar.jpg'),
('Avatar', 2009, 'James Cameron', 'Ficção Científica', 'filme', 'posters/avatar.jpg'),
('Gladiador', 2000, 'Ridley Scott', 'Drama', 'filme', 'posters/gladiador.jpg')
ON CONFLICT (titulo) DO NOTHING;

-- Verificar inserções
SELECT 
    COUNT(*) as total_obras,
    SUM(CASE WHEN tipo = 'filme' THEN 1 ELSE 0 END) as total_filmes,
    SUM(CASE WHEN tipo = 'serie' THEN 1 ELSE 0 END) as total_series
FROM catalogo_obra;

-- Listar todas as obras inseridas
SELECT 
    id, 
    titulo, 
    ano_lancamento, 
    CASE tipo 
        WHEN 'filme' THEN 'Filme' 
        WHEN 'serie' THEN 'Série' 
    END as tipo_display,
    genero,
    diretor
FROM catalogo_obra 
ORDER BY tipo DESC, titulo;
