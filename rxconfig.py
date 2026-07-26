import os
import reflex as rx

# Récupération dynamique du port Render ou 10000 par défaut
port = int(os.environ.get("PORT", 10000))

config = rx.Config(
    app_name="simminya_erpk",
    db_url="sqlite:///reflex.db",
    backend_port=port,
    backend_host="0.0.0.0",
    api_url="https://votre-app-render.onrender.com", # Remplacez par votre vraie URL Render
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)