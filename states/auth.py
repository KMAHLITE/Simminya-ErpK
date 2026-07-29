import reflex as rx
import sqlmodel
from models.models import User

class AuthState(rx.State):
    """
    State gérant l'authentification, les inscriptions et la hiérarchie des rôles.
    """
    # Champs pour l'inscription publique (Clients)
    reg_nom_prenom: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_telephone: str = ""
    reg_error: str = ""
    reg_success: str = ""

    # Champs pour la connexion
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""

    # Gestion de la visibilité du mot de passe pour les formulaires
    show_password: bool = False

    # Champs pour l'ajout d'un Admin (Réservé au Super Admin)
    new_admin_nom: str = ""
    new_admin_email: str = ""
    new_admin_password: str = ""
    new_admin_telephone: str = ""
    admin_error: str = ""
    admin_success: str = ""

    # Session utilisateur connecté
    is_authenticated: bool = False
    current_user_name: str = ""
    current_user_email: str = ""
    current_user_role: str = ""  # "superadmin", "admin", ou "client"

    @rx.event
    def toggle_password(self):
        """Bascule la visibilité du mot de passe."""
        self.show_password = not self.show_password

    # Setters pour l'inscription
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

    # Setters pour la connexion
    @rx.event
    def set_login_email(self, value: str):
        self.login_email = value

    @rx.event
    def set_login_password(self, value: str):
        self.login_password = value

    def check_is_setup(self):
        """
        Si aucun utilisateur n'existe dans la base, 
        le tout premier inscrit devient automatiquement Super Admin.
        """
        with rx.session() as session:
            count = session.exec(sqlmodel.select(sqlmodel.func.count(User.id))).first()
            return count == 0

    @rx.event
    async def register(self):
        """Inscription publique standard."""
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
        
        # Redirection explicite vers /admin
        return rx.redirect("/admin")

    @rx.event
    async def login(self):
        """Connexion de l'utilisateur."""
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
                
                # Redirection vers /admin si admin, sinon page d'accueil ou autre
                if user.role in ["superadmin", "admin"]:
                    return rx.redirect("/admin")
                else:
                    return rx.redirect("/")
            else:
                self.login_error = "Email ou mot de passe incorrect."

    @rx.event
    async def create_admin_by_superadmin(self):
        if self.current_user_role != "superadmin":
            self.admin_error = "Action non autorisée."
            return

        if not self.new_admin_nom or not self.new_admin_email or not self.new_admin_password or not self.new_admin_telephone:
            self.admin_error = "Veuillez remplir tous les champs."
            return

        with rx.session() as session:
            existing = session.exec(
                sqlmodel.select(User).where(User.email == self.new_admin_email)
            ).first()

            if existing:
                self.admin_error = "Cet email est déjà utilisé."
                return

            new_admin = User(
                nom_prenom=self.new_admin_nom,
                email=self.new_admin_email,
                password_hash=self.new_admin_password,
                telephone=self.new_admin_telephone,
                role="admin"
            )
            session.add(new_admin)
            session.commit()

        self.admin_error = ""
        self.admin_success = "Administrateur créé avec succès !"
        self.new_admin_nom = ""
        self.new_admin_email = ""
        self.new_admin_password = ""
        self.new_admin_telephone = ""

    def logout(self):
        self.is_authenticated = False
        self.current_user_name = ""
        self.current_user_email = ""
        self.current_user_role = ""
        return rx.redirect("/login")