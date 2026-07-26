import reflex as rx

class AuthState(rx.State):
    """
    State (Backend) gérant l'authentification et l'inscription pour Simminya.
    """
    # Champs pour l'inscription
    reg_nom_prenom: str = ""
    reg_email: str = ""
    reg_password: str = ""
    reg_telephone: str = ""
    reg_error: str = ""

    # Champs pour la connexion
    login_email: str = "" # Remplacé par l'email pour la connexion
    login_password: str = ""
    login_error: str = ""

    # Base de données simulée stockant les utilisateurs par email
    # Format : { "email": {"password": "...", "nom_prenom": "...", "telephone": "..."} }
    users_db: dict[str, dict] = {
        "admin@simminya.com": {
            "password": "password123",
            "nom_prenom": "Administrateur Simminya",
            "telephone": "+224000000000"
        }
    } 
    
    is_authenticated: bool = False
    current_user: str = ""

    def register(self):
        """Logique d'inscription d'un nouvel utilisateur avec tous les champs requis."""
        if not self.reg_nom_prenom or not self.reg_email or not self.reg_password or not self.reg_telephone:
            self.reg_error = "Veuillez remplir tous les champs du formulaire."
            return
        
        if self.reg_email in self.users_db:
            self.reg_error = "Un compte existe déjà avec cet email."
            return
        
        # Enregistrement des informations de l'utilisateur
        self.users_db[self.reg_email] = {
            "password": self.reg_password,
            "nom_prenom": self.reg_nom_prenom,
            "telephone": self.reg_telephone
        }
        
        # Réinitialisation et redirection vers la page de login
        self.reg_error = ""
        self.reg_nom_prenom = ""
        self.reg_email = ""
        self.reg_password = ""
        self.reg_telephone = ""
        
        return rx.redirect("/login")

    def login(self):
        """Logique de connexion basée sur l'email."""
        if self.login_email in self.users_db and self.users_db[self.login_email]["password"] == self.login_password:
            self.is_authenticated = True
            self.current_user = self.users_db[self.login_email]["nom_prenom"]
            self.login_error = ""
            self.login_email = ""
            self.login_password = ""
            return rx.redirect("/admin")
        else:
            self.login_error = "Email ou mot de passe incorrect."

    def logout(self):
        """Déconnexion de l'utilisateur."""
        self.is_authenticated = False
        self.current_user = ""
        return rx.redirect("/")