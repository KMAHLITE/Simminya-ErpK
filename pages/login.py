import reflex as rx
from states.auth import AuthState  # Assurez-vous d'importer votre AuthState

@rx.page(route="/login", title="AGUIFERME - Connexion")
def login() -> rx.Component:
    return rx.box(
        rx.box(position="absolute", width="100vw", height="100vh", z_index="0", 
               background_image="url('/logo.png')", background_size="cover", background_position="center", opacity="0.75"),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.image(src="/logo.png", width="100px", height="80px", margin_bottom="1em"),
                    rx.heading("Connexion", size="7", color="grass", weight="light"),
                    
                    rx.cond(
                        AuthState.login_error != "",
                        rx.text(AuthState.login_error, color="red", size="2")
                    ),

                    rx.input(placeholder="Email", on_change=AuthState.set_login_email, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                    rx.hstack(
                        rx.input(placeholder="Mot de passe", type=rx.cond(AuthState.show_password, "text", "password"), 
                                 on_change=AuthState.set_login_password, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                        rx.icon(tag=rx.cond(AuthState.show_password, "eye", "eye-off"), on_click=AuthState.toggle_password, cursor="pointer", margin_left="-40px"),
                        width="100%", align="center"
                    ),
                    
                    # Appel direct de la méthode login de AuthState avec redirection intégrée
                    rx.button("Se connecter", on_click=AuthState.login, width="60%", radius="full", color_scheme="grass"),
                    
                    rx.text("Pas de compte ? ", rx.link("S'inscrire", href="/register", color="grass")),
                    spacing="5", align="center", padding="2em", width="100%"
                ),
                style={"backdrop_filter": "blur(3px)"},
                width=["90%", "450px"], background="rgba(255, 255, 255, 0.2)", border_radius="30px"
            ),
            width="100vw", height="100vh", position="relative", z_index="1"
        )
    )