import reflex as rx
import httpx

class LoginState(rx.State):
    username: str = ""
    password: str = ""
    show_password: bool = False

    @rx.event
    def set_username(self, value: str): self.username = value
    @rx.event
    def set_password(self, value: str): self.password = value

    def toggle_password(self):
        self.show_password = not self.show_password

    @rx.event
    async def handle_login(self):
        async with httpx.AsyncClient() as client:
            try:
                payload = {"username": self.username, "password": self.password}
                response = await client.post("http://localhost:8001/api/v1/auth/login", data=payload)
                if response.status_code == 200:
                    return rx.redirect("/admin")
                return rx.window_alert(f"Erreur : {response.text}")
            except Exception as e:
                return rx.window_alert(f"Erreur de connexion : {str(e)}")

def login() -> rx.Component:
    return rx.box(
        rx.box(position="absolute", width="100vw", height="100vh", z_index="0", 
               background_image="url('/logo.png')", background_size="cover", background_position="center", opacity="0.75"),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.image(src="/logo.png", width="100px", height="80px", margin_bottom="1em"),
                    rx.heading("Connexion", size="7", color="grass", weight="light"),
                    rx.input(placeholder="Email", on_change=LoginState.set_username, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                    rx.hstack(
                        rx.input(placeholder="Mot de passe", type=rx.cond(LoginState.show_password, "text", "password"), 
                                 on_change=LoginState.set_password, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                        rx.icon(tag=rx.cond(LoginState.show_password, "eye", "eye-off"), on_click=LoginState.toggle_password, cursor="pointer", margin_left="-40px"),
                        width="100%", align="center"
                    ),
                    rx.button("Se connecter", on_click=LoginState.handle_login, width="60%", radius="full", color_scheme="grass"),
                    rx.text("Pas de compte ? ", rx.link("S'inscrire", href="/register", color="grass")),
                    spacing="5", align="center", padding="2em", width="100%"
                ),
                style={"backdrop_filter": "blur(3px)"},
                width=["90%", "450px"], background="rgba(255, 255, 255, 0.2)", border_radius="30px"
            ),
            width="100vw", height="100vh", position="relative", z_index="1"
        )
    )