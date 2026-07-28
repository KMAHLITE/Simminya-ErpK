import os
import sqlmodel

# Récupération sécurisée de l'URL (PostgreSQL sur Render ou SQLite en local par défaut)
def get_database_url():
    url = os.getenv("DATABASE_URL", "sqlite:///reflex.db")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

engine = sqlmodel.create_engine(get_database_url(), echo=True)

def init_db():
    """Crée les tables dans la base de données si elles n'existent pas."""
    sqlmodel.SQLModel.metadata.create_all(engine)

def get_session():
    """Fournit une session de base de données pour les requêtes."""
    with sqlmodel.Session(engine) as session:
        yield session