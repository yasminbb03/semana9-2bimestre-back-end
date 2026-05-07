from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

# Chave secreta
app.config['SECRET_KEY'] = 'minha_chave_secreta'

# Função para verificar token
def token_requerido(f):

    @wraps(f)

    def decorator(*args, **kwargs):

        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({
                'mensagem': 'Token de acesso é necessário!'
            }), 401

        try:
            dados = jwt.decode(
                token,
                app.config['SECRET_KEY'],
                algorithms=["HS256"]
            )

            request.user_data = dados

        except:
            return jsonify({
                'mensagem': 'Token inválido!'
            }), 401

        return f(*args, **kwargs)

    return decorator

# Login
@app.route('/login', methods=['POST'])
def login():

    dados = request.get_json()

    if dados['usuario'] == 'admin' and dados['senha'] == '1234':

        token = jwt.encode({

            'usuario': dados['usuario'],

            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)

        }, app.config['SECRET_KEY'])

        return jsonify({
            'token': token
        })

    return make_response(
        'Usuário ou senha incorretos!',
        401
    )

# Produtos
@app.route('/produtos', methods=['GET'])
@token_requerido
def listar_produtos():

    produtos = [
        {"id": 1, "nome": "Camiseta", "preco": 50.00},
        {"id": 2, "nome": "Tênis", "preco": 120.00}
    ]

    return jsonify(produtos)

# Adicionar produto
@app.route('/produtos', methods=['POST'])
@token_requerido
def adicionar_produto():

    if request.user_data['usuario'] != 'admin':

        return jsonify({
            'mensagem': 'Ação não permitida!'
        }), 403

    novo_produto = request.get_json()

    return jsonify({
        'mensagem': 'Produto adicionado com sucesso!'
    }), 201

# Remover produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
@token_requerido
def remover_produto(id):

    if request.user_data['usuario'] != 'admin':

        return jsonify({
            'mensagem': 'Ação não permitida!'
        }), 403

    return jsonify({
        'mensagem': 'Produto removido com sucesso!'
    }), 200

# Executar API
if __name__ == '__main__':
    app.run(debug=True)