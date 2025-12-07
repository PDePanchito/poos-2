from models.security import Security
from models.user import User


class UserController:
    def __init__(self, db):
        self.db = db

    def create_user(self):
        cleaned_username = Security.clean_text(input("Ingresa el usuario: "))
        password_hash = Security.clean_text(input("Ingresa la contraseña: "))
        role = Security.clean_text(input("Ingresa el rol (admin/user/manager): "))
        if role not in ["admin", "user", "manager"]:
            print("Rol inválido. Usando 'user' por defecto.")
            role = "user"
        user = User(cleaned_username, password_hash, role=role)
        return user.create_user(self.db, password_hash)

    def login(self):
        username = Security.clean_text(input("Usuario: "))
        password = input("Contraseña: ")
        user = User.authenticate(self.db, username, password)
        if user:
            print(f"Bienvenido, {user.username}! Rol: {user.get_user_role()}")
            return user
        else:
            print("Autenticación fallida. Usuario o contraseña incorrectos.")
            return None
