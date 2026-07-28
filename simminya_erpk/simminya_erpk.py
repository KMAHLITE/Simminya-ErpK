import reflex as rx
from db import init_db
from pages import welcom, login, register, admin

# Initialisation unique de la BDB au démarrage
init_db()

app = rx.App()

# Enregistrement des routes
