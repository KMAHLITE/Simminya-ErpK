import reflex as rx
from states.auth import AuthState  # Assurez-vous que l'import pointe vers votre AuthState

def login() -> rx.Component:
    return rx.box(
        rx.box(
            position="absolute", 
            width="100vw", 
            height="100vh", 
            z_index="0", 
            background_image="url('/logo.png')", 
            background_size="cover", 
            background_position="center", 
            opacity="0.75"
        ),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.image(src="/logo.png", width="100px", height="80px"),
                    rx.heading("Connexion", size="7", color="grass", weight="light"),
                    
                    # Affichage des erreurs de connexion du AuthState
                    rx.cond(
                        AuthState.login_error != "",
                        rx.text(AuthState.login_error, color="red", size="2")
                    ),

                    rx.input(
                        placeholder="Email", 
                        on_change=AuthState.set_login_email, 
                        width="100%", 
                        radius="full", 
                        background="rgba(255, 255, 255, 0.1)"
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Mot de passe", 
                            type=rx.cond(AuthState.show_password, "text", "password"), 
                            on_change=AuthState.set_login_password, 
                            width="100%", 
                            radius="full", 
                            background="rgba(255, 255, 255, 0.1)"
                        ),
                        rx.icon(
                            tag=rx.cond(AuthState.show_password, "eye", "eye-off"), 
                            on_click=AuthState.toggle_password, 
                            cursor="pointer", 
                        ),
                        width="100%", 
                        align="center"
                    ),
                    rx.button(
                        "Se connecter", 
                        on_click=AuthState.login, 
                        width="60%", 
                        radius="full", 
                        color_scheme="grass"
                    ),
                    rx.text(
                        "Pas encore de compte ? ", 
                        rx.link("S'inscrire", href="/register", color="grass"), 
                        size="2"
                    ),
                    spacing="5", 
                    width="100%", 
                    align="center", 
                    padding="2em"
                ),
                width=["90%", "450px"], 
                background="rgba(255, 255, 255, 0.1)", 
                border_radius="30px"
            ),
            style={"backdrop_filter": "blur(3px)"},
            width="100vw", 
            height="100vh", 
            position="relative", 
            z_index="1"
        )
    )