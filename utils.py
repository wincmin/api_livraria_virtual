import mysql.connector

def connect_to_database():
    db_host = 'localhost'
    db_user = 'root'
    db_passaword = ''
    db_name = 'loja_virtual_db'

    try:
        connection = mysql.connector.connect(
         host = db_host,
         user = db_user,
         passaword = db_passaword,
         database= db_name
        )

        return connection 
    except mysql.connector.Error as e:
        print("Erro ao conectar ao banco de dados: (e)")
        return None   