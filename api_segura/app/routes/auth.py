# app/routes/auth.py

from flask import Blueprint, request, jsonify, current_app, redirect, url_for, session
from app.models import User
from app.extensions import db
from app.utils.auth_utils import token_required
from app.extensions.oauth import oauth
import re
import datetime
import jwt
import secrets

auth_bp = Blueprint('auth', __name__)

def generate_token(user_id, expires_in_hours=1):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=expires_in_hours)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

def generate_refresh_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not username or not email or not password:
        return jsonify({"error": "Todos os campos são obrigatórios!"}), 400

    if len(username) < 3 or len(username) > 30:
        return jsonify({"error": "O nome de utilizador deve ter entre 3 e 30 caracteres"}), 400

    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        return jsonify({"error": "Email inválido"}), 400

    if len(password) < 8:
        return jsonify({"error": "A password deve ter pelo menos 8 caracteres"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Utilizador já existe"}), 409

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Utilizador registado com sucesso"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email", "").strip()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"error": "Email e password são obrigatórios"}), 400

    email_regex = r"[^@]+@[^@]+\.[^@]+"
    if not re.match(email_regex, email):
        return jsonify({"error": "Email inválido"}), 400

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = generate_token(user.id)
        refresh_token = generate_refresh_token(user.id)

        return jsonify({
            "token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 3600
        }), 200

    return jsonify({"error": "Credenciais inválidas"}), 401

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh_token")

    if not refresh_token:
        return jsonify({"error": "Refresh token é obrigatório"}), 400

    try:
        payload = jwt.decode(refresh_token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        user_id = payload["user_id"]

        new_token = generate_token(user_id)
        return jsonify({
            "token": new_token,
            "expires_in": 3600
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Refresh token inválido"}), 401

@auth_bp.route('/protected', methods=['GET'])
@token_required
def protected_route(current_user_id):
    return jsonify({"message": f"Bem-vindo, utilizador {current_user_id}!"})

@auth_bp.route("/login/google")
def login_google():
    state = secrets.token_urlsafe(16)
    session["oauth_state"] = state

    redirect_uri = url_for("auth.google_callback", _external=True)
    return oauth.google.authorize_redirect(redirect_uri, state=state)

@auth_bp.route("/login/google/callback")
def google_callback():
    state_in_session = session.get("oauth_state")
    state_from_provider = request.args.get("state")

    if not state_in_session or state_in_session != state_from_provider:
        return jsonify({"error": "Estado inválido."}), 400

    token = oauth.google.authorize_access_token()
    user_info = oauth.google.userinfo()


    if user_info is None:
        return jsonify({"error": "Erro ao obter dados do utilizador"}), 400

    email = user_info["email"]
    name = user_info.get("name", "Utilizador Google")

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email, username=name)
        db.session.add(user)
        db.session.commit()

    access_token = generate_token(user.id)
    refresh_token = generate_refresh_token(user.id)

    return jsonify({
        "token": access_token,
        "refresh_token": refresh_token,
        "expires_in": 3600
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():    
    session.pop("oauth_state", None)
    
    return jsonify({"message": "Logout efetuado com sucesso"}), 200
