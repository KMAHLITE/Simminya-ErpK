import reflex as rx
from states.auth import AuthState

@rx.page(route="/register", title="AGUIFERME - Inscription")
def register() -> rx.Component:
    return rx.box(
        # Arrière-plan avec image et effet visuel
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
                    rx.heading("Inscription", size="7", color="#1a4d44", weight="light"),
                    
                    # Affichage des erreurs d'inscription
                    rx.cond(
                        AuthState.register_error != "",
                        rx.text(AuthState.register_error, color="red", size="2")
                    ),

                    rx.input(
                        placeholder="Nom et Prénom", 
                        on_change=AuthState.set_register_nom_prenom, 
                        width="100%", 
                        radius="full", 
                        background="rgba(255, 255, 255, 0.1)"
                    ),
                    rx.input(
                        placeholder="Email", 
                        on_change=AuthState.set_register_email, 
                        width="100%", 
                        radius="full", 
                        background="rgba(255, 255, 255, 0.1)"
                    ),
                    rx.hstack(
                        rx.input(
                            placeholder="Mot de passe", 
                            type=rx.cond(AuthState.show_password, "text", "password"), 
                            on_change=AuthState.set_register_password, 
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
                        "S'inscrire", 
                        on_click=AuthState.register_user, 
                        width="60%", 
                        radius="full", 
                        background="#1a4d44",
                        color="white"
                    ),
                    rx.text(
                        "Déjà un compte ? ", 
                        rx.link("Se connecter", href="/login", color="#1a4d44", weight="bold"), 
                        size="2"
                    ),
                    spacing="5", 
                    width="100%", 
                    align="center", 
                    padding="2em"
                ),
                width=["90%", "450px"], 
                background="rgba(255, 255, 255, 0.85)", 
                border_radius="30px",
                box_shadow="0 10px 25px rgba(0,0,0,0.15)"
            ),
            style={"backdrop_filter": "blur(3px)"},
            width="100vw", 
            height="100vh", 
            position="relative", 
            z_index="1"
        )
    )