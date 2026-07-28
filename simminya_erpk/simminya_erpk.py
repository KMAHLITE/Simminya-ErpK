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

# --- INITIALISATION DE LA BASE DE DONNÉES ---
def init_db():
    # Crée un moteur de base de données à partir de la configuration Reflex/SQLModel
    engine = sqlmodel.create_engine(rx.get_db_engine_url())
    sqlmodel.SQLModel.metadata.create_all(engine)

# Exécution de la création des tables au lancement du script
init_db()
# ---------------------------------------------

# Enregistrement des routes de l'application Simminya
app.add_page(welcome, route="/", title="Simminya - Accueil")
app.add_page(login, route="/login", title="Simminya - Connexion")
app.add_page(register, route="/register", title="Simminya - Inscription")
# app.add_page(admin_dashboard_page, route="/admin", title="Simminya - Admin")