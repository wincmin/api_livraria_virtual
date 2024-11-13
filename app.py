from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db_host = 'localhost'
db_user = 'root'
db_password = ''
db_name = 'livraria_virtual'

# Rota para processar o formulário
@app.route('/livros', methods=['PUT'])
def submit_formulario():
    # Obter dados do formulário
    id = request.form['id']
    nome = request.form['nome']
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
        sql = sql = """UPDATE usuarios
        SET
            nome = CASE WHEN %s IS NOT NULL THEN %s ELSE nome END,
            email = CASE WHEN %s IS NOT NULL THEN %s ELSE email END,
            idade = CASE WHEN %s IS NOT NULL THEN %s ELSE idade END,
            genero = CASE WHEN %s IS NOT NULL THEN %s ELSE genero END,
            mensagem = CASE WHEN %s IS NOT NULL THEN %s ELSE mensagem END
        WHERE id = %s
"""
        params = (id, nome, genero, sinopse)
        mycursor.execute(sql, params)
        cursor.execute(sql, (nome, genero, sinopse))
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

# Rota para página de sucesso
@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)


