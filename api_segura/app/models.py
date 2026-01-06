# app/models.py

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=True) 

    #! Métodos de Segurança
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # Usar algoritmo de hashing seguro (ex: PBKDF2, bcrypt, Argon2). Combina salting e hashing. Protege contra tabelas rainbow
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # Resistente a ataques de timing