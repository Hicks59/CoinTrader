import sqlite3
from datetime import datetime
from src.models.database_model import DatabaseModel

class BotModel:
    """Gestion des bots de trading"""
    
    def __init__(self, db_model=None):
        self.db = db_model if db_model else DatabaseModel()
    
    def create_bot(self, account_id, exchange_name, crypto_source, crypto_target, 
                   pourcentage_gain, montant_trade, type_ordre, 
                   prix_achat_cible=None):
        """
        Crée un nouveau bot de trading
        
        Args:
            account_id (int): ID du compte utilisateur
            exchange_name (str): Nom de l'exchange (ex: 'coinbase')
            crypto_source (str): Crypto à acheter (ex: 'BTC')
            crypto_target (str): Crypto pour payer (ex: 'USDC')
            pourcentage_gain (float): Pourcentage de gain souhaité
            montant_trade (float): Montant du trade en USDC
            type_ordre (str): Type d'ordre ('Market' ou 'Limit')
            prix_achat_cible (float, optional): Prix d'achat cible
            
        Returns:
            tuple: (success: bool, message: str, bot_id: int or None)
        """
        try:
            # Récupérer l'exchange_id
            self.db.cursor.execute(
                "SELECT id FROM exchanges WHERE name = ?",
                (exchange_name.lower(),)
            )
            exchange_result = self.db.cursor.fetchone()
            
            if not exchange_result:
                return False, f"Exchange '{exchange_name}' introuvable", None
            
            exchange_id = exchange_result[0]
            
            # Générer automatiquement le product_id
            product_id = f"{crypto_source}-{crypto_target}"
            
            # Insérer le bot
            query = """
                INSERT INTO bots (
                    account_id, exchange_id, crypto_source, crypto_target, 
                    product_id, prix_achat_cible, pourcentage_gain, 
                    montant_trade, type_ordre, is_active
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """
            
            self.db.cursor.execute(
                query,
                (account_id, exchange_id, crypto_source, crypto_target, 
                 product_id, prix_achat_cible, pourcentage_gain, 
                 montant_trade, type_ordre)
            )
            self.db.connection.commit()
            
            bot_id = self.db.cursor.lastrowid
            
            self.db.logger.log_query(f"Bot créé: {product_id} (ID: {bot_id})")
            
            return True, "Bot créé avec succès", bot_id
            
        except sqlite3.Error as e:
            error_msg = f"Erreur création bot: {e}"
            self.db.logger.log_error(error_msg)
            return False, "Erreur lors de la création du bot", None
    
    def get_user_bots(self, account_id):
        """
        Récupère tous les bots d'un utilisateur
        
        Args:
            account_id (int): ID du compte utilisateur
            
        Returns:
            list: Liste des bots avec leurs informations
        """
        try:
            query = """
                SELECT 
                    b.id, b.crypto_source, b.crypto_target, b.product_id,
                    b.prix_achat_cible, b.pourcentage_gain, b.montant_trade,
                    b.type_ordre, b.is_active, b.created_at,
                    e.display_name as exchange_name
                FROM bots b
                JOIN exchanges e ON b.exchange_id = e.id
                WHERE b.account_id = ?
                ORDER BY b.created_at DESC
            """
            
            self.db.cursor.execute(query, (account_id,))
            rows = self.db.cursor.fetchall()
            
            bots = []
            for row in rows:
                bots.append({
                    'id': row[0],
                    'crypto_source': row[1],
                    'crypto_target': row[2],
                    'product_id': row[3],
                    'prix_achat_cible': row[4],
                    'pourcentage_gain': row[5],
                    'montant_trade': row[6],
                    'type_ordre': row[7],
                    'is_active': row[8],
                    'created_at': row[9],
                    'exchange_name': row[10]
                })
            
            return bots
            
        except sqlite3.Error as e:
            error_msg = f"Erreur récupération bots: {e}"
            self.db.logger.log_error(error_msg)
            return []
    
    def toggle_bot_status(self, bot_id, is_active):
        """
        Active ou désactive un bot
        
        Args:
            bot_id (int): ID du bot
            is_active (bool): Nouveau statut
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            query = """
                UPDATE bots 
                SET is_active = ?, updated_at = ?
                WHERE id = ?
            """
            
            self.db.cursor.execute(
                query,
                (1 if is_active else 0, datetime.now(), bot_id)
            )
            self.db.connection.commit()
            
            status_text = "activé" if is_active else "désactivé"
            self.db.logger.log_query(f"Bot {status_text}: ID {bot_id}")
            
            return True, f"Bot {status_text} avec succès"
            
        except sqlite3.Error as e:
            error_msg = f"Erreur changement statut bot: {e}"
            self.db.logger.log_error(error_msg)
            return False, "Erreur lors du changement de statut"
    
    def delete_bot(self, bot_id):
        """
        Supprime un bot
        
        Args:
            bot_id (int): ID du bot
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            query = "DELETE FROM bots WHERE id = ?"
            self.db.cursor.execute(query, (bot_id,))
            self.db.connection.commit()
            
            self.db.logger.log_query(f"Bot supprimé: ID {bot_id}")
            
            return True, "Bot supprimé avec succès"
            
        except sqlite3.Error as e:
            error_msg = f"Erreur suppression bot: {e}"
            self.db.logger.log_error(error_msg)
            return False, "Erreur lors de la suppression"