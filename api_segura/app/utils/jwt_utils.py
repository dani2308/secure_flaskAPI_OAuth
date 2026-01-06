# app/utils/jwt_utils.py

import jwt
import datetime
from flask import current_app

def generate_jwt(user_id, expires_in=3600):

    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=expires_in)
    }

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    #! Resultado é uma string codificada em base64
    return token


# Stateless - não mantém a sessão no servidor