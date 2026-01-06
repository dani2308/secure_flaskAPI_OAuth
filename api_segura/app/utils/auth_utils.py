# app/utils/auth_utils.py

import jwt
from flask import request, jsonify, current_app
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        #! Verifica se o token JWT está presente no cabeçalho
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        #! Se não estiver, retorna erro
        if not token:
            return jsonify({'error': 'Token JWT é obrigatório'}), 401

        #! Tenta decodificar o token JWT
        try:
            data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401

        #! Se tudo estiver ok, chama a função original com o user_id atual
        return f(current_user_id, *args, **kwargs)

    return decorated
