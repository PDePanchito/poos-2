from abstracts.module_access import ModuleAccess
from models.security import Security
from models.user import User
from getpass import getpass


class UserController(ModuleAccess):
    ALLOWED_ROLES = [
        "admin"
    ]

    def __init__(self, db):
        self.db = db
        self.create_initial_user()

    def create_initial_user(self):
        if self.db.is_user_data_empty():
            self.create_user()

    def create_user(self):
        cleaned_username = Security.clean_text(input("Ingresa el usuario: "))
        if not cleaned_username:
            print("Debes ingresar un usuario")
            return

        password = getpass("Ingresa la contraseña: ")
        if len(password) < 8:
            print("La contraseña debe tener al menos 8 caracteres")
            return
        role = Security.clean_text(input("Ingresa el rol (admin/user/manager): "))
        if role not in ["admin", "user", "manager"]:
            print("Rol inválido. Usando 'user' por defecto.")
            role = "user"
        user = User(cleaned_username, password, role=role)
        return user.create_user(self.db, password)

    def login(self):
        username = Security.clean_text(input("Usuario: "))
        password = getpass("Contraseña: ")
        user = User.authenticate(self.db, username, password)
        if user:
            print(f"Bienvenido, {user.username}! Rol: {user.get_user_role()}")
            return user
        else:
            print("Autenticación fallida. Usuario o contraseña incorrectos.")
            return None
