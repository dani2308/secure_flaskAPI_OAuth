# app/extensions.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
# Para Interface entre app Flask e BD. Facilita a criação de modelos de dados.
migrate = Migrate()
# Integra Alembic para gerir migrações (criar/alterar tabelas).

# Usar flask db init para criar pasta migrations
# Usar flask db migrate para criar ficheiro com alterações
# Usar flask db upgrade para aplicar migrações
