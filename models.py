from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuarios(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(100), nullable=False)
    senha_usuario = db.Column(db.String(150), nullable=True)
    email_usuario = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return "<Usuario %r>" % self.nome_usuario

class Livros(db.Model):
    id_livro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_livro = db.Column(db.String(100), nullable=False)
    autor_livro = db.Column(db.String(100), nullable=False)
    genero_livro = db.Column(db.String, nullable=False)
    ano_livro = db.Column(db.Integer, nullable=False)
    descricao_livro = db.Column(db.Text)
    imagem_livro = db.Column(db.String(300), nullable=True)
    favorito = db.Column(db.Boolean, default=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)

    usuario = db.relationship('Usuarios', backref=db.backref('livros', lazy=True))

    def __repr__(self):
        return "<Livro %r>" % self.nome_livro

class Terror(db.Model):
    id_terror = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo_terror = db.Column(db.String(100), nullable=False)
    autor_terror = db.Column(db.String(100), nullable=False)
    capa_terror = db.Column(db.String(250), nullable=True)
    favorito = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Terror %r>" % self.titulo_terror

class Fantasia(db.Model):
    id_fantasia = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo_fantasia = db.Column(db.String(100), nullable=False)
    autor_fantasia = db.Column(db.String(100), nullable=False)
    capa_fantasia = db.Column(db.String(250), nullable=True)
    favorito = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Fantasia %r>" % self.titulo_fantasia



class Romance(db.Model):
    id_romance= db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo_romance = db.Column(db.String(100), nullable=False)
    autor_romance = db.Column(db.String(100), nullable=False)
    capa_romance = db.Column(db.String(250), nullable=True)
    favorito = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return "<Romance %r>" % self.titulo_romance
    

class Ficcao(db.Model):
    id_ficcao= db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo_ficcao = db.Column(db.String(100), nullable=False)
    autor_ficcao = db.Column(db.String(100), nullable=False)
    capa_ficcao = db.Column(db.String(250), nullable=True)
    favorito = db.Column(db.Boolean, default=False)
    def __repr__(self):
        return "<Ficcao %r>" % self.titulo_ficcao
  
