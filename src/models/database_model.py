import sqlite3
import os
from src.utils.db_logger import DbLogger

class DatabaseModel:
    """Gestion de la connexion et initialisation de la base de données SQLite"""
    
    def __init__(self, db_path="datas/kipacoin.db"):
        """
        Initialise la connexion à la base de données
        
        Args:
            db_path (str): Chemin vers le fichier de base de données
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.logger = DbLogger()
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        self._connect()
    
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