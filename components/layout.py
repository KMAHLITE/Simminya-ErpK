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
            rx.icon(tag=icon, size=20, color="#d4af37"),  # Touche de doré luxueux
            rx.text(text, size="2", weight="medium", color="#f8f9fa"),
            spacing="3", padding="12px 16px", width="100%",
        ),
        href=href, width="100%",
        _hover={"background": "rgba(212, 175, 55, 0.15)", "border_radius": "12px", "transition": "all 0.2s ease"},
    )

def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.box(
        rx.flex(
            # Overlay sombre de fond sur mobile uniquement quand le menu tiroir est ouvert
            rx.cond(
                MenuState.is_menu_open,
                rx.box(
                    position="fixed", top="0", left="0", width="100vw", height="100vh",
                    background="rgba(10, 25, 20, 0.6)", z_index="998",
                    backdrop_filter="blur(4px)",
                    on_click=MenuState.close_menu,
                    display={"initial": "block", "md": "none"}
                ),
                rx.fragment()
            ),

            # Sidebar / Menu Tiroir (95% sur mobile, fixe élégant sur desktop)
            rx.box(
                rx.vstack(
                    rx.hstack(
                        rx.image(src="/logo.png", width="30px"), 
                        rx.heading("AGUIFERME", size="5", color="white", weight="bold", letter_spacing="1px"),
                        rx.spacer(),
                        # Bouton de fermeture 'x' affiché uniquement sur mobile lorsque le menu est ouvert
                        rx.button(
                            rx.icon("x", size=22, color="white"), 
                            on_click=MenuState.close_menu, 
                            variant="ghost", 
                            background="rgba(255,255,255,0.1)",
                            border_radius="50%",
                            padding="8px",
                            display={"initial": "flex", "md": "none"}
                        ),
                        width="100%", align="center", padding_bottom="10px"
                    ),
                    rx.divider(color="rgba(212,175,55,0.3)", margin_y="0.5em"),
                    
                    sidebar_item("Tableau de bord", "layout-dashboard", "/admin"),
                    sidebar_item("Ferme", "building-2", "/admin/ferme"),
                    
                    # Section Agriculture avec sous-menu
                    rx.vstack(
                        rx.button(
                            rx.hstack(
                                rx.icon(tag="sprout", size=20, color="#d4af37"), 
                                rx.text("Agriculture", size="2", weight="medium", color="white"), 
                                rx.spacer(), 
                                rx.icon(tag="chevron-down", size=16, color="white"),
                                spacing="3", width="100%", align="center"
                            ),
                            on_click=MenuState.toggle_agriculture, 
                            variant="ghost", width="100%", padding="12px 16px", justify="between",
                            _hover={"background": "rgba(212, 175, 55, 0.15)", "border_radius": "12px"}
                        ),
                        rx.cond(
                            MenuState.is_agriculture_open, 
                            rx.vstack(
                                sidebar_item("Cartographie", "map", "/admin/map"),
                                sidebar_item("Opérations", "list-todo", "/admin/operations"),
                                width="100%", padding_left="1em", spacing="1"
                            )
                        ),
                        width="100%", spacing="0"
                    ),
                    
                    sidebar_item("Paramètres", "settings", "/admin/settings"),
                    rx.spacer(),
                    width="100%", height="100%",
                ),
                # Comportement Responsive : Glissement tiroir sur mobile, statique sur grand écran
                position={"initial": "fixed", "md": "sticky"},
                top="0",
                left="0",
                height="100vh",
                width={"initial": "95%", "sm": "320px"},
                max_width="340px",
                background="linear-gradient(180deg, #113832 0%, #0c2824 100%)", 
                padding="2em 1.5em",
                z_index="999",
                transition="transform 0.35s cubic-bezier(0.4, 0, 0.2, 1)",
                transform=rx.cond(
                    MenuState.is_menu_open,
                    "translateX(0)",
                    {"initial": "translateX(-100%)", "md": "translateX(0)"}
                ),
                box_shadow={"initial": "10px 0 30px rgba(0,0,0,0.5)", "md": "none"}
            ),

            # Contenu principal de la page
            rx.vstack(
                rx.hstack(
                    # Bouton Hamburger visible uniquement sur mobile pour ouvrir le menu
                    rx.button(
                        rx.icon(tag="menu", size=22, color="#113832"),
                        on_click=MenuState.toggle_menu,
                        background="white",
                        border="1px solid #e0e0e0",
                        border_radius="10px",
                        box_shadow="0 2px 5px rgba(0,0,0,0.05)",
                        variant="solid",
                        display={"initial": "flex", "md": "none"}
                    ),
                    rx.spacer(),
                    rx.hstack(
                        rx.text("Admin • AGUIFERME", size="2", weight="medium", color="#555"),
                        rx.avatar(fallback="AG", size="2", border_radius="50px", border="2px solid #d4af37"),
                        spacing="3", align="center"
                    ),
                    width="100%", padding="1em 2em", background="white", 
                    border_bottom="1px solid #eaeaea", box_shadow="0 4px 20px rgba(0,0,0,0.03)"
                ),
                rx.box(content, width="100%", padding={"initial": "1em", "md": "2.5em"}, overflow_y="auto"),
                width="100%", background="#f7f9f8", min_height="100vh", flex="1", spacing="0"
            ),
            width="100%", position="relative"
        ),
        width="100%", min_height="100vh"
    )