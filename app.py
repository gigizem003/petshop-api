from flask import Flask, jsonify, request
from produtos import products
from auth import token_required

app = Flask(__name__)

@app.route("/products", methods=["GET"])
@token_required
def get_products():
    preco_asc = request.args.get("preco_asc")
    preco_desc = request.args.get("preco_desc")
    description_part = request.args.get("description_part")

    result = products.copy()

    if preco_asc == "true":
        result.sort(key=lambda x: x["product_price"])
    elif preco_desc == "true":
        result.sort(key=lambda x: x["product_price"], reverse=True)

    if description_part:
        result = [p for p in result if description_part.lower() in p["product_description"].lower()]

    return jsonify(result)

@app.route("/products/<int:id>", methods=["GET"])
@token_required
def get_product_by_id(id):
    for product in products:
        if product["id"] == id:
            return jsonify(product)
    return jsonify({"error": "Produto não encontrado"}), 404

@app.route("/login", methods=["POST"])
def login():
    auth = request.get_json()
    if auth["nome"] == "admin" and auth["senha"] == "admin":
        import jwt
        token = jwt.encode({"user": auth['nome']}, "secreto123", algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"error": "Cadastro inválido"}), 401

if __name__ == "__main__":
    app.run(debug=True)
