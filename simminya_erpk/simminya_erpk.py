import reflex as rx
from db import init_db
from pages.welcom import welcome
from pages.login import login
from pages.register import register
from pages.admin import admin_page

# Initialisation unique de la BDB au démarrage
init_db()

app = rx.App()

# Enregistrement des routes
app.add_page(welcome, route="/", title="Simminya - Accueil")
app.add_page(login, route="/login", title="Simminya - Connexion")
app.add_page(register, route="/register", title="Simminya - Inscription")
app.add_page(admin_page, route="/admin", title="Simminya - Dashboard")