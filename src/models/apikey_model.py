from src.models.database_model import DatabaseModel
from datetime import datetime

class ApiKeyModel:
    """Gère les exchanges et les clés API liées aux comptes"""

    def __init__(self, db_model=None):
        self.db = db_model if db_model else DatabaseModel()

    # Exchanges
    def get_exchanges(self):
        try:
            self.db.cursor.execute("SELECT exchange_id, name, display_name FROM exchanges ORDER BY display_name")
            rows = self.db.cursor.fetchall()
            return [{"exchange_id": row[0], "name": row[1], "display_name": row[2]} for row in rows]
        except Exception as e:
            self.db.logger.log_error(f"Erreur récupération exchanges: {e}")
            return []

    def get_exchange_by_name(self, name):
        try:
            self.db.cursor.execute("SELECT exchange_id, name, display_name FROM exchanges WHERE name = ?", (name.lower(),))
            row = self.db.cursor.fetchone()
            if row:
                return {"exchange_id": row[0], "name": row[1], "display_name": row[2]}
            return None
        except Exception as e:
            self.db.logger.log_error(f"Erreur get_exchange_by_name: {e}")
            return None

    def add_exchange(self, name, display_name):
        try:
            self.db.cursor.execute(
                "INSERT INTO exchanges (name, display_name) VALUES (?, ?)",
                (name.lower(), display_name)
            )
            self.db.connection.commit()
            return True, "Exchange ajouté"
        except Exception as e:
            self.db.logger.log_error(f"Erreur ajout exchange: {e}")
            return False, str(e)

    # API keys
    def get_api_keys_for_user(self, user_id):
        try:
            query = """
                SELECT ak.api_key_id, ak.account_id, ak.fk_exchange_id, ak.api_key, ak.api_secret, e.display_name
                FROM api_keys ak
                JOIN exchanges e ON ak.fk_exchange_id = e.exchange_id
                WHERE ak.account_id = ?
                ORDER BY e.display_name
            """
            self.db.cursor.execute(query, (user_id,))
            rows = self.db.cursor.fetchall()
            return [
                {
                    "api_key_id": row[0],
                    "account_id": row[1],
                    "exchange_id": row[2],
                    "api_key": row[3],
                    "api_secret": row[4],
                    "exchange_display": row[5]
                } for row in rows
            ]
        except Exception as e:
            self.db.logger.log_error(f"Erreur récupération api keys: {e}")
            return []

    def add_api_key(self, account_id, exchange_id, api_key, api_secret):
        try:
            self.db.cursor.execute(
                "INSERT INTO api_keys (account_id, fk_exchange_id, api_key, api_secret, created_at) VALUES (?, ?, ?, ?, ?)",
                (account_id, exchange_id, api_key, api_secret, datetime.now())
            )
            self.db.connection.commit()
            return True, "Clé API ajoutée"
        except Exception as e:
            self.db.logger.log_error(f"Erreur ajout api key: {e}")
            return False, str(e)

    def delete_api_key(self, api_key_id):
        try:
            self.db.cursor.execute("DELETE FROM api_keys WHERE api_key_id = ?", (api_key_id,))
            self.db.connection.commit()
            return True, "Clé API supprimée"
        except Exception as e:
            self.db.logger.log_error(f"Erreur suppression api key: {e}")
            return False, str(e)
