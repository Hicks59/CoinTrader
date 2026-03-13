from src.models.database_model import DatabaseModel
from datetime import datetime

class ExchangeModel:
    """Modèle pour gérer les plateformes d'échange (exchanges) par utilisateur"""
    
    def __init__(self, db_model=None):
        self.db = db_model if db_model else DatabaseModel()
    
    def get_all_exchanges(self, account_id):
        """
        Récupère toutes les plateformes d'un utilisateur
        
        Args:
            account_id (int): ID de l'utilisateur
            
        Returns:
            list: Liste des exchanges de l'utilisateur
        """
        try:
            query = """
                SELECT exchange_id, fk_account_id, name, display_name, logo, endpoint_url, is_active, created_at, updated_at
                FROM exchanges 
                WHERE fk_account_id = ?
                ORDER BY display_name
            """
            self.db.cursor.execute(query, (account_id,))
            rows = self.db.cursor.fetchall()
            
            exchanges = []
            for row in rows:
                exchanges.append({
                    'exchange_id': row[0],
                    'account_id': row[1],
                    'name': row[2],
                    'display_name': row[3],
                    'logo': row[4] or '💱',
                    'endpoint_url': row[5],
                    'is_active': row[6],
                    'created_at': row[7],
                    'updated_at': row[8]
                })
            
            return exchanges
            
        except Exception as e:
            self.db.logger.log_error(f"Erreur récupération exchanges pour user {account_id}: {e}")
            return []
    
    def get_exchange_by_id(self, exchange_id, account_id):
        """
        Récupère une plateforme par son ID (avec vérification propriétaire)
        
        Args:
            exchange_id (int): ID de l'exchange
            account_id (int): ID de l'utilisateur (pour vérifier qu'il est propriétaire)
            
        Returns:
            dict or None: Informations de l'exchange ou None
        """
        try:
            query = """
                SELECT exchange_id, fk_account_id, name, display_name, logo, endpoint_url, is_active, created_at, updated_at
                FROM exchanges 
                WHERE exchange_id = ? AND fk_account_id = ?
            """
            self.db.cursor.execute(query, (exchange_id, account_id))
            row = self.db.cursor.fetchone()
            
            if row:
                return {
                    'exchange_id': row[0],
                    'account_id': row[1],
                    'name': row[2],
                    'display_name': row[3],
                    'logo': row[4] or '💱',
                    'endpoint_url': row[5],
                    'is_active': row[6],
                    'created_at': row[7],
                    'updated_at': row[8]
                }
            
            return None
            
        except Exception as e:
            self.db.logger.log_error(f"Erreur récupération exchange {exchange_id}: {e}")
            return None
    
    def get_exchange_by_name(self, name, account_id):
        """
        Récupère une plateforme par son nom technique pour un utilisateur
        
        Args:
            name (str): Nom technique de l'exchange
            account_id (int): ID de l'utilisateur
            
        Returns:
            dict or None: Informations de l'exchange ou None
        """
        try:
            query = """
                SELECT exchange_id, fk_account_id, name, display_name, logo, endpoint_url, is_active, created_at, updated_at
                FROM exchanges 
                WHERE name = ? AND fk_account_id = ?
            """
            self.db.cursor.execute(query, (name.lower(), account_id))
            row = self.db.cursor.fetchone()
            
            if row:
                return {
                    'exchange_id': row[0],
                    'account_id': row[1],
                    'name': row[2],
                    'display_name': row[3],
                    'logo': row[4] or '💱',
                    'endpoint_url': row[5],
                    'is_active': row[6],
                    'created_at': row[7],
                    'updated_at': row[8]
                }
            
            return None
            
        except Exception as e:
            self.db.logger.log_error(f"Erreur récupération exchange par nom {name}: {e}")
            return None
    
    def create_exchange(self, account_id, name, display_name, logo='💱', endpoint_url=None):
        """
        Crée une nouvelle plateforme pour un utilisateur
        
        Args:
            account_id (int): ID de l'utilisateur propriétaire
            name (str): Nom technique (identifiant unique pour cet utilisateur)
            display_name (str): Nom affiché
            logo (str): Logo (emoji ou URL)
            endpoint_url (str): URL de l'API
            
        Returns:
            tuple: (success: bool, message: str, exchange_id: int or None)
        """
        try:
            # Vérifier si l'exchange existe déjà pour cet utilisateur
            existing = self.get_exchange_by_name(name, account_id)
            if existing:
                return False, f"Vous avez déjà une plateforme nommée '{name}'", None
            
            query = """
                INSERT INTO exchanges (fk_account_id, name, display_name, logo, endpoint_url, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            now = datetime.now()
            self.db.cursor.execute(
                query,
                (account_id, name.lower(), display_name, logo, endpoint_url, now, now)
            )
            self.db.connection.commit()
            
            exchange_id = self.db.cursor.lastrowid
            
            self.db.logger.log_query(f"Exchange créée: {display_name} (ID: {exchange_id}, User: {account_id})")
            self.db.log_activity(account_id, 'PLATFORM_ADDED', f"Plateforme ajoutée : {display_name}")

            return True, "Plateforme créée avec succès", exchange_id
            
        except Exception as e:
            error_msg = f"Erreur création exchange: {e}"
            self.db.logger.log_error(error_msg)
            return False, "Erreur lors de la création de la plateforme", None
    
    def update_exchange(self, exchange_id, account_id, display_name=None, logo=None, endpoint_url=None, is_active=None):
        """
        Met à jour une plateforme (avec vérification propriétaire)
        
        Args:
            exchange_id (int): ID de l'exchange
            account_id (int): ID de l'utilisateur (pour vérifier qu'il est propriétaire)
            display_name (str): Nouveau nom affiché (optionnel)
            logo (str): Nouveau logo (optionnel)
            endpoint_url (str): Nouvelle URL (optionnel)
            is_active (bool): Nouveau statut (optionnel)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Vérifier que l'exchange existe ET appartient à l'utilisateur
            existing = self.get_exchange_by_id(exchange_id, account_id)
            if not existing:
                return False, "Plateforme introuvable ou vous n'en êtes pas le propriétaire"
            
            # Construire la requête dynamiquement
            updates = []
            params = []
            
            if display_name is not None:
                updates.append("display_name = ?")
                params.append(display_name)
            
            if logo is not None:
                updates.append("logo = ?")
                params.append(logo)
            
            if endpoint_url is not None:
                updates.append("endpoint_url = ?")
                params.append(endpoint_url)
            
            if is_active is not None:
                updates.append("is_active = ?")
                params.append(1 if is_active else 0)
            
            if not updates:
                return True, "Aucune modification à effectuer"
            
            # Ajouter updated_at
            updates.append("updated_at = ?")
            params.append(datetime.now())
            
            # Ajouter les conditions WHERE
            params.append(exchange_id)
            params.append(account_id)
            
            query = f"UPDATE exchanges SET {', '.join(updates)} WHERE exchange_id = ? AND fk_account_id = ?"
            self.db.cursor.execute(query, params)
            self.db.connection.commit()
            
            self.db.logger.log_query(f"Exchange modifiée: ID {exchange_id} by User {account_id}")
            
            return True, "Plateforme modifiée avec succès"
            
        except Exception as e:
            error_msg = f"Erreur modification exchange: {e}"
            self.db.logger.log_error(error_msg)
            return False, "Erreur lors de la modification de la plateforme"
    
    def delete_exchange(self, exchange_id, account_id):
        """
        Supprime une plateforme (avec vérification propriétaire)
        
        ATTENTION: Cela supprimera aussi toutes les clés API et bots associés (CASCADE)
        
        Args:
            exchange_id (int): ID de l'exchange
            account_id (int): ID de l'utilisateur (pour vérifier qu'il est propriétaire)
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Vérifier que l'exchange existe ET appartient à l'utilisateur
            existing = self.get_exchange_by_id(exchange_id, account_id)
            if not existing:
                return False, "Plateforme introuvable ou vous n'en êtes pas le propriétaire"
            
            # Vérifier s'il y a des API keys ou bots liés
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM api_keys WHERE fk_exchange_id = ?",
                (exchange_id,)
            )
            api_keys_count = self.db.cursor.fetchone()[0]
            
            self.db.cursor.execute(
                "SELECT COUNT(*) FROM bots WHERE fk_exchange_id = ?",
                (exchange_id,)
            )
            bots_count = self.db.cursor.fetchone()[0]
            
            if api_keys_count > 0 or bots_count > 0:
                return False, f"Impossible de supprimer: {api_keys_count} clé(s) API et {bots_count} bot(s) sont liés à cette plateforme"
            
            # Supprimer
            query = "DELETE FROM exchanges WHERE exchange_id = ? AND fk_account_id = ?"
            self.db.cursor.execute(query, (exchange_id, account_id))
            self.db.connection.commit()
            
            self.db.logger.log_query(f"Exchange supprimée: ID {exchange_id} by User {account_id}")
            
            return True, "Plateforme supprimée avec succès"
            
        except Exception as e:
            error_msg = f"Erreur suppression exchange: {e}"
            self.db.logger.log_error(error_msg)
            return False, "Erreur lors de la suppression de la plateforme"
    
    def toggle_exchange_status(self, exchange_id, account_id, is_active):
        """
        Active ou désactive une plateforme
        
        Args:
            exchange_id (int): ID de l'exchange
            account_id (int): ID de l'utilisateur
            is_active (bool): Nouveau statut
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.update_exchange(exchange_id, account_id, is_active=is_active) 