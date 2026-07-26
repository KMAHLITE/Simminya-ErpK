import reflex as rx

# Importation de vos pages depuis le dossier racine pages/
from pages.welcom import welcome
from pages.login import login
from pages.register import register

# Optionnel : Importation du dashboard admin si déjà créé
# from pages.admin_dashboard import admin_dashboard_page

app = rx.App()

# Enregistrement des routes de l'application Simminya
app.add_page(welcome, route="/", title="Simminya - Accueil")
app.add_page(login, route="/login", title="Simminya - Connexion")
app.add_page(register, route="/register", title="Simminya - Inscription")
# app.add_page(admin_dashboard_page, route="/admin", title="Simminya - Admin")