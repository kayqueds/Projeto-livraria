from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


# configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = \
    '{SGDB}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGDB = 'mysql+mysqlconnector',
        usuario = 'root',
        # senha = ''
        senha = 'toor',
        servidor = 'localhost',
        database = 'prj_cadastro'
    )


# a linha abaixo instancia o banco de dados
db = SQLAlchemy(app)




@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Aqui você pode processar os dados do formulário, se necessário
    
        nome = request.form.get('nome')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        
        return f"Nome: {nome}, Email: {email}, CPF {cpf}"

    # Renderiza a página inicial    

    return render_template('index.html', titulo = 'Página inicial')


@app.route('/cadastro')
def cadastro():
    return render_template('telaCadastro.html', titulo = 'Cadastro de Usuário')



if __name__ == '__main__':
    app.run(debug=True)