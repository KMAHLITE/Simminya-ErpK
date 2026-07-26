import os
import reflex as rx

port = int(os.environ.get("PORT", 10000))
# Récupère PostgreSQL sur Render, ou SQLite par défaut en local
database_url = os.environ.get("DATABASE_URL", "sqlite:///reflex.db")

config = rx.Config(
    app_name="simminya_erpk",
    db_url=database_url,
    backend_port=port,
    backend_host="0.0.0.0",
    api_url="https://simminya-erpk.onrender.com",
    deploy_url="https://simminya-erpk.onrender.com",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)