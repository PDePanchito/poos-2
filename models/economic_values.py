from datetime import datetime

from config.database import Database


class EconomicValues:
    def __init__(self, index_code: str, date: str, value: float, requested_at: datetime = None,
                 username: str = None, source: str = None):
        self.index_code = index_code
        self.date = date
        self.value = value
        self.requested_at = requested_at
        self.username = username
        self.source = source

    def save_to_db(self, db: Database):
        try:
            existing = db.fetch_all(
                "SELECT id FROM economic_values WHERE index_code = %s AND date = %s",
                (self.index_code, self.date),
            )
            if existing:
                return
            db.execute(
                "INSERT INTO economic_values (index_code, date, value, requested_at, username, source) VALUES (%s,%s,%s,%s,%s,%s)",
                (
                    self.index_code,
                    self.date,
                    self.value,
                    self.requested_at,
                    self.username,
                    self.source,
                ),
            )
        except Exception as exc:
            print("Ocurrió un error al guardar los valores económicos:", exc)
