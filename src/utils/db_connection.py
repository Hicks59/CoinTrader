"""
Utilitaire centralisé pour gérer les connexions à la base de données SQLite
"""
import sqlite3
from contextlib import contextmanager
from src.utils.db_logger import DbLogger

DB_PATH = 'datas/cointrader.db'


def get_db_connection(db_path=DB_PATH):
    """
    Crée et retourne une connexion à la base de données
    
    Args:
        db_path (str): Chemin vers le fichier de base de données
        
    Returns:
        sqlite3.Connection: Connexion à la base de données
    """
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as e:
        logger = DbLogger()
        error_msg = f"Erreur de connexion à {db_path}: {e}"
        logger.log_error(error_msg)
        raise


@contextmanager
def get_db_context(db_path=DB_PATH):
    """
    Context manager pour gérer automatiquement la connexion et le curseur
    Ferme la connexion après utilisation
    
    Args:
        db_path (str): Chemin vers le fichier de base de données
        
    Yields:
        tuple: (connection, cursor)
    """
    conn = None
    try:
        conn = get_db_connection(db_path)
        cursor = conn.cursor()
        yield conn, cursor
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        logger = DbLogger()
        logger.log_error(f"Erreur lors de l'opération DB: {e}")
        raise
    finally:
        if conn:
            conn.close()
