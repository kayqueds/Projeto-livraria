from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from models import db, Usuarios, Livros, Terror, Fantasia, Romance, Ficcao  # importa as classes do models.py
import os
from datetime import date
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
    livros_terror = Terror.query.limit(3).all()
    return render_template('terror.html', titulo='Livros de Terror', terror=livros_terror)

@app.route('/fantasia')
def fantasia():
    livros_fantasia = Fantasia.query.limit(3).all()
    return render_template('fantasia.html', titulo='Livros de Fantasia', fantasia=livros_fantasia)

@app.route('/romance')
def romance():
    livros_romance = Romance.query.limit(3).all()
    return render_template('romance.html', titulo='Livros de Romance', romance=livros_romance)

@app.route('/ficcao')
def ficcao():
    livros_ficcao = Ficcao.query.limit(3).all()
    return render_template('ficcao.html', titulo='Livros de Ficção', ficcao=livros_ficcao)
# Criação das tabelas no banco de dados (caso ainda não existam)
with app.app_context():
    db.create_all()

    livros_terror = [
    Terror(titulo_terror="It", autor_terror="Stephen King",
           capa_terror="https://upload.wikimedia.org/wikipedia/pt/8/82/It_2017.jpg", favorito=False),
    Terror(titulo_terror="O Iluminado", autor_terror="Stephen King",
           capa_terror="https://www.planocritico.com/wp-content/uploads/2018/10/o_iluminado_1980_plano_critico.jpg", favorito=False),
    Terror(titulo_terror="A Volta do Parafuso", autor_terror="Henry James",
           capa_terror="https://m.media-amazon.com/images/I/51AKQKcfIIL._SY445_SX342_.jpg", favorito=False),
]
    db.session.bulk_save_objects(livros_terror)
    db.session.commit()

    livros_fantasia = [
        Fantasia(titulo_fantasia="O Labirinto do Fauno", autor_fantasia="Guillermo del Toro", capa_fantasia="https://th.bing.com/th/id/R.55947da1b2396a1f9a5619b421b0c01a?rik=SSWAZu%2bz5E8lcA&pid=ImgRaw&r=0", favorito=False),
        Fantasia(titulo_fantasia="O Senhor dos Anéis", autor_fantasia="J.R.R. Tolkien", capa_fantasia="https://m.media-amazon.com/images/I/71+4uDgt8JL._AC_UF1000,1000_QL80_.jpg", favorito=False),
        Fantasia(titulo_fantasia="Harry Potter e a Pedra Filosofal", autor_fantasia="J.K. Rowling", capa_fantasia="https://m.media-amazon.com/images/I/51UoqRAxwEL.jpg", favorito=False),
    ]
    db.session.bulk_save_objects(livros_fantasia)
    db.session.commit()

    livros_romance = [
        Romance(titulo_romance=" A cinco passos de você", autor_romance= "Lippincott Rachael", capa_romance="https://a-static.mlcdn.com.br/1500x1500/livro-a-cinco-passos-de-voce-rachael-lippincott/cliquebooks/566487-1/95de66714818c058f07977e70c8d71e1.jpeg", favorito=False),
        Romance(titulo_romance="É assim que acaba", autor_romance="Colleen Houver", capa_romance="https://m.media-amazon.com/images/I/9112cWOV-OL._UF894,1000_QL80_.jpg", favorito=False),
        Romance(titulo_romance="Até o verão terminar", autor_romance="Collen Houver", capa_romance="https://images.thalia.media/-/BF750-750/d9e5962e334d4dada918c1e1067e652d/ate-o-verao-terminar-epub-3-colleen-hoover.jpeg", favorito=False),
    ]
    db.session.bulk_save_objects(livros_romance)
    db.session.commit()

    livros_ficcao= [
        Ficcao(titulo_ficcao="Fahrenheit 451", autor_ficcao="Ray Braobury", capa_ficcao="https://livrariapublica.com.br/capa/fahrenheit-451-edicao-especial-ray-bradbury-pdf-B08J9GHH12.webp"),
        Ficcao(titulo_ficcao="Mickey 7", autor_ficcao="Edward Ashton", capa_ficcao="https://upload.wikimedia.org/wikipedia/en/c/cc/Mickey7_book_cover.jpg"),
        Ficcao(titulo_ficcao="A guerra dos mundos", autor_ficcao="H. G. Wells", capa_ficcao="https://th.bing.com/th/id/OIP.MT9pZnpQt-7FI-BMGovgqAHaLa?cb=iwc2&rs=1&pid=ImgDetMain"),
    ]

    db.session.bulk_save_objects(livros_ficcao)
    db.session.commit()

# Rotas da aplicação
agora = date.today()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html', titulo='Página inicial', ano=agora.year)

@app.route('/listaUsuarios')
def listaUsuarios():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')
    usuarios_cadastrados = Usuarios.query.order_by(Usuarios.id_usuario)
    return render_template('listaUsuarios.html', titulo='Lista de Usuários', usuarios=usuarios_cadastrados)

@app.route('/cadastro')
def cadastro():
    return render_template('telaCadastro.html', titulo='Cadastro de Usuário')


@app.route('/login')
def login():
    return render_template('telaLogin.html', titulo='Login de Usuário')

generos = ['Fantasia ⚔', 'Romance 🤎', 'Terror 😱', 'Suspense 🦹‍♂️', 'Aventura 🧙‍♂️', 'Ficção Científica 🤖', 'Drama 😭', 'Comédia 🤡']

# Rota de logout
@app.route('/logout') 
def logout():
    session.pop('usuario_logado', None)
    return redirect('/login')  

# Rota de autenticar usuario
@app.route('/autenticar', methods=['POST'])
def autenticar_usuario():
    email = request.form.get('txtLogin', '').strip()
    senha = request.form.get('txtSenha', '').strip()
    usuario = Usuarios.query.filter_by(email_usuario=email).first()
    if usuario and usuario.senha_usuario == senha:
        session['usuario_logado'] = usuario.email_usuario
        flash(f'Login realizado com sucesso, olá {usuario.nome_usuario}', 'success')
        return redirect('/')
    else:
        flash('Usuário ou senha inválidos', 'alert')
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

# baixando livros na tela de favoritos
@app.route('/baixar/<path:titulo>')
def baixar_livro(titulo):
    nome_arquivo = secure_filename(f"{titulo.lower().replace(' ', '_')}.pdf")
    pasta_livros = os.path.join(app.root_path, 'static', 'livros')
    return send_from_directory(pasta_livros, nome_arquivo, as_attachment=True)


@app.route('/livros')
def listar_livros():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')

    # Obter o usuário logado
    usuario_logado = session['usuario_logado']
    usuario = Usuarios.query.filter_by(email_usuario=usuario_logado).first()

    # Buscar apenas os livros cadastrados pelo usuário logado
    livros = Livros.query.filter_by(usuario_id=usuario.id_usuario).all()

    return render_template('livros.html', titulo='Meus Livros', livros=livros)

@app.route('/excluir_livro/<int:id>')  
def excluir_livro(id):
   # Exclui o livro
   Livros.query.filter_by(id_livro=id).delete()
   db.session.commit()
   return redirect('/livros')    

@app.route('/favoritos')
def favoritos():
    if 'usuario_logado' not in session or session['usuario_logado'] is None:
        return redirect('/login')

    livros_terror = Terror.query.filter_by(favorito=True).all()
    livros_fantasia = Fantasia.query.filter_by(favorito=True).all()
    livros_romance = Romance.query.filter_by(favorito=True).all()
    livros_ficcao = Ficcao.query.filter_by(favorito=True).all()
    return render_template("favorito.html", terror=livros_terror, titulo='Livros Favoritos', icone='❤️'
    , fantasia=livros_fantasia, romance=livros_romance, ficcao=livros_ficcao)

@app.route('/favoritar_terror/<int:id>', methods=['POST'])
def favoritar_terror(id):
    livro = Terror.query.get_or_404(id)
    livro.favorito = not livro.favorito
    db.session.commit()
    print(f'Livro {livro.titulo_terror} - favorito: {livro.favorito}')  # debug
    return redirect(url_for('terror'))



@app.route('/favoritar_fantasia/<int:id>', methods=['POST'])
def favoritar_fantasia(id):
    livro = Fantasia.query.get_or_404(id)
    livro.favorito = not livro.favorito
    db.session.commit()
    print(f'Livro {livro.titulo_fantasia} - favorito: {livro.favorito}')
     # debug    
    return redirect(url_for('fantasia'))

@app.route('/favoritar_romance/<int:id>', methods=['POST'])
def favoritar_romance(id):
    livro = Romance.query.get_or_404(id)
    livro.favorito = not livro.favorito
    db.session.commit()
    print(f'Livro {livro.titulo_romance} - favorito: {livro.favorito}')
    return redirect(url_for('romance'))

@app.route('/favoritar_ficcao/<int:id>', methods=['POST'])
def favoritar_ficcao(id):
    livro = Ficcao.query.get_or_404(id)
    livro.favorito = not livro.favorito
    db.session.commit()
    print(f'Livro {livro.titulo_ficcao} - favorito: {livro.favorito}')
    return redirect(url_for('ficcao'))


@app.route('/editar_livro/<int:id>')
def editar_livro(id):
    livro = Livros.query.get_or_404(id)
    return render_template('editarLivro.html', titulo='Editar livro', icone='✏️', livro=livro, generos=generos)
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('erro.html', titulo='Página não encontrada')


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
