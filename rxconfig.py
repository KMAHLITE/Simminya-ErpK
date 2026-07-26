import os
import reflex as rx

port = int(os.environ.get("PORT", 10000))

config = rx.Config(
    app_name="simminya_erpk",
    db_url="sqlite:///reflex.db",
    backend_port=port,
    backend_host="0.0.0.0",
    api_url="https://simminya-erpk.onrender.com",
    deploy_url="https://simminya-erpk.onrender.com", # Ajout crucial pour les assets et les websockets front
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)