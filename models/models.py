import reflex as rx
import sqlmodel

class User(rx.Model, table=True):
    """Modèle de table utilisateur pour PostgreSQL avec gestion des rôles."""
    nom_prenom: str
    email: str = sqlmodel.Field(index=True, unique=True)
    password: str
    telephone: str
    role: str = "client"  # Valeurs possibles : "superadmin", "admin", "client"