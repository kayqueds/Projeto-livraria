from flask import Flask, render_template, request, redirect, session, flash
from models import db, Usuarios, Livros, Terror, Fantasia  # importa as classes do models.py
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "livraria"

# Configurações do upload
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB='mysql+mysqlconnector',
        usuario='root',
        senha='',
        servidor='localhost',
        database='livraria'
    )

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/terror')
def terror():
    livros_terror = Terror.query.limit(5).all()
    return render_template('terror.html', titulo='Livros de Terror', terror=livros_terror)

@app.route('/fantasia')
def fantasia():
    livros_fantasia = Fantasia.query.limit(3).all()
    return render_template('fantasia.html', titulo='Livros de Fantasia', fantasia=livros_fantasia)

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

    livros_fantasia = [
        Fantasia(titulo_fantasia="O Labirinto do Fauno", autor_fantasia="Guillermo del Toro", capa_fantasia="https://m.media-amazon.com/images/I/51epGsQvSaL._SY445_SX342_.jpg"),
        Fantasia(titulo_fantasia="Viagem ao centro da terra", autor_fantasia="Júlio Verne", capa_fantasia="https://m.media-amazon.com/images/I/71g8eE8d8QL._AC_UF1000,1000_QL80_.jpg"),
        Fantasia(titulo_fantasia="O Nome do Vento", autor_fantasia="Patrick Rothfuss", capa_fantasia="https://m.media-amazon.com/images/I/81yWqSBM+5L._AC_UF1000,1000_QL80_.jpg"),
    ]

    db.session.bulk_save_objects(livros_fantasia)
    db.session.commit()

# rotas da aplicação

# rota inicial
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', titulo='Página inicial')

@app.route('/listaUsuarios')
def listaUsuarios():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
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



# rota de logout
@app.route('/logout') 
def logout():
    session.pop('usuario_logado', None)
    flash('Logout realizado com sucesso!', 'sucesso')
    return redirect('/login')  

# rota de autenticar usuario
@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    email = request.form.get('txtLogin', '').strip()
    senha = request.form.get('txtSenha', '').strip()

    usuario = Usuarios.query.filter_by(email_usuario=email).first()

    if usuario and usuario.senha_usuario == senha:
        session['usuario_logado'] = usuario.email_usuario
        flash('Login realizado com sucesso!', 'sucesso') 
        print('Usuário logado:', session.get('usuario_logado'))
        return redirect('/')
    else:
        flash('Usuário ou senha inválidos', 'erro')
        return redirect('/login')

@app.route('/cadastroLivros', methods=['GET', 'POST'])
def cadastroLivros():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')

    if request.method == 'POST':
        nome_livro = request.form['nome_livro']
        autor_livro = request.form['autor_livro']
        genero_livro = request.form['genero_livro']
        ano_livro = request.form['ano_livro']
        descricao_livro = request.form['descricao_livro']
        imagem_livro = request.files['imagem_livro']

        # Salva a imagem na pasta uploads
        nome_arquivo = secure_filename(imagem_livro.filename)
        caminho_arquivo = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
        imagem_livro.save(caminho_arquivo)

        # Obter o usuário logado
        usuario_logado = session['usuario_logado']
        usuario = Usuarios.query.filter_by(email_usuario=usuario_logado).first()

        # Cria o novo livro associado ao usuário logado
        novo_livro = Livros(
            nome_livro=nome_livro,
            autor_livro=autor_livro,
            genero_livro=genero_livro,
            descricao_livro=descricao_livro,
            ano_livro=int(ano_livro),
            imagem_livro=nome_arquivo,
            usuario_id=usuario.id_usuario
        )

        db.session.add(novo_livro)
        db.session.commit()

        return redirect('/livros')

    return render_template('cadastrarLivro.html', titulo='Cadastro de Livros', icone='📚', generos=generos)


@app.route('/livros')
def listar_livros():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')

    # Obter o usuário logado
    usuario_logado = session['usuario_logado']

    # Buscar apenas os livros cadastrados pelo usuário logado
    livros = Livros.query.filter_by(usuario_id=usuario_logado).all()

    return render_template('livros.html', titulo='Meus Livros', livros=livros)



@app.errorhandler(404)
def paginaNaoExiste(e):
    return render_template('erro.html', titulo="Página não existe")



@app.route('/excluir_livro/<int:id>')  
def excluir_livro(id):
    
   # a linha abaixo exclui o aluno
   Livros.query.filter_by(id_livro = id).delete()

   db.session.commit()
   return redirect('/livros')    



# adicionando rota para editar livro
@app.route('/editar_livro/<int:id>')
def editar_livro(id):
    livro = Livros.query.get_or_404(id)
    return render_template(
        'editarLivro.html',
        titulo='Editar livro',
        icone='✏️',
        livro=livro,
        generos=generos
    )

@app.route('/atualizar_livro', methods=['POST'])
def atualizar_livro():
    livro_id = request.form['id_livro']
    livro = Livros.query.get_or_404(livro_id)

    livro.nome_livro = request.form['nome_livro']
    livro.autor_livro = request.form['autor_livro']
    livro.genero_livro = request.form['genero_livro']
    livro.ano_livro = int(request.form['ano_livro'])
    livro.descricao_livro = request.form['descricao_livro']

    imagem = request.files.get('imagem_livro')
    if imagem and imagem.filename != '':
        nome_arquivo = secure_filename(imagem.filename)
        imagem.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo))
        livro.imagem_livro = nome_arquivo

    db.session.commit()

    return redirect('/livros')

@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        email = request.form['email']

        # Criar o novo usuário no banco de dados
        novo_usuario = Usuarios(nome_usuario=nome, senha_usuario=senha, email_usuario=email)
        db.session.add(novo_usuario)
        db.session.commit()

        # Redirecionar para a tela de login
        return redirect('/login') 

if __name__ == '__main__':
    app.run(debug=True)

