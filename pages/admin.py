import reflex as rx
import time
from components.layout import dashboard_layout

class AdminState(rx.State):
    """État sécurisé avec gestion du délai d'inactivité de 15 minutes et interactivité de la page."""
    agriculture_index: int = 0
    
    # Sécurité & Session
    is_authenticated: bool = True  # À lier à votre authentification réelle
    last_activity_time: float = time.time()

    def check_session(self):
        """Vérifie l'accès et déconnecte l'utilisateur après 15 minutes (900s) d'inactivité[cite: 2]."""
        TIMEOUT_LIMIT = 900  # 15 minutes en secondes
        current_time = time.time()

        if not self.is_authenticated:
            return rx.redirect("/login")

        if (current_time - self.last_activity_time) > TIMEOUT_LIMIT:
            self.is_authenticated = False
            return rx.redirect("/login")

        self.last_activity_time = current_time

    def update_activity(self):
        """Met à jour le timestamp de la dernière action de l'utilisateur."""
        self.last_activity_time = time.time()

    def next_season(self):
        self.update_activity()
        self.agriculture_index = (self.agriculture_index + 1) % 3

    def prev_season(self):
        self.update_activity()
        self.agriculture_index = (self.agriculture_index - 1) % 3


def kpi_card(title: str, value: str, icon: str, action_text: str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.box(
                rx.icon(tag=icon, color="#113832", size=22),
                background="linear-gradient(135deg, #e1efe9 0%, #c8e6c9 100%)", 
                padding="12px", border_radius="14px", 
                box_shadow="0 4px 10px rgba(17, 56, 50, 0.1)"
            ),
            rx.vstack(
                rx.text(value, size="6", color="#113832", weight="bold"),
                rx.text(title, size="2", color="#666", weight="medium"),
                align="start", spacing="0"
            ),
            rx.spacer(),
            rx.badge(action_text, color_scheme="green", variant="soft", cursor="pointer", border_radius="8px"),
            spacing="4", align="center"
        ),
        background="white", width="100%", border_radius="20px",
        box_shadow="0 10px 30px rgba(0,0,0,0.04)", 
        border="1px solid rgba(0,0,0,0.04)",
        transition="all 0.3s ease",
        _hover={"transform": "translateY(-4px)", "box_shadow": "0 15px 35px rgba(17, 56, 50, 0.08)"}
    )

def parcel_item(name: str, stock_info: str) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(name, weight="bold", size="3", color="#222"),
            rx.text(stock_info, size="1", color="#666"),
            spacing="0", align="start"
        ),
        rx.spacer(),
        rx.icon("chevron-right", size=18, color="#888"),
        width="100%", padding="14px", border_bottom="1px solid #f2f5f3",
        _hover={"background": "#f8fbf9", "border_radius": "10px"}, cursor="pointer"
    )

@rx.page(
    route="/admin",
    on_load=AdminState.check_session  # Sécurité automatique à l'accès de la page admin[cite: 2]
)
def admin_page():
    return dashboard_layout(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading("Tableau de Bord", size="7", color="#113832", weight="bold"),
                    rx.text("Bienvenue sur la plateforme de gestion AGUIFERME.", size="2", color="#666"),
                    align="start", spacing="1"
                ),
                rx.spacer(),
                rx.badge("Mode Sécurisé • Actif", color_scheme="green", variant="surface", padding="8px 12px", border_radius="10px"),
                width="100%", align="center"
            ),
            
            # Grille KPI responsive de luxe
            rx.grid(
                kpi_card("Alvéoles d'Œufs", "145 Alv.", "egg", "Gérer"),
                kpi_card("Stock Légumes", "320 Kg", "carrot", "Prix"),
                kpi_card("Commandes Clients", "8 en attente", "shopping-cart", "Traiter"),
                kpi_card("Chiffre d'Affaires", "1.250.000 GNF", "trending-up", "Détails"),
                columns={"initial": "1", "sm": "2", "md": "2", "lg": "4"}, 
                spacing="5", 
                width="100%"
            ),
            
            # Grille Centrale responsive
            rx.grid(
                # Colonne 1 : Tarifs du jour
                rx.card(
                    rx.vstack(
                        rx.heading("TARIFS DU JOUR", size="4", color="#113832", weight="bold"),
                        rx.input(placeholder="Rechercher un produit...", width="100%", radius="full", variant="surface", border="1px solid #e0e0e0"),
                        rx.vstack(
                            rx.hstack(
                                rx.text("Alvéole d'œufs (30 œufs)", size="2", weight="medium", color="#333"),
                                rx.spacer(),
                                rx.badge("65 000 GNF", color_scheme="green", variant="solid"),
                                width="100%", padding="10px 0", border_bottom="1px solid #f2f5f3"
                            ),
                            rx.hstack(
                                rx.text("Tomate (1 kg)", size="2", weight="medium", color="#333"),
                                rx.spacer(),
                                rx.badge("25 000 GNF", color_scheme="green", variant="solid"),
                                width="100%", padding="10px 0", border_bottom="1px solid #f2f5f3"
                            ),
                            rx.hstack(
                                rx.text("Piment (1 kg)", size="2", weight="medium", color="#333"),
                                rx.spacer(),
                                rx.badge("15 000 GNF", color_scheme="green", variant="solid"),
                                width="100%", padding="10px 0"
                            ),
                            width="100%", spacing="1"
                        ),
                        width="100%", spacing="4"
                    ),
                    background="white", border_radius="20px", width="100%", box_shadow="0 10px 30px rgba(0,0,0,0.04)", padding="1.5em", border="1px solid rgba(0,0,0,0.04)"
                ),
                
                # Colonne 2 : Parcelles
                rx.card(
                    rx.vstack(
                        rx.heading("PARCELLES", size="4", color="#113832", weight="bold"),
                        parcel_item("P1 - Maïs", "12 Ha • En croissance"),
                        parcel_item("P2 - Tomate", "4 Ha • Prêt récolte"),
                        parcel_item("P3 - Tomate", "6 Ha • Floraison"),
                        parcel_item("P4 - Piment", "3 Ha • Récolte en cours"),
                        width="100%", spacing="1"
                    ),
                    background="white", border_radius="20px", width="100%", box_shadow="0 10px 30px rgba(0,0,0,0.04)", padding="1.5em", border="1px solid rgba(0,0,0,0.04)"
                ),
                
                # Colonne 3 : Suivi Opérations Végétales (Chevrons dynamiques)
                rx.card(
                    rx.vstack(
                        rx.heading("SUIVI OPÉRATIONS", size="4", color="#113832", weight="bold"),
                        rx.text("AGRICULTURE", size="1", color="#888", weight="bold"),
                        rx.hstack(
                            rx.icon(
                                "chevron-left", 
                                cursor="pointer", 
                                color="#113832",
                                _hover={"transform": "scale(1.2)"},
                                on_click=AdminState.prev_season
                            ), 
                            rx.spacer(), 
                            rx.text(
                                rx.cond(
                                    AdminState.agriculture_index == 0, "Saison en cours",
                                    rx.cond(AdminState.agriculture_index == 1, "Saison Prévisionnelle", "Saison Passée")
                                ), 
                                weight="bold", color="#113832"
                            ), 
                            rx.spacer(), 
                            rx.icon(
                                "chevron-right", 
                                cursor="pointer", 
                                color="#113832",
                                _hover={"transform": "scale(1.2)"},
                                on_click=AdminState.next_season
                            ), 
                            width="100%", padding="10px", background="#f4f8f5", border_radius="12px"
                        ),
                        rx.box(
                            rx.text(
                                rx.cond(
                                    AdminState.agriculture_index == 0, "Rendement optimal",
                                    rx.cond(AdminState.agriculture_index == 1, "Planification active", "Bilan clôturé")
                                ), 
                                color="#113832", weight="bold", size="3"
                            ),
                            height="110px", background="linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)", border_radius="14px", width="100%", display="flex", align_items="center", justify_content="center"
                        ),
                        rx.button("NOUVELLE OPÉRATION +", background="#113832", color="white", width="100%", radius="full", padding="1.2em", box_shadow="0 4px 12px rgba(17, 56, 50, 0.2)"),
                        width="100%", spacing="4"
                    ),
                    background="white", border_radius="20px", width="100%", box_shadow="0 10px 30px rgba(0,0,0,0.04)", padding="1.5em", border="1px solid rgba(0,0,0,0.04)"
                ),
                columns={"initial": "1", "md": "3"}, 
                spacing="5", 
                width="100%"
            ),
            
            # Bloc Commandes Clients
            rx.card(
                rx.flex(
                    rx.vstack(
                        rx.heading("DERNIÈRES COMMANDES CLIENTS", size="4", color="#113832", weight="bold"),
                        rx.flex(
                            rx.badge("Client: Restaurant Le Palmier - 10 Alvéoles", color_scheme="blue", variant="soft", padding="8px"),
                            rx.badge("Client: Marché Central - 25 Kg Tomates", color_scheme="green", variant="soft", padding="8px"),
                            direction={"initial": "column", "sm": "row"},
                            spacing="3"
                        ),
                        align="start", spacing="2"
                    ),
                    rx.spacer(),
                    rx.button("VOIR TOUTES LES COMMANDES", background="#113832", color="white", radius="full", width={"initial": "100%", "sm": "auto"}, box_shadow="0 4px 12px rgba(17, 56, 50, 0.2)"),
                    direction={"initial": "column", "sm": "row"},
                    width="100%", align="center", spacing="4"
                ),
                background="white", border_radius="20px", width="100%", box_shadow="0 10px 30px rgba(0,0,0,0.04)", padding="2em", border="1px solid rgba(0,0,0,0.04)"
            ),
            
            width="100%", align="start", spacing="6"
        )
    )