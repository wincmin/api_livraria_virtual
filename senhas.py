om flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector
import utils

senhas_bp = Blueprint('senhas_bp',__name__)


@senhas_bp.route('/cria_senha/<int:usuario_id>', methods=['PUT'])
def cria_senha(usuario_id):


    try:
        # Connect to the database using a context manager (recommended)
        con = utils.connect_to_database()  # Assuming you have a function to get a valid connection
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            # Print the constructed SQL query for debugging
            sql = "INSERT INTO senhas (id_usuario) VALUES (%s)"
            valores = (usuario_id,)
            print(f"SQL Query: {sql}")
            mycursor.execute(sql, valores)
            mydb.commit()

        return jsonify({'mensagem': 'Senha cadastrada com sucesso!'}), 201


    except mysql.connector.Error as error:
        print(f"Failed to insert record: {error}")
        return "Ocorreu um erro ao inserir os dados.", 500