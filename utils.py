import mysql.connector

def connect_to_database():
    db_host = 'localhost'
    db_user = 'root'
    db_password = ''
    db_name = 'aula_django'

    try:
        connection = mysql.connector.connect(
         host = db_host,
         user = db_user,
         password = db_password,
         database= db_name
        )

        return connection 
    except mysql.connector.Error as e:
        print("Erro ao conectar ao banco de dados: (e)")
        return None   