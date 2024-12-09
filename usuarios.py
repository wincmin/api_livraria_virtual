from flask import Blueprint, Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector
from utils import connect_to_database

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/usuario', methods=['POST'])
def submit_formulario():
    nome = request.form['nome']
    email = request.form['email']
    idade = request.form['idade']
    genero = request.form['genero']
    mensagem = request.form['mensagem']

    try:
        connection = connect_to_database()
        if connection is None:
            return "Erro ao conectar ao banco de dados."

        cursor = connection.cursor()
        sql = "INSERT INTO usuarios (nome, email, idade, genero, mensagem) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nome, email, idade, genero, mensagem))
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Erro ao processar os dados: {err}")
        return "Erro ao processar os dados. Tente novamente mais tarde."
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

    return redirect(url_for('sucesso'))


@usuarios_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        connection = connect_to_database()
        if connection is None:
            return jsonify({'error': 'Erro ao conectar ao banco de dados.'}), 500

        cursor = connection.cursor()
        sql = "SELECT * FROM usuarios"
        cursor.execute(sql)
        resultados = cursor.fetchall()

        usuarios = [{'id': u[0], 'nome': u[1], 'email': u[2], 'genero': u[3], 'idade': u[4]} for u in resultados]
        return jsonify({'usuarios': usuarios}), 200
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
