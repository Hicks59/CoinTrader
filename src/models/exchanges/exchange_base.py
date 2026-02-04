from abc import ABC, abstractmethod

class ExchangeBase(ABC):
    """Classe de base abstraite pour tous les exchanges"""
    
    def __init__(self):
        self.name = ""
    
    @abstractmethod
    def get_crypto_price(self, symbol, quote_currency='USDC'):
        """
        Récupère le prix actuel d'une crypto
        
        Args:
            symbol (str): Symbole de la crypto (ex: 'BTC')
            quote_currency (str): Devise de cotation (ex: 'USDC')
            
        Returns:
            float: Prix actuel ou 0.0 si erreur
        """
        pass
    
    @abstractmethod
    def get_available_balance(self, symbol, account_id=None):
        """
        Récupère le solde disponible d'une crypto
        
        Args:
            symbol (str): Symbole de la crypto (ex: 'USDC')
            account_id: Identifiant du compte utilisateur
            
        Returns:
            float: Solde disponible ou 0.0 si erreur
        """
        pass
    
    @abstractmethod
    def get_product_ticker(self, product_id):
        """
        Récupère les informations de ticker d'un produit
        
        Args:
            product_id (str): ID du produit (ex: 'BTC-USDC')
            
        Returns:
            dict: Informations du ticker ou None si erreur
        """
        pass