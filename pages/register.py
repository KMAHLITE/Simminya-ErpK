import reflex as rx
import httpx

class RegisterState(rx.State):
    email: str = ""
    nom: str = ""
    prenom: str = ""
    telephone: str = ""
    password: str = ""
    show_password: bool = False

    @rx.event
    def set_email(self, value: str): self.email = value
    @rx.event
    def set_nom(self, value: str): self.nom = value
    @rx.event
    def set_prenom(self, value: str): self.prenom = value
    @rx.event
    def set_telephone(self, value: str): self.telephone = value
    @rx.event
    def set_password(self, value: str): self.password = value

    def toggle_password(self):
        self.show_password = not self.show_password

    @rx.event
    async def handle_register(self):
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "email": self.email, 
                    "nom": self.nom, 
                    "prenom": self.prenom, 
                    "telephone": self.telephone,
                    "password": self.password
                }
                response = await client.post("http://localhost:8001/api/v1/auth/inscription", json=payload)
                if response.status_code == 201:
                    return rx.redirect("/admin")
                return rx.window_alert(f"Erreur : {response.text}")
            except Exception as e:
                return rx.window_alert(f"Erreur : {str(e)}")

def register() -> rx.Component:
    return rx.box(
        rx.box(position="absolute", width="100vw", height="100vh", z_index="0", 
               background_image="url('/logo.png')", background_size="cover", background_position="center", opacity="0.75"),
        rx.center(
            rx.card(
                rx.vstack(
                    rx.image(src="/logo.png", width="100px", height="80px"),
                    rx.heading("Inscription", size="7", color="grass", weight="light"),
                    rx.input(placeholder="Nom", on_change=RegisterState.set_nom, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                    rx.input(placeholder="Prénom", on_change=RegisterState.set_prenom, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                    rx.input(placeholder="Email", on_change=RegisterState.set_email, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                    rx.input(placeholder="Numéro de téléphone", on_change=RegisterState.set_telephone, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                    rx.hstack(
                        rx.input(placeholder="Mot de passe", type=rx.cond(RegisterState.show_password, "text", "password"), 
                                 on_change=RegisterState.set_password, width="100%", radius="full", background="rgba(255, 255, 255, 0.1)"),
                        rx.icon(tag=rx.cond(RegisterState.show_password, "eye", "eye-off"), on_click=RegisterState.toggle_password, cursor="pointer", margin_left="-40px"),
                        width="100%", align="center"
                    ),
                    rx.button("S'inscrire", on_click=RegisterState.handle_register, width="60%", radius="full", color_scheme="grass"),
                    rx.text("Déjà un compte ? ", rx.link("Se connecter", href="/login", color="grass"), size="2"),
                    spacing="5", width="100%", align="center", padding="2em"
                ),
                width=["90%", "450px"], background="rgba(255, 255, 255, 0.1)", border_radius="30px"
            ),
            style={"backdrop_filter": "blur(3px)"},
            width="100vw", height="100vh", position="relative", z_index="1"
        )
    )