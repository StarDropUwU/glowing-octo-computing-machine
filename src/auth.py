from functools import wraps
from flask import request, jsonify
import jwt
from config import Config

class TokenRequired:
    def __init__(self, f):
        self.f = f

    def __call__(self, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 403
        try:
            jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except:
            return jsonify({"error": "Invalid Token"}), 403
        return self.f(*args, **kwargs)


