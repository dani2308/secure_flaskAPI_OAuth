# app/__init__.py
# Ficheiro que cria a app flask e integra extensões, configs e rotas
from flask import Flask
from app.extensions import db, migrate
from app.config import Config
from app.extensions.oauth import configure_oauth 
from app.extensions.oauth import oauth
from app.routes.auth import auth_bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.secret_key = os.getenv("SECRET_KEY", "uma_chave_muito_secreta_e_segura")

    db.init_app(app)
    migrate.init_app(app, db)

    configure_oauth(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(oauth, url_prefix="/auth/oauth")

    return app
