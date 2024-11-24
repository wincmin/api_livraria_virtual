from flask import Blueprint, Flask, app, jsonify, render_template, request, redirect, url_for
import mysql.connector
import utils
produtos_bp = Blueprint('/register_produtos', methods=['POST'])

@produtos_bp.route('/produto', methods=['POST'])
def criar_produtos():

    categoria = request.form('categoria')
    cor = request.form('cor')
    qntd = request.form('qntd', type=int) 
    nome_produto = request.form('nome_produto')
    preco = request.form('preco', type=float) 
    imagem = request.form('imagem')
    descricao = request.form('descricao')
    autor = request.form('autor')
    ano_lancamento = request.form('ano_lancamento', type=int)
    genero = request.form('genero')
    marca = request.form('marca')

    try:
        con = utils.connect_to_database()  
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

        sql = """
            INSERT INTO produtos 
            (categoria, cor, qntd, nome_produto, preco, imagem, descricao, autor, ano_lancamento, genero, marca)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        print(f"SLQ Query: {sql}")

        mycursor.execute(sql, (categoria, cor, qntd, nome_produto, preco, imagem, descricao, autor, ano_lancamento, genero, marca))
    
        return redirect(url_for('sucesso'))

    except mysql.connector.Error as error:
        print(f"Failed to insert record: {error}")
        return "Ocorreu um erro ao inserir os dados.", 500


@produtos_bp.route('/produto/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    dados = request.form

    sql = """
            UPDATE produtos 
            SET 
                categoria=%s, 
                cor=%s, 
                qntd=%s, 
                nome_produto=%s, 
                preco=%s, 
                imagem=%s, 
                descricao=%s, 
                autor=%s, 
                ano_lancamento=%s, 
                genero=%s, 
                marca=%s
            WHERE id=%s
        """
    valores = (
            dados['categoria'], 
            dados['cor'], 
            dados['qntd'], 
            dados['nome_produto'], 
            dados['preco'], 
            dados['imagem'], 
            dados['descricao'], 
            dados['autor'], 
            dados['ano_lancamento'], 
            dados['genero'], 
            dados['marca'], 
            produto_id
        )

    try:
        con = utils.connect_to_database()  
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()
            mycursor = mydb.cursor()
            mycursor.execute(sql, valores)
            mydb.commit()
            
        return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    

@app.route('/produto', methods=['GET'])
def listar_produtos():
    try:

        con = utils.connect_to_database() 
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            sql = "SELECT * FROM produtos"
            mycursor.execute(sql)

            resultados = mycursor.fetchall()

            produtos = []
            for produto in resultados:
                produtos.append({
                    'id': produto[0],
                    'categoria': produto[1],
                    'cor': produto[2],
                    'qntd': produto[3],
                    'nome_produto': produto[4],
                    'preco': produto[5],
                    'imagem': produto[6],
                    'descricao': produto[7],
                    'autor': produto[8],
                    'ano_lancamento': produto[9],
                    'genero': produto[10],
                    'marca': produto[11]
                })

            return jsonify({'produtos': produtos}), 500
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500

@app.route('/get_produto/<int:produto_id>', methods=['GET'])
def get_produto(produto_id):

 
    try:
        con = utils.connect_to_database() 
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            sql = "SELECT * FROM produtos where id=%s "
            valores = (produto_id,)

            mycursor.execute(sql,valores)
            resultados = mycursor.fetchall()

            produtos = []
            for produto in resultados:
                produtos.append({
                    'id': produto[0],
                    'categoria': produto[1],
                    'cor': produto[2],
                    'qntd': produto[3],
                    'nome_produto': produto[4],
                    'preco': produto[5],
                    'imagem': produto[6],
                    'descricao': produto[7],
                    'autor': produto[8],
                    'ano_lancamento': produto[9],
                    'genero': produto[10],
                    'marca': produto[11]
                })
            return jsonify({'produto': produto[0]}), 500
    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500
    
@produtos_bp.route('/get_nome_produtos', methods=['GET'])
def buscar_nome_produtos():
    nome = request.args.get('nome')

    if nome:

        sql = "SELECT * FROM produtos WHERE nome_produto LIKE %s"
        valores = ('%' + nome + '%',)

        try:
            con = utils.connect_to_database()
            if not con:
                return jsonify({'error': 'Failed to connect to database'}), 500

            with con as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                produtos = []
                for produto in resultados:
                    produtos.append({
                        'id': produto[0],
                        'categoria': produto[1],
                        'cor': produto[2],
                        'qntd': produto[3],
                        'nome_produto': produto[4],
                        'preco': float(produto[5]),
                        'imagem': produto[6],
                        'descricao': produto[7],
                        'autor': produto[8],
                        'ano_lancamento': produto[9],
                        'genero': produto[10],
                        'marca': produto[11]
                    })

                return jsonify({'produtos': produtos}), 500

        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
    else:
        return jsonify({'mensagem: O parâmetro "nome" é obrigatório'}), 400


@produtos_bp.route('/get_categoria_produtos', methods=['GET'])
def buscar_categoria_produtos():
    categoria = request.args.get('categoria')

    if categoria:

        sql = "SELECT * FROM produtos WHERE categoria LIKE %s"
        valores = ('%' + categoria + '%',)

        try:
            con = utils.connect_to_database()
            if not con:
                return jsonify({'error': 'Failed to connect to database'}), 500
            with con as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                produtos = []
                for produto in resultados:
                    produtos.append({
                        'id': produto[0],
                        'categoria': produto[1],
                        'cor': produto[2],
                        'qntd': produto[3],
                        'nome_produto': produto[4],
                        'preco': float(produto[5]),
                        'imagem': produto[6],
                        'descricao': produto[7],
                        'autor': produto[8],
                        'ano_lancamento': produto[9],
                        'genero': produto[10],
                        'marca': produto[11]
                    })

                return jsonify({'produtos': produtos}), 500

        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500

    else:
        return jsonify({'mensagem': 'O parâmetro "nome" é obrigatório'}), 400

@produtos_bp.route('/get_marca_produtos', methods=['GET'])
def buscar_marca_produtos():
    marca = request.args.get('marca')

    if marca:

       sql = "SELECT * FROM produtos WHERE marca LIKE %s"
       valores = ('%' + marca + '%',)

       try:
            con = utils.connect_to_database()
            if not con:
                return jsonify({'error': 'Failed to connect to database'}), 500
            with con as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                produtos = []
                for produto in resultados:
                    produtos.append({
                        'id': produto[0],
                        'categoria': produto[1],
                        'cor': produto[2],
                        'qntd': produto[3],
                        'nome_produto': produto[4],
                        'preco': float(produto[5]),
                        'imagem': produto[6],
                        'descricao': produto[7],
                        'autor': produto[8],
                        'ano_lancamento': produto[9],
                        'genero': produto[10],
                        'marca': produto[11]
                    })

                return jsonify({'produtos': produtos}), 500

       except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
    else:
        return jsonify({'mensagem': 'O parâmetro "nome" é obrigatório'}), 400

@produtos_bp.route('/get_genero_produtos', methods=['GET'])
def buscar_genero_produto():
    genero = request.args.get('genero')

    if genero:

        sql = "SELECT * FROM produtos WHERE genero LIKE %s"
        valores = ('%' + genero + '%',)

        try:
            con = utils.connect_to_database()
            if not con:
                return jsonify({'error': 'Failed to connect to database'}), 500
            with con as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                produtos = []
                for produto in resultados:
                    produtos.append({
                        'id': produto[0],
                        'categoria': produto[1],
                        'cor': produto[2],
                        'qntd': produto[3],
                        'nome_produto': produto[4],
                        'preco': float(produto[5]),
                        'imagem': produto[6],
                        'descricao': produto[7],
                        'autor': produto[8],
                        'ano_lancamento': produto[9],
                        'genero': produto[10],
                        'marca': produto[11]
                    })

                return jsonify({'produtos': produtos}), 500

        except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
    else:
        return jsonify({'mensagem': 'O parâmetro "nome" é obrigatório'}), 400

@produtos_bp.route('/get_preco_produtos', methods=['GET'])
def buscar_preco_produtos():
    min_preco = request.args.get('min_preco')
    max_preco = request.args.get('max_preco')

    if not min_preco or not max_preco:
        return jsonify({'mensagem': 'Os parâmetros "min_preco" e "max_preco" são obrigatórios'}), 400

    try:
        min_preco = float(min_preco)
        max_preco = float(max_preco)
    except ValueError:
        return jsonify({'mensagem': 'Os valores de "min_preco" e "max_preco" devem ser numéricos'}), 400

    sql = "SELECT * FROM produtos WHERE preco BETWEEN %s AND %s"
    valores = (min_preco, max_preco)

    try:
            con = utils.connect_to_database()
            if not con:
                return jsonify({'error': 'Failed to connect to database'}), 500
            with con as mydb:
                mycursor = mydb.cursor()
                mycursor.execute(sql, valores)
                resultados = mycursor.fetchall()

                produtos = []
                for produto in resultados:
                    produtos.append({
                        'id': produto[0],
                        'categoria': produto[1],
                        'cor': produto[2],
                        'qntd': produto[3],
                        'nome_produto': produto[4],
                        'preco': float(produto[5]),
                        'imagem': produto[6],
                        'descricao': produto[7],
                        'autor': produto[8],
                        'ano_lancamento': produto[9],
                        'genero': produto[10],
                        'marca': produto[11]
                    })

                return jsonify({'produtos': produtos}), 500

    except mysql.connector.Error as error:
            return jsonify({'error': str(error)}), 500
    else:
        return jsonify({'mensagem': 'O parâmetro "nome" é obrigatório'}), 400



@produtos_bp.route('/del_produto/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    try:
        con = utils.connect_to_database()  
        if not con:
            return jsonify({'error': 'Falha ao conectar ao banco de dados'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            sql = "DELETE FROM produtos WHERE id=%s"
            valores = (produto_id,)

            mycursor.execute(sql, valores)
            mydb.commit()

            if mycursor.rowcount == 0:
                return jsonify({'mensagem': 'Produto não encontrado'}), 404

            return jsonify({'mensagem': f'Produto com ID {produto_id} deletado com sucesso'}), 200

    except mysql.connector.Error as error:
        return jsonify({'error': str(error)}), 500



@produtos_bp.route('/delete_all_produtos', methods=['DELETE'])
def delete_all_produtos():
    try:
        con = utils.connect_to_database()  
        if not con:
            return jsonify({'error': 'Failed to connect to database'}), 500
        with con as mydb:
            mycursor = mydb.cursor()

            sql = "DELETE FROM produtos"

            mycursor.execute(sql)
            mydb.commit()
            
            if mycursor.rowcount > 0:
                return jsonify({'mensagem': 'Todos os livros foram deletados com sucesso'}), 200
            else:
                return jsonify({'mensagem': 'Nenhum livro para deletar'}), 404

    except mysql.connector.Error as error:
        return jsonify({'erro': str(error)}), 500