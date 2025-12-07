from datetime import datetime

import requests
from tabulate import tabulate

from models.economic_values import EconomicValues


class EconomicService:
    BASE_URL = "https://mindicador.cl/api/"

    @staticmethod
    def available_indexes():
        return ["UF", "IVP", "IPC", "UTM", "Dolar", "Euro"]

    @staticmethod
    def _extract_date(date_str):
        return date_str.split("T")[0]

    def _save_data(self, username, db, index_code, index_data):
        series = index_data['serie']
        for index in series:
            economic_record = EconomicValues(
                index_code=index_code,
                date=self._extract_date(index['fecha']),
                value=index['valor'],
                requested_at=datetime.now(),
                username=username,
                source=self.BASE_URL
            )
            economic_record.save_to_db(db)
        print("Datos guardados en la base de datos.")

    def _tabulate_data(self, data):
        series = data['serie']
        table_data = [(item['fecha'], item['valor']) for item in series]
        headers = ["Fecha", "Valor"]
        return tabulate(table_data, headers, tablefmt="grid")

    def fetch_data(self, index):
        try:
            response = requests.get(f"{self.BASE_URL}{index}")
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"Ocurrio un error al obtener los datos: {e}")

    def fetch_and_save(self, username, db, index, to_save):
        data = self.fetch_data(index)
        if to_save:
            self._save_data(username, db, index, data)
            print(f"Datos del índice {index} guardados correctamente.")
        table = self._tabulate_data(data)
        print(f"\nDatos del índice {index.upper()}:\n")
        print(table)
        return "success"
