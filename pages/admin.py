import reflex as rx
from components.layout import dashboard_layout

class AdminState(rx.State):
    """État pour gérer l'interactivité de la page admin (chevron dynamique AGRICULTURE)."""
    # Index ou état pour faire basculer dynamiquement le contenu ou l'affichage de l'onglet agriculture
    agriculture_index: int = 0

    def next_season(self):
        """Passe à la saison ou vue suivante lors du clic sur le chevron droit."""
        self.agriculture_index = (self.agriculture_index + 1) % 3

    def prev_season(self):
        """Passe à la saison ou vue précédente lors du clic sur le chevron gauche."""
        self.agriculture_index = (self.agriculture_index - 1) % 3


def kpi_card(title: str, value: str, icon: str, action_text: str) -> rx.Component:
    return rx.card(
        rx.hstack(
            rx.box(
                rx.icon(tag=icon, color="#1a4d44", size=20),
                background="#c8e6c9", padding="10px", border_radius="12px", 
            ),
            rx.vstack(
                rx.text(value, size="5", color="black", weight="regular"),
                rx.text(title, size="2", color="gray", weight="light"),
                align="start", spacing="0"
            ),
            rx.spacer(),
            rx.badge(action_text, color_scheme="green", variant="outline", cursor="pointer"),
            spacing="4", align="center"
        ),
        background="white", width="100%", border_radius="15px",
        box_shadow="0 10px 20px rgba(0,0,0,0.15)", 
        transition="transform 0.2s",
        _hover={"transform": "translateY(-5px)"}
    )

def parcel_item(name: str, stock_info: str) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.text(name, weight="medium", size="3"),
            rx.text(stock_info, size="1", color="gray"),
            spacing="0", align="start"
        ),
        rx.spacer(),
        rx.icon("chevron-right", size=18, color="gray"),
        width="100%", padding="12px", border_bottom="1px solid #f0f0f0",
        _hover={"background": "#f9f9f9", "border_radius": "8px"}, cursor="pointer"
    )

@rx.page(route="/admin")
def admin_page():
    return dashboard_layout(
        rx.vstack(
            rx.text("Tableau de bord ", size="4", color="gray", weight="light"),
            
            # Grille KPI adaptée responsive (colonnes fluides selon l'écran)
            rx.grid(
                kpi_card("Alvéoles d'Œufs", "145 Alv.", "egg", "Gérer"),
                kpi_card("Stock Légumes", "320 Kg", "carrot", "Prix"),
                kpi_card("Commandes Clients", "8 en attente", "shopping-cart", "Traiter"),
                kpi_card("Chiffre d'Affaires", "1.250.000 GNF", "trending-up", "Détails"),
                columns=["1", "2", "2", "4"], spacing="4", width="100%"
            ),
            
            # Grille Centrale responsive (passe de 3 colonnes sur grand écran à 1 colonne sur mobile)
            rx.grid(
                # Colonne 1 : Gestion Rapide des Prix & Catalogue
                rx.card(
                    rx.vstack(
                        rx.heading("TARIFS DU JOUR", size="4", margin_bottom="0.5em", weight="regular"),
                        rx.input(placeholder="Rechercher un produit...", width="100%", radius="full", variant="surface"),
                        rx.hstack(
                            rx.text("Alvéole d'œufs (30 œufs)", size="2", weight="medium"),
                            rx.spacer(),
                            rx.badge("65 000 GNF", color_scheme="green", variant="solid"),
                            width="100%", padding="8px 0", border_bottom="1px solid #f0f0f0"
                        ),
                        rx.hstack(
                            rx.text("Tomate (1 kg)", size="2", weight="medium"),
                            rx.spacer(),
                            rx.badge("25 000 GNF", color_scheme="green", variant="solid"),
                            width="100%", padding="8px 0", border_bottom="1px solid #f0f0f0"
                        ),
                        rx.hstack(
                            rx.text("Piment (1 kg)", size="2", weight="medium"),
                            rx.spacer(),
                            rx.badge("15 000 GNF", color_scheme="green", variant="solid"),
                            width="100%", padding="8px 0"
                        ),
                        width="100%", spacing="3"
                    ),
                    background="white", border_radius="15px", width="100%", box_shadow="0 5px 15px rgba(0,0,0,0.05)"
                ),
                
                # Colonne 2 : Parcelles & Cultures
                rx.card(
                    rx.vstack(
                        rx.heading("PARCELLES", size="4", margin_bottom="0.5em", weight="light"),
                        parcel_item("P1 - Maïs", "12 Ha • En croissance"),
                        parcel_item("P2 - Tomate", "4 Ha • Prêt récolte"),
                        parcel_item("P3 - Tomate", "6 Ha • Floraison"),
                        parcel_item("P4 - Piment", "3 Ha • Récolte en cours"),
                        width="100%", spacing="1"
                    ),
                    background="white", border_radius="15px", width="100%", box_shadow="0 5px 15px rgba(0,0,0,0.05)"
                ),
                
                # Colonne 3 : Suivi Opérations Végétales (Chevrons dynamiques cliquables)
                rx.card(
                    rx.vstack(
                        rx.heading("SUIVI OPÉRATIONS", size="4"),
                        rx.text("AGRICULTURE", size="1", color="gray"),
                        rx.hstack(
                            rx.icon(
                                "chevron-left", 
                                cursor="pointer", 
                                _hover={"color": "#1a4d44", "transform": "scale(1.1)"},
                                on_click=AdminState.prev_season
                            ), 
                            rx.spacer(), 
                            rx.text(
                                rx.cond(
                                    AdminState.agriculture_index == 0, "Saison en cours",
                                    rx.cond(AdminState.agriculture_index == 1, "Saison Prévisionnelle", "Saison Passée")
                                ), 
                                weight="bold"
                            ), 
                            rx.spacer(), 
                            rx.icon(
                                "chevron-right", 
                                cursor="pointer", 
                                _hover={"color": "#1a4d44", "transform": "scale(1.1)"},
                                on_click=AdminState.next_season
                            ), 
                            width="100%", padding="5px", background="#f4f6f8", border_radius="8px"
                        ),
                        rx.box(
                            rx.text(
                                rx.cond(
                                    AdminState.agriculture_index == 0, "Rendement optimal",
                                    rx.cond(AdminState.agriculture_index == 1, "Planification active", "Bilan clôturé")
                                ), 
                                color="#1a4d44", weight="bold", size="2"
                            ),
                            height="110px", background="#e8f5e9", border_radius="10px", width="100%", display="flex", align_items="center", justify_content="center"
                        ),
                        rx.button("NOUVELLE OPÉRATION +", background="#1a4d44", color="white", width="100%", radius="full"),
                        width="100%", spacing="3"
                    ),
                    background="white", border_radius="15px", width="100%", box_shadow="0 5px 15px rgba(0,0,0,0.05)"
                ),
                columns=["1", "1", "3"], spacing="4", width="100%"
            ),
            
            # Bloc Commandes Clients / Traçabilité en bas (Responsive empilé sur mobile)
            rx.card(
                rx.flex(
                    rx.vstack(
                        rx.heading("DERNIÈRES COMMANDES CLIENTS", size="4"),
                        rx.flex(
                            rx.badge("Client: Restaurant Le Palmier - 10 Alvéoles", color_scheme="blue", variant="soft"),
                            rx.badge("Client: Marché Central - 25 Kg Tomates", color_scheme="green", variant="soft"),
                            direction=["column", "row"],
                            spacing="3"
                        ),
                        align="start", spacing="2"
                    ),
                    rx.spacer(),
                    rx.button("VOIR TOUTES LES COMMANDES", background="#1a4d44", color="white", radius="full", width=["100%", "auto"]),
                    direction=["column", "row"],
                    width="100%", align="center", spacing="4"
                ),
                background="white", border_radius="15px", width="100%", box_shadow="0 5px 15px rgba(0,0,0,0.05)", padding="1.5em"
            ),
            
            width="100%", align="start", spacing="5"
        )
    )