from src.models.exchange_model import ExchangeModel
from src.models.apikey_model import ApiKeyModel

class ExchangeController:
    """Contrôleur pour gérer les exchanges (plateformes) et les API keys"""
    
    def __init__(self):
        self.exchange_model = ExchangeModel()
        self.apikey_model = ApiKeyModel()
    
    # ============================================
    # GESTION DES EXCHANGES (PLATEFORMES)
    # ============================================
    
    def list_exchanges(self):
        """
        Liste toutes les plateformes
        
        Returns:
            list: Liste des exchanges
        """
        return self.exchange_model.get_all_exchanges()
    
    def get_exchange(self, exchange_id):
        """
        Récupère une plateforme par son ID
        
        Args:
            exchange_id (int): ID de l'exchange
            
        Returns:
            dict or None: Informations de l'exchange
        """
        return self.exchange_model.get_exchange_by_id(exchange_id)
    
    def get_exchange_by_name(self, name):
        """
        Récupère une plateforme par son nom
        
        Args:
            name (str): Nom de l'exchange
            
        Returns:
            dict or None: Informations de l'exchange
        """
        return self.exchange_model.get_exchange_by_name(name)
    
    def add_exchange(self, name, display_name, logo='💱', endpoint_url=None):
        """
        Ajoute une nouvelle plateforme
        
        Args:
            name (str): Nom technique (identifiant)
            display_name (str): Nom affiché
            logo (str): Logo (emoji ou URL)
            endpoint_url (str): URL de l'API
            
        Returns:
            tuple: (success: bool, message: str)
        """
        success, message, exchange_id = self.exchange_model.create_exchange(
            name, display_name, logo, endpoint_url
        )
        return success, message
    
    def update_exchange(self, exchange_id, display_name=None, logo=None, endpoint_url=None):
        """
        Met à jour une plateforme
        
        Args:
            exchange_id (int): ID de l'exchange
            display_name (str): Nouveau nom affiché
            logo (str): Nouveau logo
            endpoint_url (str): Nouvelle URL
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.exchange_model.update_exchange(
            exchange_id, display_name, logo, endpoint_url
        )
    
    def delete_exchange(self, exchange_id):
        """
        Supprime une plateforme
        
        Args:
            exchange_id (int): ID de l'exchange
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.exchange_model.delete_exchange(exchange_id)
    
    def toggle_exchange(self, exchange_id, is_active):
        """
        Active/désactive une plateforme
        
        Args:
            exchange_id (int): ID de l'exchange
            is_active (bool): Nouveau statut
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.exchange_model.toggle_exchange_status(exchange_id, is_active)
    
    # ============================================
    # GESTION DES API KEYS
    # ============================================
    
    def get_api_keys_for_user(self, user_id):
        """
        Récupère toutes les clés API d'un utilisateur
        
        Args:
            user_id (int): ID de l'utilisateur
            
        Returns:
            list: Liste des API keys
        """
        return self.apikey_model.get_api_keys_for_user(user_id)
    
    def add_api_key(self, account_id, exchange_id, api_key, api_secret, label=None):
        """
        Ajoute une clé API
        
        Args:
            account_id (int): ID du compte
            exchange_id (int): ID de l'exchange
            api_key (str): Clé API
            api_secret (str): Secret API
            label (str): Label optionnel
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.apikey_model.add_api_key(
            account_id, exchange_id, api_key, api_secret, label
        )
    
    def update_api_key(self, api_key_id, api_key, api_secret, label=None):
        """
        Met à jour une clé API
        
        Args:
            api_key_id (int): ID de la clé API
            api_key (str): Nouvelle clé
            api_secret (str): Nouveau secret
            label (str): Nouveau label
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.apikey_model.update_api_key(
            api_key_id, api_key, api_secret, label
        )
    
    def delete_api_key(self, api_key_id):
        """
        Supprime une clé API
        
        Args:
            api_key_id (int): ID de la clé API
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return self.apikey_model.delete_api_key(api_key_id)