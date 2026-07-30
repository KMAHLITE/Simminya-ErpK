import reflex as rx

class MenuState(rx.State):
    is_agriculture_open: bool = False
    is_menu_open: bool = True

    def toggle_menu(self):
        self.is_menu_open = not self.is_menu_open
    
    def toggle_agriculture(self):
        self.is_agriculture_open = not self.is_agriculture_open

def sidebar_item(text: str, icon: str, href: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(tag=icon, size=30),
            rx.text(text, size="3", weight="regular"),
            spacing="3", padding="10px", color="white",
        ),
        href=href, width="100%",
        _hover={"background": "rgba(255, 255, 255, 0.1)", "border_radius": "8px"},
    )

def dashboard_layout(content: rx.Component) -> rx.Component:
    return rx.hstack(
        rx.cond(
            MenuState.is_menu_open,
            rx.vstack(
                rx.hstack(rx.image(src="/logo.png", width="25px"), rx.heading("SIMMINYA", size="5", color="white", weight="light")),
                rx.divider(color="rgba(255,255,255,0.5)", margin_y="0.75em", box_shadow="0 5px 10px rgba(0,0,0,0.15)"),
                
                sidebar_item("Tableau de bord", "layout-dashboard", "/admin"),
                sidebar_item("Ferme", "building-2", "/admin/ferme"),
                
                # Section Agriculture alignée avec les autres onglets principaux
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
                width="280px", height="100vh", background="#1a4d44", padding="1.5em",
            )
        ),
        rx.vstack(
            rx.hstack(
                rx.button(
                    rx.icon(tag=rx.cond(MenuState.is_menu_open, "x", "menu")),
                    on_click=MenuState.toggle_menu,
                    background=rx.cond(MenuState.is_menu_open, "transparent", "transparent"),
                    color=rx.cond(MenuState.is_menu_open, "#1a4d44", "#1a4d44"),
                    variant=rx.cond(MenuState.is_menu_open, "solid", "ghost")
                ),
                rx.spacer(),
                rx.avatar(fallback="AF", size="2", margin_right="1em", border_radius="50px", border="1px solid #1a4d44"),
                width="100%", padding="1em", border_bottom="1px solid #e0e0e0", border_radius="10px", box_shadow="0 2px 5px rgba(0,0,0,0.15)"
            ),
            rx.box(content, width="100%", padding="2em", overflow_y="auto"),
            width="100%", background="#f4f6f8", height="100vh", spacing="0"
        ),
        spacing="0"
    )