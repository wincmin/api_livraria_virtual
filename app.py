from flask import Flask,jsonify,render_template,request, redirect,url_for
import mysql.connector
import utils

from usuarios import usuarios_hp
#from livraria import livraria_virtual

app = Flask(__name__)

app.register_blueprint(usuarios_hp)
#app.register_blueprint(livraria_virtual)

@app.route('/sucesso')
def sucesso():
    return "Dados inseridos com sucesso"





if __name__ == '__main__':
    app.run(debug=True)