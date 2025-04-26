from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB='mysql+mysqlconnector',
        usuario='root',
        senha='',
        servidor='localhost',
        database='livraria'
    )

# instancia o banco de dados
db = SQLAlchemy(app)

class Usuarios(db.Model): 
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_usuario = db.Column(db.String(80), nullable=False)
    senha_usuario = db.Column(db.Integer, nullable=True)
    email_usuario = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return "<Usuario %r>" % self.nome_usuario


class Livros(db.Model):
    id_livro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_livro = db.Column(db.String(100), nullable=False)
    autor_livro = db.Column(db.String(100), nullable=False)
    ano_livro = db.Column(db.Integer, nullable=True)
    imagem_livro = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return "<Livro %r>" % self.nome_livro

# classe dos cards de livros
class Terror(db.Model):
    id_terror = db.Column(db.Integer, primary_key=True, autoincrement=True)
    titulo_terror = db.Column(db.String(100), nullable=False)
    autor_terror = db.Column(db.String(100), nullable=False)
    capa_terror = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return "<Terror %r>" % self.titulo_terror


@app.route('/terror')
def terror():
    livros_terror = Terror.query.limit(5).all()
    return render_template('terror.html', titulo='Livros de Terror', terror=livros_terror)


# essa linha cria o banco e as tabelas
with app.app_context():
    db.create_all()

    livros_terror = [
        Terror(titulo_terror="It", autor_terror="Stephen King", capa_terror="https://upload.wikimedia.org/wikipedia/pt/8/82/It_2017.jpg"),
        Terror(titulo_terror="O Iluminado", autor_terror="Stephen King", capa_terror="https://www.planocritico.com/wp-content/uploads/2018/10/o_iluminado_1980_plano_critico.jpg"),
        Terror(titulo_terror="A Volta do Parafuso", autor_terror="Henry James", capa_terror="https://m.media-amazon.com/images/I/51AKQKcfIIL._SY445_SX342_.jpg"),
        Terror(titulo_terror="Drácula", autor_terror="Bram Stoker", capa_terror="https://m.media-amazon.com/images/I/61MgodE1s0L._AC_UF1000,1000_QL80_.jpg"),
        Terror(titulo_terror="Frankenstein", autor_terror="Mary Shelley", capa_terror="https://cdl-static.s3-sa-east-1.amazonaws.com/blog/artigo/6739/images/frankenstein-edicao-bolso-de-luxo.jpg"),
    ]
    db.session.bulk_save_objects(livros_terror)
    db.session.commit()




@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', titulo='Página inicial')


@app.route('/listaUsuarios')
def listaUsuarios():
    usuarios_cadastrados = Usuarios.query.order_by(Usuarios.id_usuario)
    return render_template('listaUsuarios.html',
                           titulo='Lista de Usuários', usuarios=usuarios_cadastrados)


@app.route('/cadastro')
def cadastro():
    return render_template('telaCadastro.html', titulo='Cadastro de Usuário')




@app.route('/login')
def login():
    return render_template('telaLogin.html', titulo='Login de Usuário')


generos = ['Fantasia ⚔', 'Romance 🤎', 'Terror 😱', 'Suspense 🦹‍♂️', 'Aventura 🧙‍♂️', 'Ficção Científica 🤖', 'Drama 😭', 'Comédia 🤡']
# rota de cadastro de livros
@app.route('/cadastroLivros')
def cadastroLivros():
    return render_template('cadastrarLivro.html', titulo='Cadastro de Livros'
                           , icone = '📚', generos = generos)


# rota para adicionar um novo usuário
@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = str(request.form['senha'])
        email = request.form['email']

        novo_usuario = Usuarios(nome_usuario=nome, senha_usuario=senha, email_usuario=email)
        db.session.add(novo_usuario)
        db.session.commit()

        
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
