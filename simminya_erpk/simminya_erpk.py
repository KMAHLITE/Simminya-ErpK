import reflex as rx
import sqlmodel
from models.models import User  # Import indispensable pour que Reflex connaisse votre modèle de données

# Importation de vos pages depuis le dossier racine pages/
from pages.welcom import welcome
from pages.login import login
from pages.register import register

# Optionnel : Importation du dashboard admin si déjà créé
# from pages.admin_dashboard import admin_dashboard_page

app = rx.App()

# --- CRÉATION AUTOMATIQUE DES TABLES DANS POSTGRESQL AU DÉMARRAGE ---
@app.on_load
def create_tables_on_startup():
    with rx.session() as session:
        sqlmodel.SQLModel.metadata.create_all(session.bind)
# -------------------------------------------------------------------

# Enregistrement des routes de l'application Simminya
app.add_page(welcome, route="/", title="Simminya - Accueil")
app.add_page(login, route="/login", title="Simminya - Connexion")
app.add_page(register, route="/register", title="Simminya - Inscription")
# app.add_page(admin_dashboard_page, route="/admin", title="Simminya - Admin")