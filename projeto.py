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


with app.app_context():
    db.create_all()


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
