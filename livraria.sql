-- CREATE DATABASE livraria;
USE livraria;


CREATE TABLE usuarios(
	id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nome_usuario VARCHAR(100) NOT NULL,
    senha_usuario VARCHAR(150) NOT NULL,
    email_usuario VARCHAR(250) NOT NULL
);

-- DROP TABLE usuarios;

CREATE TABLE livros(
	id_livro INT AUTO_INCREMENT PRIMARY KEY,
	nome_livro VARCHAR (100) NOT NULL,
    autor_livro VARCHAR(100) NOT NULL,
    genero_livro VARCHAR(50) NOT NULL,
	ano_livro INT NOT NULL,
    descricao_livro VARCHAR(500),
    imagem_livro VARCHAR(300),
    favorito BOOLEAN,
    usuario_id INT NOT NULL
);


-- drop table livros;
-- drop table usuarios;
CREATE TABLE terror(
	id_terror INT PRIMARY KEY AUTO_INCREMENT,
    titulo_terror VARCHAR(100) NOT NULL,
    autor_terror VARCHAR(100) NOT NULL,
    capa_terror VARCHAR(250),
    favorito BOOLEAN
);

-- DROP TABLE terror;

CREATE TABLE fantasia(
	id_fantasia INT PRIMARY KEY AUTO_INCREMENT,
    titulo_fantasia VARCHAR(100) NOT NULL,
    autor_fantasia VARCHAR(100) NOT NULL,
    capa_fantasia VARCHAR(250),
    favorito BOOLEAN
);
-- DROP TABLE fantasia;

CREATE TABLE romance(
	id_romance INT PRIMARY KEY AUTO_INCREMENT,
    titulo_romance VARCHAR(100) NOT NULL,
    autor_romance VARCHAR(100) NOT NULL,
    capa_romance VARCHAR(250),
    favorito BOOLEAN
);

-- DROP TABLE romance;

CREATE TABLE ficcao(
	id_ficcao INT PRIMARY KEY AUTO_INCREMENT,
    titulo_ficcao VARCHAR(100) NOT NULL,
    autor_ficcao VARCHAR(100) NOT NULL,
    capa_ficcao VARCHAR(250),
    favorito BOOLEAN
);
    
 -- DROP TABLE ficcao;

SELECT * FROM usuarios;
-- DROP TABLE livros;
DROP TABLE usuarios;


