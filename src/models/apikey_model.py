from src.models.database_model import DatabaseModel
from datetime import datetime
from src.utils.crypto_utils import encrypt_secret, decrypt_secret

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
                SELECT ak.api_key_id, ak.fk_account_id, ak.fk_exchange_id, ak.api_key, ak.api_secret, e.display_name, ak.label
                FROM api_keys ak
                JOIN exchanges e ON ak.fk_exchange_id = e.exchange_id
                WHERE ak.fk_account_id = ?
                ORDER BY e.display_name
            """
            self.db.cursor.execute(query, (user_id,))
            rows = self.db.cursor.fetchall()
            result = []
            for row in rows:
                try:
                    secret_decrypted = decrypt_secret(row[4]) if row[4] else ''
                except Exception:
                    secret_decrypted = ''
                result.append({
                    "api_key_id": row[0],
                    "account_id": row[1],
                    "exchange_id": row[2],
                    "api_key": row[3],
                    "api_secret": secret_decrypted,
                    "exchange_display": row[5],
                    "label": row[6]
                })
            return result
        except Exception as e:
            self.db.logger.log_error(f"Erreur récupération api keys: {e}")
            return []

    def add_api_key(self, account_id, exchange_id, api_key, api_secret, label=None):
        try:
            # Chiffrer le secret avant stockage
            secret_encrypted = encrypt_secret(api_secret) if api_secret else ''
            print(f"[DEBUG ADD_API_KEY] account_id={account_id}, exchange_id={exchange_id}, label={label}")
            self.db.cursor.execute(
                "INSERT INTO api_keys (fk_account_id, fk_exchange_id, api_key, api_secret, label, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (account_id, exchange_id, api_key, secret_encrypted, label, datetime.now())
            )
            print(f"[DEBUG ADD_API_KEY] INSERT exécuté, rowcount={self.db.cursor.rowcount}")
            self.db.connection.commit()
            print(f"[DEBUG ADD_API_KEY] COMMIT réussi")
            return True, "Clé API ajoutée"
        except Exception as e:
            print(f"[DEBUG ADD_API_KEY] ERREUR: {e}")
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

    def update_api_key(self, api_key_id, api_key, api_secret, label=None):
        try:
            # Chiffrer le secret avant stockage
            secret_encrypted = encrypt_secret(api_secret) if api_secret else ''
            print(f"[DEBUG UPDATE_API_KEY] api_key_id={api_key_id}, label={label}")
            self.db.cursor.execute(
                "UPDATE api_keys SET api_key = ?, api_secret = ?, label = ? WHERE api_key_id = ?",
                (api_key, secret_encrypted, label, api_key_id)
            )
            print(f"[DEBUG UPDATE_API_KEY] UPDATE exécuté, rowcount={self.db.cursor.rowcount}")
            self.db.connection.commit()
            print(f"[DEBUG UPDATE_API_KEY] COMMIT réussi")
            return True, "Clé API modifiée"
        except Exception as e:
            print(f"[DEBUG UPDATE_API_KEY] ERREUR: {e}")
            self.db.logger.log_error(f"Erreur modification api key: {e}")
            return False, str(e)
