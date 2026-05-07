from flask import Flask, jsonify, request
 
app = Flask(__name__)
 
# Banco de dados fictício
produtos = [
    {"id": 1, "nome": "Camiseta", "preco": 50.00},
    {"id": 2, "nome": "Tênis", "preco": 120.00}
]
 
# GET - Listar produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(produtos)
 
# POST - Adicionar produto
@app.route('/produtos', methods=['POST'])
def adicionar_produto():
 
    novo_produto = request.get_json()
 
    produtos.append(novo_produto)
 
    return jsonify({
        "mensagem": "Produto adicionado com sucesso!"
    }), 201
 
# PUT - Atualizar produto
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
 
    produto = next((p for p in produtos if p['id'] == id), None)
 
    if produto is None:
        return jsonify({
            "erro": "Produto não encontrado!"
        }), 404
 
    dados_atualizados = request.get_json()
 
    produto.update(dados_atualizados)
 
    return jsonify({
        "mensagem": "Produto atualizado com sucesso!"
    })
 
# DELETE - Remover produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
def remover_produto(id):
 
    produto = next((p for p in produtos if p['id'] == id), None)
 
    if produto is None:
        return jsonify({
            "erro": "Produto não encontrado!"
        }), 404
 
    produtos.remove(produto)
 
    return jsonify({
        "mensagem": "Produto removido com sucesso!"
    })
 
# Executar aplicação
if __name__ == '__main__':
    app.run(debug=True)