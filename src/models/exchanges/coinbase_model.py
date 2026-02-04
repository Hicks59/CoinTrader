import requests
from src.models.exchanges.exchange_base import ExchangeBase

# Constantes - URLs API
COINBASE_BASE_URL = "https://api.coinbase.com/v2"
COINBASE_PRO_BASE_URL = "https://api.exchange.coinbase.com"

# Constantes - Timeouts
REQUEST_TIMEOUT = 5

# Constantes - Messages de log
LOG_PRICE_SUCCESS = "✓ Prix {product_id}: ${price:,.8f}"
LOG_PRICE_INVALID = "✗ Prix invalide reçu pour {product_id}: {price}"
LOG_API_ERROR = "✗ Erreur API Coinbase ({status_code}) pour {product_id}"
LOG_API_RESPONSE = "   Réponse: {response}"
LOG_TIMEOUT = "✗ Timeout lors de la récupération du prix de {symbol}"
LOG_CONNECTION_ERROR = "✗ Erreur de connexion à l'API Coinbase pour {symbol}"
LOG_NETWORK_ERROR = "✗ Erreur réseau Coinbase pour {symbol}: {error}"
LOG_CONVERSION_ERROR = "✗ Erreur de conversion du prix pour {symbol}: {error}"
LOG_UNEXPECTED_ERROR = "✗ Erreur inattendue lors de la récupération du prix {symbol}: {error}"
LOG_BALANCE_NOT_IMPLEMENTED = "⚠ get_available_balance non implémenté pour {symbol}"
LOG_BALANCE_AUTH_REQUIRED = "   Nécessite l'authentification API Coinbase"
LOG_TICKER_ERROR = "✗ Erreur API ticker ({status_code}) pour {product_id}"
LOG_TICKER_EXCEPTION = "✗ Erreur récupération ticker {product_id}: {error}"
LOG_STATS_ERROR = "✗ Erreur API stats ({status_code}) pour {product_id}"
LOG_STATS_EXCEPTION = "✗ Erreur récupération stats {product_id}: {error}"

class CoinbaseModel(ExchangeBase):
    """Modèle pour interagir avec l'API Coinbase"""
    
    def __init__(self):
        super().__init__()
        self.name = "Coinbase"
        self.base_url = COINBASE_BASE_URL
        self.pro_base_url = COINBASE_PRO_BASE_URL
    
    def get_crypto_price(self, symbol, quote_currency='USDC'):
        """
        Récupère le prix actuel d'une crypto depuis Coinbase
        
        Args:
            symbol (str): Symbole de la crypto (ex: 'BTC')
            quote_currency (str): Devise de cotation (ex: 'USDC')
            
        Returns:
            float: Prix actuel ou None si erreur
        """
        try:
            # Cas spécial : si on demande le prix d'une stablecoin vs elle-même
            if symbol == quote_currency:
                return 1.0
            
            # Construire le product_id
            product_id = f"{symbol}-{quote_currency}"
            
            # Appel à l'API publique Coinbase Pro
            url = f"{self.pro_base_url}/products/{product_id}/ticker"
            
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                price = float(data.get('price', 0.0))
                
                if price > 0:
                    print(LOG_PRICE_SUCCESS.format(product_id=product_id, price=price))
                    return price
                else:
                    print(LOG_PRICE_INVALID.format(product_id=product_id, price=price))
                    return None
            else:
                print(LOG_API_ERROR.format(status_code=response.status_code, product_id=product_id))
                print(LOG_API_RESPONSE.format(response=response.text[:200]))
                return None
                
        except requests.exceptions.Timeout:
            print(LOG_TIMEOUT.format(symbol=symbol))
            return None
        except requests.exceptions.ConnectionError:
            print(LOG_CONNECTION_ERROR.format(symbol=symbol))
            return None
        except requests.exceptions.RequestException as e:
            print(LOG_NETWORK_ERROR.format(symbol=symbol, error=e))
            return None
        except ValueError as e:
            print(LOG_CONVERSION_ERROR.format(symbol=symbol, error=e))
            return None
        except Exception as e:
            print(LOG_UNEXPECTED_ERROR.format(symbol=symbol, error=e))
            return None
    
    def get_available_balance(self, symbol, account_id=None):
        """
        Récupère le solde disponible d'une crypto
        
        NOTE: Cette méthode nécessite une authentification API.
        Pour l'instant, retourne None (non implémenté).
        
        Args:
            symbol (str): Symbole de la crypto (ex: 'USDC')
            account_id: Identifiant du compte utilisateur
            
        Returns:
            float: Solde disponible ou None si erreur
        """
        # TODO: Implémenter l'authentification et l'appel à l'API
        # Nécessite les clés API de l'utilisateur stockées en BDD
        
        print(LOG_BALANCE_NOT_IMPLEMENTED.format(symbol=symbol))
        print(LOG_BALANCE_AUTH_REQUIRED)
        return None
    
    def get_product_ticker(self, product_id):
        """
        Récupère les informations de ticker d'un produit
        
        Args:
            product_id (str): ID du produit (ex: 'BTC-USDC')
            
        Returns:
            dict: Informations du ticker ou None si erreur
        """
        try:
            url = f"{self.pro_base_url}/products/{product_id}/ticker"
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'price': float(data.get('price', 0.0)),
                    'bid': float(data.get('bid', 0.0)),
                    'ask': float(data.get('ask', 0.0)),
                    'volume': float(data.get('volume', 0.0)),
                    'time': data.get('time', '')
                }
            else:
                print(LOG_TICKER_ERROR.format(status_code=response.status_code, product_id=product_id))
                return None
                
        except Exception as e:
            print(LOG_TICKER_EXCEPTION.format(product_id=product_id, error=e))
            return None
    
    def get_product_stats(self, product_id):
        """
        Récupère les statistiques 24h d'un produit
        
        Args:
            product_id (str): ID du produit (ex: 'BTC-USDC')
            
        Returns:
            dict: Statistiques 24h ou None si erreur
        """
        try:
            url = f"{self.pro_base_url}/products/{product_id}/stats"
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'open': float(data.get('open', 0.0)),
                    'high': float(data.get('high', 0.0)),
                    'low': float(data.get('low', 0.0)),
                    'volume': float(data.get('volume', 0.0)),
                    'last': float(data.get('last', 0.0)),
                    'volume_30day': float(data.get('volume_30day', 0.0))
                }
            else:
                print(LOG_STATS_ERROR.format(status_code=response.status_code, product_id=product_id))
                return None
                
        except Exception as e:
            print(LOG_STATS_EXCEPTION.format(product_id=product_id, error=e))
            return None