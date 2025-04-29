import jwt
from flask import request, jsonify

SECRET_KEY = "secreto123"

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token não fornecido'}), 401

        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401

        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper
