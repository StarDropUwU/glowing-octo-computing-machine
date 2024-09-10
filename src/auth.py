from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

def token_required(f):
    """
    Decorador para verificar a presença e validade de um token JWT nas rotas protegidas.

    O token deve ser enviado no cabeçalho 'Authorization' no formato 'Bearer <token>'.
    Caso o token seja inválido, expirado ou ausente, a requisição falha com um código 403.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Token is missing"}), 403

        # Valida se o token está no formato 'Bearer <token>'
        try:
            token_type, token = auth_header.split()
            if token_type.lower() != 'bearer':
                return jsonify({"error": "Invalid token type, must be 'Bearer'"}), 403
        except ValueError:
            return jsonify({"error": "Invalid Authorization header format"}), 403

        # Verifica o token JWT
        try:
            jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid Token"}), 403

        return f(*args, **kwargs)

    return decorated_function
