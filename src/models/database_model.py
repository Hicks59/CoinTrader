import sqlite3
import os
from src.utils.db_logger import DbLogger

class DatabaseModel:
    """Gestion de la connexion et initialisation de la base de données SQLite"""

    _activity_logs_ready = False

    def __init__(self, db_path="datas/cointrader.db"):
        """
        Initialise la connexion à la base de données

        Args:
            db_path (str): Chemin vers le fichier de base de données
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.logger = DbLogger()

        is_new = not os.path.exists(db_path)
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self._connect()
        if is_new:
            self.init_database()
        self._ensure_activity_logs_table()

    def _ensure_activity_logs_table(self):
        """Crée la table activity_logs si elle n'existe pas (une seule fois par session)"""
        if DatabaseModel._activity_logs_ready:
            return
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS activity_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fk_account_id INTEGER NOT NULL,
                    action_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (fk_account_id) REFERENCES accounts(account_id) ON DELETE CASCADE
                )
            """)
            self.connection.commit()
            DatabaseModel._activity_logs_ready = True
        except Exception as e:
            self.logger.log_error(f"Erreur création table activity_logs: {e}")

    def log_activity(self, account_id, action_type, description):
        """Enregistre une action utilisateur dans activity_logs"""
        try:
            self.cursor.execute(
                "INSERT INTO activity_logs (fk_account_id, action_type, description) VALUES (?, ?, ?)",
                (account_id, action_type, description)
            )
            self.connection.commit()
        except Exception as e:
            self.logger.log_error(f"Erreur log_activity: {e}")

    def get_activity_logs(self, account_id, action_type=None):
        """Récupère les logs d'activité d'un utilisateur, avec filtre optionnel"""
        try:
            where = "WHERE fk_account_id = ?"
            params = [account_id]
            if action_type:
                where += " AND action_type = ?"
                params.append(action_type)
            self.cursor.execute(
                f"SELECT log_id, action_type, description, created_at FROM activity_logs "
                f"{where} ORDER BY created_at DESC",
                tuple(params)
            )
            rows = self.cursor.fetchall()
            return [
                {"log_id": r[0], "action_type": r[1], "description": r[2], "created_at": r[3]}
                for r in rows
            ]
        except Exception as e:
            self.logger.log_error(f"Erreur get_activity_logs: {e}")
            return []

    def _connect(self):
        """Établit la connexion à la base de données"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            self.logger.log_connection(self.db_path)
        except sqlite3.Error as e:
            error_msg = f"Erreur de connexion à {self.db_path}: {e}"
            self.logger.log_error(error_msg)
            raise
    
    def test_connection(self):
        """
        Test la connexion à la base de données
        
        Returns:
            bool: True si la connexion est active, False sinon
        """
        try:
            query = "SELECT 1"
            self.logger.log_query(query)
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            error_msg = f"Test de connexion échoué: {e}"
            self.logger.log_error(error_msg)
            return False
    
    def init_database(self, sql_file_path="init_project/init_database.sql"):
        """
        Initialise la base de données en exécutant le fichier SQL
        
        Args:
            sql_file_path (str): Chemin vers le fichier SQL d'initialisation
            
        Returns:
            bool: True si l'initialisation réussit, False sinon
        """
        try:
            if not os.path.exists(sql_file_path):
                error_msg = f"Fichier SQL introuvable : {sql_file_path}"
                self.logger.log_error(error_msg)
                return False
            
            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            self.logger.log_query(f"Execution du script d'initialisation : {sql_file_path}")
            
            self.cursor.executescript(sql_script)
            self.connection.commit()
            
            return True
            
        except sqlite3.Error as e:
            error_msg = f"Erreur lors de l'initialisation de la BDD: {e}"
            self.logger.log_error(error_msg)
            self.connection.rollback()
            return False
        except (IOError, OSError) as e:
            error_msg = f"Erreur de lecture du fichier SQL {sql_file_path}: {e}"
            self.logger.log_error(error_msg)
            return False
    
    def close(self):
        """Ferme la connexion à la base de données"""
        if self.connection:
            self.connection.close()
            self.logger.log_disconnection()
    
    def __enter__(self):
        """Support du context manager (with statement)"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Fermeture automatique avec context manager"""
        self.close()