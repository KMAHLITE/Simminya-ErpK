import reflex as rx

class MenuState(rx.State):
    is_agriculture_open: bool = False
    is_menu_open: bool = False  # Fermé par défaut sur mobile pour ne pas encombrer

    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open

    def close_menu(self):
        self.is_menu_open = False
    
    def toggle_agriculture(self):
        self.is_agriculture_open = not self.is_agriculture_open

def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(tag=icon, size=20),
            rx.text(text, size="2", weight="light"),
            spacing="3", padding="10px", color="white",
        ),
        href=href, width="100%",
        _hover={"background": "rgba(255, 255, 255, 0.1)", "border_radius": "8px"},
    )

def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.box(
        rx.flex(
            # Overlay sombre en arrière-plan sur mobile quand le menu est ouvert
            rx.cond(
                MenuState.is_menu_open,
                rx.box(
                    position="fixed", top="0", left="0", width="100vw", height="100vh",
                    background="rgba(0,0,0,0.5)", z_index="998",
                    on_click=MenuState.close_menu,
                    display={"initial": "block", "md": "none"}
                ),
                rx.fragment()
            ),

            # Sidebar (Tiroir responsive : couvre 95% sur mobile en position fixed, et sticky/normal sur desktop)
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.image(src="/logo.png", width="25px"), 
                        rx.heading("SIMMINYA", size="5", color="white", weight="light"),
                        rx.spacer(),
                        # Bouton de fermeture 'x' visible uniquement sur mobile dans le tiroir
                        rx.button(
                            rx.icon("x", size=20), 
                            on_click=MenuState.close_menu, 
                            variant="ghost", 
                            color="white",
                            display={"initial": "flex", "md": "none"}
                        ),
                        width="100%", align="center"
                    ),
                    rx.divider(color="rgba(255,255,255,0.5)", margin_y="0.75em", box_shadow="0 5px 10px rgba(0,0,0,0.15)"),
                    
                    sidebar_item("Tableau de bord", "layout-dashboard", "/admin"),
                    sidebar_item("Ferme", "building-2", "/admin/ferme"),
                    
                    # Section Agriculture
                    rx.vstack(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="sprout", size=20), 
                                rx.text("Agriculture", size="3", weight="regular"), 
                                rx.spacer(), 
                                rx.icon(tag="chevron-down", size=16),
                                spacing="3", width="100%", color="white", align="center"
                            ),
                            on_click=MenuState.toggle_agriculture, 
                            variant="ghost", width="100%", padding="10px", justify="between",
                            _hover={"background": "rgba(255, 255, 255, 0.1)", "border_radius": "8px"}
                        ),
                        rx.cond(
                            MenuState.is_agriculture_open, 
                            rx.vstack(
                                sidebar_item("Cartographie", "map", "/admin/map"),
                                sidebar_item("Opérations", "list-todo", "/admin/operations"),
                                width="100%", padding_left="1.5em", spacing="1"
                            )
                        ),
                        width="100%", spacing="0"
                    ),
                    
                    sidebar_item("Paramètres", "settings", "/admin/settings"),
                    rx.spacer(),
                    width="100%", height="100%",
                ),
                # Positionnement dynamique : tiroir glissant sur mobile, fixe sur grand écran
                position={"initial": "fixed", "md": "sticky"},
                top="0",
                left="0",
                height="100vh",
                width={"initial": "95%", "sm": "300px"},
                max_width="320px",
                background="#1a4d44", 
                padding="1.5em",
                z_index="999",
                transition="transform 0.3s ease-in-out",
                transform=rx.cond(
                    MenuState.is_menu_open,
                    "translateX(0)",
                    {"initial": "translateX(-100%)", "md": "translateX(0)"}
                ),
                box_shadow={"initial": "5px 0 15px rgba(0,0,0,0.3)", "md": "none"}
            ),

            # Contenu principal de la page
            rx.vstack(
                rx.hstack(
                    rx.button(
                        rx.icon(tag="menu", size=22),
                        on_click=MenuState.toggle_menu,
                        background="transparent",
                        color="#1a4d44",
                        variant="ghost"
                    ),
                    rx.spacer(),
                    rx.avatar(fallback="AF", size="2", margin_right="1em", border_radius="50px", border="1px solid #1a4d44"),
                    width="100%", padding="1em", background="white", border_bottom="1px solid #e0e0e0", 
                    box_shadow="0 2px 5px rgba(0,0,0,0.05)"
                ),
                rx.box(content, width="100%", padding="2em", overflow_y="auto"),
                width="100%", background="#f4f6f8", min_height="100vh", flex="1", spacing="0"
            ),
            width="100%", position="relative"
        ),
        width="100%", min_height="100vh"
    )