import json
import os

class CryptoModel:
    """Modèle pour gérer les cryptomonnaies disponibles depuis les fichiers JSON"""
    
    def __init__(self):
        # Obtenir le chemin racine du projet (2 niveaux au-dessus de ce fichier)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.base_path = os.path.join(project_root, 'datas')
        
        self.cryptos = []
        self.crypto_details = {}  # {symbol: {name, product_id}}
        self.load_cryptos()
        
        # Cache pour les modèles d'exchange
        self._exchange_models = {}
    
    def load_cryptos(self):
        """Charge les cryptos depuis les fichiers JSON"""
        try:
            # Chercher le fichier JSON des cryptos
            json_file = os.path.join(self.base_path, 'coinbase_cryptos_list.json')
            
            if not os.path.exists(json_file):
                print(f"⚠ Fichier {json_file} introuvable")
                self.cryptos = []
                return
            
            # Lire le fichier JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Extraire les cryptos
            if 'cryptos' in data and isinstance(data['cryptos'], list):
                for crypto in data['cryptos']:
                    symbol = crypto.get('symbol', '').upper()
                    name = crypto.get('name', symbol)
                    product_id = crypto.get('product_id', '')
                    
                    if symbol:
                        self.cryptos.append(symbol)
                        self.crypto_details[symbol] = {
                            'name': name,
                            'product_id': product_id
                        }
            
            # Trier les symboles
            self.cryptos = sorted(self.cryptos)
            
            print(f"✓ {len(self.cryptos)} cryptomonnaies chargées depuis {json_file}")
        
        except Exception as e:
            print(f"✗ Erreur chargement cryptos: {e}")
            self.cryptos = []
            self.crypto_details = {}
    
    def _get_exchange_model(self, exchange_name):
        """Récupère ou crée une instance du modèle d'exchange"""
        exchange_name = exchange_name.lower()
        
        if exchange_name not in self._exchange_models:
            if exchange_name == 'coinbase':
                from src.models.exchanges.coinbase_model import CoinbaseModel
                self._exchange_models[exchange_name] = CoinbaseModel()
            else:
                print(f"⚠ Exchange '{exchange_name}' non supporté")
                return None
        
        return self._exchange_models.get(exchange_name)
    
    def get_crypto_price(self, symbol, exchange_name='coinbase', quote_currency='USDC'):
        """
        Récupère le prix actuel d'une crypto depuis un exchange
        
        Args:
            symbol (str): Symbole de la crypto (ex: 'BTC')
            exchange_name (str): Nom de l'exchange (ex: 'coinbase')
            quote_currency (str): Devise de cotation (ex: 'USDC')
            
        Returns:
            float: Prix actuel ou None si erreur
        """
        try:
            exchange_model = self._get_exchange_model(exchange_name)
            
            if exchange_model is None:
                return None
            
            price = exchange_model.get_crypto_price(symbol, quote_currency)
            return price
            
        except Exception as e:
            print(f"✗ Erreur récupération prix {symbol}: {e}")
            return None
    
    def get_available_balance(self, symbol, exchange_name='coinbase', account_id=None):
        """
        Récupère le solde disponible d'une crypto depuis un exchange
        
        Args:
            symbol (str): Symbole de la crypto (ex: 'USDC')
            exchange_name (str): Nom de l'exchange (ex: 'coinbase')
            account_id: Identifiant du compte utilisateur
            
        Returns:
            float: Solde disponible ou None si erreur
        """
        try:
            exchange_model = self._get_exchange_model(exchange_name)
            
            if exchange_model is None:
                return None
            
            balance = exchange_model.get_available_balance(symbol, account_id)
            return balance
            
        except Exception as e:
            print(f"✗ Erreur récupération balance {symbol}: {e}")
            return None
    
    def get_all_symbols(self):
        """Retourne la liste de tous les symboles disponibles"""
        return self.cryptos
    
    def get_symbol_name(self, symbol):
        """Retourne le nom complet d'une crypto à partir de son symbole"""
        symbol_upper = symbol.upper()
        if symbol_upper in self.crypto_details:
            return self.crypto_details[symbol_upper]['name']
        return symbol
    
    def get_product_id(self, symbol):
        """Retourne le product_id d'une crypto"""
        symbol_upper = symbol.upper()
        if symbol_upper in self.crypto_details:
            return self.crypto_details[symbol_upper].get('product_id', '')
        return ''
    
    def get_crypto_info(self, symbol):
        """Retourne toutes les informations d'une crypto"""
        symbol_upper = symbol.upper()
        return self.crypto_details.get(symbol_upper, {})
    
    def is_valid_symbol(self, symbol):
        """Vérifie si un symbole est valide"""
        return symbol.upper() in self.cryptos
    
    def reload_cryptos(self):
        """Recharge les cryptos depuis les fichiers JSON"""
        self.cryptos = []
        self.crypto_details = {}
        self.load_cryptos()