from src.models.bot_model import BotModel

class BotController:
    """Contrôleur pour la gestion des bots de trading"""
    
    def __init__(self):
        self.bot_model = BotModel()
    
    def create_bot(self, user_id, exchange, product_id, crypto_source, 
                   crypto_target, prix_achat, pourcentage_gain, 
                   montant_trade, type_ordre):
        """
        Crée un nouveau bot de trading avec validation
        
        Args:
            user_id (int): ID de l'utilisateur
            exchange (str): Nom de l'exchange
            product_id (str): Paire de trading
            crypto_source (str): Crypto source
            crypto_target (str): Crypto target
            prix_achat (str): Prix d'achat cible (peut être vide)
            pourcentage_gain (str): Pourcentage de gain
            montant_trade (str): Montant du trade
            type_ordre (str): Type d'ordre
            
        Returns:
            dict: {
                'success': bool,
                'message': str,
                'bot_id': int or None
            }
        """
        # Validation des champs obligatoires
        if not all([product_id, crypto_source, crypto_target, pourcentage_gain, montant_trade]):
            return {
                'success': False,
                'message': 'Veuillez remplir tous les champs obligatoires',
                'bot_id': None
            }
        
        # Validation et conversion des valeurs numériques
        try:
            pourcentage_gain_float = float(pourcentage_gain)
            montant_trade_float = float(montant_trade)
            
            if prix_achat:
                prix_achat_float = float(prix_achat)
            else:
                prix_achat_float = None
                
        except ValueError:
            return {
                'success': False,
                'message': 'Valeurs numériques invalides',
                'bot_id': None
            }
        
        # Validation des valeurs
        if pourcentage_gain_float <= 0:
            return {
                'success': False,
                'message': 'Le pourcentage de gain doit être positif',
                'bot_id': None
            }
        
        if montant_trade_float <= 0:
            return {
                'success': False,
                'message': 'Le montant du trade doit être positif',
                'bot_id': None
            }
        
        # Normaliser les cryptos en majuscules
        crypto_source = crypto_source.strip().upper()
        crypto_target = crypto_target.strip().upper()
        
        # Créer le bot via le modèle
        success, message, bot_id = self.bot_model.create_bot(
            account_id=user_id,
            exchange_name=exchange,
            crypto_source=crypto_source,
            crypto_target=crypto_target,
            product_id=product_id,
            pourcentage_gain=pourcentage_gain_float,
            montant_trade=montant_trade_float,
            type_ordre=type_ordre,
            prix_achat_cible=prix_achat_float
        )
        
        return {
            'success': success,
            'message': message,
            'bot_id': bot_id
        }
    
    def get_user_bots(self, user_id):
        """
        Récupère tous les bots d'un utilisateur
        
        Args:
            user_id (int): ID de l'utilisateur
            
        Returns:
            list: Liste des bots
        """
        return self.bot_model.get_user_bots(user_id)
    
    def toggle_bot(self, bot_id, is_active):
        """
        Active ou désactive un bot
        
        Args:
            bot_id (int): ID du bot
            is_active (bool): Nouveau statut
            
        Returns:
            dict: {
                'success': bool,
                'message': str
            }
        """
        success, message = self.bot_model.toggle_bot_status(bot_id, is_active)
        
        return {
            'success': success,
            'message': message
        }
    
    def delete_bot(self, bot_id):
        """
        Supprime un bot
        
        Args:
            bot_id (int): ID du bot
            
        Returns:
            dict: {
                'success': bool,
                'message': str
            }
        """
        success, message = self.bot_model.delete_bot(bot_id)
        
        return {
            'success': success,
            'message': message
        }
    
    def format_bot_for_display(self, bot):
        """
        Formate les données d'un bot pour l'affichage
        
        Args:
            bot (dict): Données brutes du bot
            
        Returns:
            dict: Données formatées
        """
        return {
            'id': bot['id'],
            'pair': bot['product_id'],
            'exchange': bot['exchange_name'],
            'source': bot['crypto_source'],
            'target': bot['crypto_target'],
            'gain': f"{bot['pourcentage_gain']}%",
            'amount': f"{bot['montant_trade']} USDC",
            'target_price': f"{bot['prix_achat_cible']}" if bot['prix_achat_cible'] else "Prix marché",
            'order_type': bot['type_ordre'],
            'status': 'Actif' if bot['is_active'] else 'Inactif',
            'is_active': bot['is_active'],
            'created_at': bot['created_at']
        }