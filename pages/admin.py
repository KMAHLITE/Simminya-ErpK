import reflex as rx
import sqlmodel
from models.models import User

class AuthState(rx.State):
    reg_nom_prenom: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_telephone: str = ""
    reg_error: str = ""
    reg_success: str = ""

    login_email: str = ""
    login_password: str = ""
    login_error: str = ""

    show_password: bool = False

    is_authenticated: bool = False
    current_user_name: str = ""
    current_user_email: str = ""
    current_user_role: str = ""

    @rx.event
    def toggle_password(self):
        self.show_password = not self.show_password

    @rx.event
    def set_reg_nom_prenom(self, value: str):
        self.reg_nom_prenom = value

    @rx.event
    def set_reg_email(self, value: str):
        self.reg_email = value

    @rx.event
    def set_reg_telephone(self, value: str):
        self.reg_telephone = value

    @rx.event
    def set_reg_password(self, value: str):
        self.reg_password = value

    @rx.event
    def set_login_email(self, value: str):
        self.login_email = value

    @rx.event
    def set_login_password(self, value: str):
        self.login_password = value

    def check_is_setup(self):
        with rx.session() as session:
            count = session.exec(sqlmodel.select(sqlmodel.func.count(User.id))).first()
            return count == 0

    @rx.event
    async def register(self):
        if not self.reg_nom_prenom or not self.reg_email or not self.reg_password or not self.reg_telephone:
            self.reg_error = "Veuillez remplir tous les champs du formulaire."
            self.reg_success = ""
            return
        
        with rx.session() as session:
            existing_user = session.exec(
                sqlmodel.select(User).where(User.email == self.reg_email)
            ).first()

            if existing_user:
                self.reg_error = "Un compte existe déjà avec cet email."
                self.reg_success = ""
                return
            
            is_first = self.check_is_setup()
            assigned_role = "superadmin" if is_first else "client"

            new_user = User(
                nom_prenom=self.reg_nom_prenom,
                email=self.reg_email,
                password_hash=self.reg_password,
                telephone=self.reg_telephone,
                role=assigned_role
            )
            session.add(new_user)
            session.commit()
        
        self.reg_error = ""
        self.reg_success = "Compte créé avec succès !"
        return rx.redirect("/admin")

    @rx.event
    async def login(self):
        with rx.session() as session:
            user = session.exec(
                sqlmodel.select(User).where(User.email == self.login_email)
            ).first()

            if user and user.password_hash == self.login_password:
                self.is_authenticated = True
                self.current_user_name = user.nom_prenom
                self.current_user_email = user.email
                self.current_user_role = user.role
                self.login_error = ""
                return rx.redirect("/admin")
            else:
                self.login_error = "Email ou mot de passe incorrect."

    def logout(self):
        self.is_authenticated = False
        return rx.redirect("/login")