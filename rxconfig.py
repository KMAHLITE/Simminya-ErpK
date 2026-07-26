import reflex as rx
import os

config = rx.Config(
    app_name="simminya_erpk",
    db_url=os.environ.get("DATABASE_URL"),
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        rx.plugins.RadixThemesPlugin(),
    ]
)