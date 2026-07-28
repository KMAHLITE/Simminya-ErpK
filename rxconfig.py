import os
import reflex as rx

port = int(os.environ.get("PORT", 10000))

# On récupère DIRECTEMENT la variable d'environnement de Render. 
# Si elle n'existe pas (par exemple si vous oubliez de la configurer), 
# il vaut mieux que l'application lève une erreur plutôt que d'utiliser de faux identifiants locaux.
database_url = os.environ.get("DATABASE_URL")

config = rx.Config(
    app_name="simminya_erpk",
    db_url=database_url,  # Reflex se connectera à la base PostgreSQL de Render via cette variable
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