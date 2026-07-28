import sqlmodel
from typing import Optional

class User(sqlmodel.SQLModel, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    email: str = sqlmodel.Field(index=True, unique=True)
    password_hash: str
    nom: str
    prenom: str
    telephone: Optional[str] = None
    role: str = "client"  # Valeurs possibles : "superadmin", "admin", "client"