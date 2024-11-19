from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'formulario'

@app.route('/', methods=['GET'])
def inicial():
    return render_template('/index.html')


# Rota para processar o formulário
@app.route('/usuario', methods=['POST'])
def submit_formulario():
    # Obter dados do formulário
    nome = request.form['nome']
    email = request.form['email']
    idade = request.form['idade']
    genero = request.form['genero']
    mensagem = request.form['mensagem']

    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = connection.cursor()

        # Executar comando SQL para inserir dados
        sql = "INSERT INTO usuarios (nome, email, idade, genero, mensagem) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nome, email, idade, genero, mensagem))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return "Erro ao processar os dados. Tente novamente mais tarde."
    finally:
        # Fechar conexão com o banco de dados
        if cursor:
            cursor.close()
        if connection.is_connected():
            connection.close()

    # Redirecionar para página de sucesso ou outra página
    return redirect(url_for('sucesso'))

@app.route('/usuario/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    # Obter os dados do formulário
    dados = request.json  # Assumindo que os dados são enviados em formato JSON

    # Validar os dados
    # ... (implementar a validação aqui)

    # Construir a consulta SQL
    sql = "UPDATE usuarios SET nome=%s, email=%s,genero=%s, idade=%s WHERE id=%s"
    valores = (dados['nome'], dados['email'], dados['idade'], usuario_id)

    # Conectar ao banco de dados e executar a consulta
    try:
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()
            mycursor.execute(sql, valores)
            mydb.commit()
            return jsonify({'mensagem': 'Usuário atualizado com sucesso'}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        # Conectar ao banco de dados
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()

            # Executar a consulta SQL para selecionar todos os usuários
            sql = "SELECT * FROM usuarios"
            mycursor.execute(sql)

            # Obter os resultados da consulta
            resultados = mycursor.fetchall()

            # Formatar os resultados em um JSON
            usuarios = []
            for usuario in resultados:
                usuarios.append({'id': usuario[0], 'nome': usuario[1], 'email': usuario[2],'genero': usuario[3] ,'idade': usuario[4]})

            return jsonify({'usuarios': usuarios}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    

@app.route('/get_usuario/<int:usuario_id>', methods=['GET'])
def get_usuario(usuario_id):

    try:
        # Conectar ao banco de dados
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()

            # Executar a consulta SQL para selecionar todos os usuários
            sql = "SELECT * FROM usuarios where id=%s "
            valores = (usuario_id,)

            mycursor.execute(sql,valores)

            # Obter os resultados da consulta
            resultados = mycursor.fetchall()

            # Formatar os resultados em um JSON
            usuarios = []
            for usuario in resultados:
                usuarios.append({'id': usuario[0], 'nome': usuario[1], 'email': usuario[2], 'idade': usuario[3]})

            return jsonify({'usuario': usuarios[0]}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    
app.route('/get_nome_usuarios', methods=['GET'])
def get_nome_usuarios():
    nome = request.args.get('nome')

    if nome:
        # Construir a consulta SQL com o parâmetro de pesquisa
        sql = "SELECT * FROM usuarios WHERE nome LIKE %s"
        valores = ('%' + nome + '%',)
        try:
            with mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database=db_name
            ) as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                # Formatar os resultados em um JSON
                usuarios = []
                for usuario in resultados:
                    usuarios.append({'id': usuario[0], 'nome': usuario[1], 'email': usuario[2], 'idade': usuario[3]})

                return jsonify({'usuarios': usuarios}), 200
        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
    else:
        return jsonify({'mensagem': 'O parâmetro "nome" é obrigatório'}), 400
    

@app.route('/delete_usuario/<int:usuario_id>',methods=['DELETE'])
def excluir_user(usuario_id):
    try:
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()

            sql = "DELETE FROM usuarios WHERE id = %s"
            valores = (usuario_id,)
            mycursor.execute(sql,valores)
            mydb.commit()
    
            return jsonify({'message': "usuário deletado com sucesso!" }), 200
    except mysql.connector.Error as error:
        print(f"Error deleting user: {error}")
        return jsonify({'error': 'Erro ao deletar usuário ' + f'{error}'}), 500


# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
