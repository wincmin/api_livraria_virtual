from flask import Flask, jsonify, render_template, request, redirect, url_for
import mysql.connector
import utils

from produtos import produtos_bp

app = Flask(__name__)

app.register_blueprint(produtos_bp)

@app.route('/sucesso')
def sucesso():
    return 'Dados inseridos com sucesso!'


if __name__ == '__main__':
    app.run(debug=True)





