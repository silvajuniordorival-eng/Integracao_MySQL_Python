#import do flask para criação do servidor
#reder_template para criar uma "ponte" com html
#request para capturar os dados digitados
from flask import Flask,render_template,request, url_for,redirect
import mysql.connector

#"ajuda" o Flask a localizar os caminhos dos arquivos
app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'escola',
    'database': 'cadastro'
}


@app.route('/')
def index():
    try:
        #
        conectar = mysql.connector.connect(**db_config)
        cursor = conectar.cursor(dictionary=True)

        #seleção de tabela
        cursor.execute("SELECT CPF,PRIMEIRO_NOME,SOBRENOME,IDADE FROM cliente")
        lista_clientes = cursor.fetchall()

        return render_template('index.html', clientes = lista_clientes)
    
    except mysql.connector.Error as erro:
        return f"Erro ao carregar a Tabela: {erro}"

#criem uma rota para acessar o formulario
@app.route('/cadastrar', methods=['POST'])
def form_cadastro():
    #bloco para armazenar os dados digitados
    CPF = request.form['cpf']
    primeiro_nome = request.form['primeiro_nome']
    sobrenome = request.form['sobrenome']
    idade = request.form['idade']

    try:
        #verificando conexão com Mysql
        conectar = mysql.connector.connect(**db_config)
        cursor = conectar.cursor()
        query = "INSERT INTO cliente(CPF,PRIMEIRO_NOME,SOBRENOME,IDADE) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(CPF,primeiro_nome,sobrenome,idade))

        #atualiza as alterações e fecha as conexões
        conectar.commit()
        cursor.close()
        conectar.close()

        return f"<h3> Cliente {primeiro_nome} salvo com sucesso!</h3> <a href='/'>Voltar</a>"
    except mysql.connector.Error as erro:
        return f"Erro ao gravar no banco: {erro}"

@app.route('/excluir<CPF>')
def excluir(CPF):
    try:
        conectar = mysql.connector.connector(**db_config)
        cursor = conectar.cursor()

        cursor.execute("DELETE FROM  cliente where CPF = %s", [CPF])

        conectar.commit()
        cursor.close()
        conectar.close()

        return redirect(url_for('index'))
    except mysql.connector.error as erro:
        return f"Erro ao excluir:{erro}"
 



if __name__ == '__main__':
    app.run(debug=True) 