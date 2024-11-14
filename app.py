from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'livraria_virtual'

@app.route('/livro', methods=['POST'])
def submit_formulario():
    # Obter dados do formulário
    titulo = request.form['titulo']
    genero = request.form['genero']
    sinopse = request.form['sinopse']


    try:
        # Conectar ao banco de dados
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            charset= 'utf8'
        )
        cursor = connection.cursor()

        # Executar comando SQL para inserir dados
        sql = "INSERT INTO livros (titulo, genero, sinopse) VALUES (%s, %s, %s)"
        cursor.execute(sql, (titulo, genero, sinopse))
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

@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'



@app.route('/livro/<int:livro_id>', methods=['PUT'])
def atualizar_livro(livro_id):
    # Obter os dados do formulário
    dados = request.json  # Assumindo que os dados são enviados em formato JSON

    # Validar os dados
    # ... (implementar a validação aqui)

    # Construir a consulta SQL
    sql = "UPDATE livros SET titulo=%s, genero=%s, sinopse=%s WHERE id=%s"
    valores = (dados['titulo'], dados['genero'], dados['sinopse'], livro_id)

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
    

@app.route('/livros', methods=['GET'])
def listar_livros():
    try:
        # Conectar ao banco de dados
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()

            # Executar a consulta SQL para selecionar todos os usuários
            sql = "SELECT * FROM livros"
            mycursor.execute(sql)

            # Obter os resultados da consulta
            resultados = mycursor.fetchall()

            # Formatar os resultados em um JSON
            livros = []
            for livro in resultados:
                livros.append({'id': livro[0], 'titulo': livro[1], 'genero': livro[2], 'sinopse': livro[3]})

            return jsonify({'livros': livros}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500

@app.route('/get_livro/<int:livro_id>', methods=['GET'])
def get_livro(livro_id):

    try:
        # Conectar ao banco de dados
        with mysql.connector.connect(
            host=db_host, user=db_user, password=db_password, database=db_name
        ) as mydb:
            mycursor = mydb.cursor()

            # Executar a consulta SQL para selecionar todos os usuários
            sql = "SELECT * FROM livros where id=%s "
            valores = (livro_id,)

            mycursor.execute(sql,valores)

            # Obter os resultados da consulta
            resultados = mycursor.fetchall()

            # Formatar os resultados em um JSON
            livros = []
            for livro in resultados:
                livros.append({'id': livro[0], 'titulo': livro[1], 'genero': livro[2], 'sinopse': livro[3]})

            return jsonify({'livro': livros[0]}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    
@app.route('/get_titulo_livro', methods=['GET'])
def get_titulo_livro():
    titulo = request.args.get('titulo')

    if titulo:
        # Construir a consulta SQL com o parâmetro de pesquisa
        sql = "SELECT * FROM livros WHERE titulo LIKE %s"
        valores = ('%' + titulo + '%',)
        try:
            with mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database=db_name
            ) as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                # Formatar os resultados em um JSON
                livros = []
                for livro in resultados:
                    livros.append({'id': livro[0], 'titulo': livro[1], 'genero': livro[2], 'sinopse': livro[3]})

                return jsonify({'livros': livros}), 200
        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
    else:
        return jsonify({'mensagem': 'O parâmetro "titulo" é obrigatório'}), 400
    
@app.route('/get_genero_livro', methods=['GET'])
def get_genero_livro():
    genero = request.args.get('genero')

    if genero:
        # Construir a consulta SQL com o parâmetro de pesquisa
        sql = "SELECT * FROM livros WHERE genero LIKE %s"
        valores = ('%' + genero + '%',)
        try:
            with mysql.connector.connect(
                host=db_host, user=db_user, password=db_password, database=db_name
            ) as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                # Formatar os resultados em um JSON
                livros = []
                for livro in resultados:
                    livros.append({'id': livro[0], 'titulo': livro[1], 'genero': livro[2], 'sinopse': livro[3]})

                return jsonify({'livros': livros}), 200
        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
    else:
        return jsonify({'mensagem': 'O parâmetro "titulo" é obrigatório'}), 400




if __name__ == '__main__':
    app.run(debug=True)





