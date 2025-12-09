from abstracts.module_access import ModuleAccess
from config.database import Database
from models.security import Security
from services.economic_index import EconomicService


class EconomicIndexController(ModuleAccess):
    ALLOWED_ROLES = [
        "user",
        "admin"
    ]

    def __init__(self, db: Database):
        self.db = db

    def fetch_economic_data(self, username, date=None):
        print("\nÍndices Económicos Disponibles:")
        self._economic_index_menu()
        index = Security.clean_text(input("Ingrese el nombre del índice económico que desea consultar: ")).lower()
        to_save = Security.clean_text(input("¿Desea guardar los datos en la base de datos? (s/n): ")).lower()
        to_save = True if to_save == "s" else False
        economic_service = EconomicService()
        economic_data = economic_service.fetch_and_save(username, self.db, index, to_save, date)
        if economic_data == "error":
            print("No se pudo completar la operación.")
            return
        print("Operación completada con éxito.")

    def _economic_index_menu(self):
        indexes = self._get_available_indexes()
        for index in indexes:
            print(f"- {index}")

    def _get_available_indexes(self):
        return EconomicService.available_indexes()
