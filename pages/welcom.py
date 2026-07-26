import reflex as rx
import asyncio

class WelcomeState(rx.State):
    show_content: bool = False

    @rx.event
    async def run_animation(self):
        await asyncio.sleep(0.5)
        self.show_content = True
        yield
        await asyncio.sleep(2.5)
        yield rx.redirect("/login")

def welcome() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.image(
                src="/logo.png",
                width=["70%","70%", "70%"],
                height=["40%","60%", "50%"],
                transition="all 1.2s ease-out",
            ),
            rx.text(
                "PRODUIRE AUJOURD'HUI, NOURRIR DEMAIN",
                size="4",
                weight="light",
                opacity=rx.cond(WelcomeState.show_content, 1, 0),
                transition="opacity 1.5s ease-in-out",
            ),
            rx.progress(
                is_indeterminate=True,
                width="200px",
                opacity=rx.cond(WelcomeState.show_content, 1, 0),
                transition="opacity 1s ease-in-out",
            ),
            spacing="8",
            align="center",
        ),
        width="100vw",
        height="100vh",
        background_color="#FEFEFE",
        on_mount=WelcomeState.run_animation,
    )