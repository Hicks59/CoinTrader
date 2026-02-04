from src.models.account_model import AccountModel

# Constantes - Messages d'erreur
MSG_ERROR_MISSING_FIELDS = 'Veuillez remplir tous les champs'
MSG_ERROR_PASSWORD_MISMATCH = 'Les mots de passe ne correspondent pas'
MSG_ERROR_USERNAME_EXISTS = 'Ce nom d\'utilisateur existe déjà'
MSG_ERROR_REGISTRATION_FAILED = 'Erreur lors de la création du compte'
MSG_ERROR_INVALID_CREDENTIALS = 'Nom d\'utilisateur ou mot de passe incorrect'
MSG_ERROR_LOGIN_FAILED = 'Erreur lors de la connexion'
MSG_ERROR_UPDATE_FAILED = 'Erreur lors de la mise à jour du profil'
MSG_ERROR_CHANGE_PASSWORD_FAILED = 'Erreur lors du changement de mot de passe'
MSG_ERROR_CURRENT_PASSWORD_INCORRECT = 'Le mot de passe actuel est incorrect'

# Constantes - Messages de succès
MSG_SUCCESS_REGISTRATION = 'Compte créé avec succès !'
MSG_SUCCESS_LOGIN = 'Connexion réussie !'
MSG_SUCCESS_UPDATE = 'Profil mis à jour avec succès !'
MSG_SUCCESS_CHANGE_PASSWORD = 'Mot de passe changé avec succès !'

class AccountController:
    """Controller pour gérer les comptes utilisateurs (logique métier)"""
    
    def __init__(self):
        self.account_model = AccountModel()
    
    def register(self, username, password, confirm_password, email='', nom='', prenom=''):
        """
        Enregistre un nouveau compte utilisateur
        
        Args:
            username (str): Nom d'utilisateur
            password (str): Mot de passe
            confirm_password (str): Confirmation du mot de passe
            email (str): Email
            nom (str): Nom
            prenom (str): Prénom
            
        Returns:
            dict: {'success': bool, 'message': str}
        """
        # Validation : champs vides
        if not username or not password or not confirm_password:
            return {
                'success': False,
                'message': MSG_ERROR_MISSING_FIELDS
            }
        
        # Validation : mots de passe correspondent
        if password != confirm_password:
            return {
                'success': False,
                'message': MSG_ERROR_PASSWORD_MISMATCH
            }
        
        # Validation : username déjà pris
        if self.account_model.username_exists(username):
            return {
                'success': False,
                'message': MSG_ERROR_USERNAME_EXISTS
            }
        
        # Valeurs par défaut si non fournies
        if not email:
            email = f"{username}@kipacoin.local"
        if not nom:
            nom = username
        if not prenom:
            prenom = "User"
        
        # Créer le compte
        result = self.account_model.create_account(username, password, email, nom, prenom)
        
        if result['success']:
            return {
                'success': True,
                'message': MSG_SUCCESS_REGISTRATION
            }
        else:
            return {
                'success': False,
                'message': f"{MSG_ERROR_REGISTRATION_FAILED}: {result['error']}"
            }
    
    def login(self, username, password):
        """
        Connecte un utilisateur
        
        Args:
            username (str): Nom d'utilisateur
            password (str): Mot de passe
            
        Returns:
            dict: {'success': bool, 'message': str, 'user_data': dict}
        """
        # Validation : champs vides
        if not username or not password:
            return {
                'success': False,
                'message': MSG_ERROR_MISSING_FIELDS,
                'user_data': None
            }
        
        # Authentifier
        result = self.account_model.authenticate(username, password)
        
        if result['success']:
            return {
                'success': True,
                'message': MSG_SUCCESS_LOGIN,
                'user_data': result['user_data']
            }
        else:
            if result['error'] == 'invalid_credentials':
                return {
                    'success': False,
                    'message': MSG_ERROR_INVALID_CREDENTIALS,
                    'user_data': None
                }
            else:
                return {
                    'success': False,
                    'message': f"{MSG_ERROR_LOGIN_FAILED}: {result['error']}",
                    'user_data': None
                }
    
    def update_profile(self, account_id, current_username=None, current_email=None, current_nom=None, current_prenom=None, username=None, email=None, nom=None, prenom=None):
        """
        Met à jour le profil d'un utilisateur
        
        Args:
            account_id (int): ID du compte utilisateur
            current_username (str): Nom d'utilisateur actuel (non utilisé)
            current_email (str): Email actuel (non utilisé)
            current_nom (str): Nom actuel (non utilisé)
            current_prenom (str): Prénom actuel (non utilisé)
            username (str): Nouveau nom d'utilisateur (optionnel)
            email (str): Nouvel email (optionnel)
            nom (str): Nouveau nom (optionnel)
            prenom (str): Nouveau prénom (optionnel)
            
        Returns:
            dict: {'success': bool, 'message': str, 'updated_data': dict}
        """
        try:
            # Récupérer les données actuelles
            current_user = self.account_model.get_user_by_id(account_id)
            
            if not current_user:
                return {
                    'success': False,
                    'message': 'Utilisateur introuvable',
                    'updated_data': None
                }
            
            # Vérifier si au moins un champ a été modifié
            has_changes = False
            
            if username is not None and username != current_user['username']:
                has_changes = True
            
            if email is not None and email != current_user['email']:
                has_changes = True
            
            if nom is not None and nom != current_user['nom']:
                has_changes = True
            
            if prenom is not None and prenom != current_user['prenom']:
                has_changes = True
            
            # Si aucun changement détecté
            if not has_changes:
                return {
                    'success': True,
                    'message': 'Aucune modification détectée',
                    'updated_data': current_user
                }
            
            # Effectuer la mise à jour
            result = self.account_model.update_profile(account_id, username, email, nom, prenom)
            
            if result['success']:
                # Récupérer les données mises à jour
                user_data = self.account_model.get_user_by_id(account_id)
                
                return {
                    'success': True,
                    'message': MSG_SUCCESS_UPDATE,
                    'updated_data': user_data
                }
            else:
                return {
                    'success': False,
                    'message': f"{MSG_ERROR_UPDATE_FAILED}: {result['error']}",
                    'updated_data': None
                }
        except Exception as e:
            return {
                'success': False,
                'message': f"{MSG_ERROR_UPDATE_FAILED}: {str(e)}",
                'updated_data': None
            }
    
    def change_password(self, account_id, current_password, new_password, confirm_password):
        """
        Change le mot de passe d'un utilisateur
        
        Args:
            account_id (int): ID du compte utilisateur
            current_password (str): Mot de passe actuel
            new_password (str): Nouveau mot de passe
            confirm_password (str): Confirmation du nouveau mot de passe
            
        Returns:
            dict: {'success': bool, 'message': str}
        """
        # Validation : champs vides
        if not current_password or not new_password or not confirm_password:
            return {
                'success': False,
                'message': MSG_ERROR_MISSING_FIELDS
            }
        
        # Validation : nouveaux mots de passe correspondent
        if new_password != confirm_password:
            return {
                'success': False,
                'message': MSG_ERROR_PASSWORD_MISMATCH
            }
        
        # Changer le mot de passe
        result = self.account_model.change_password(account_id, current_password, new_password)
        
        if result['success']:
            return {
                'success': True,
                'message': MSG_SUCCESS_CHANGE_PASSWORD
            }
        else:
            if result['error'] == 'invalid_current_password':
                return {
                    'success': False,
                    'message': MSG_ERROR_CURRENT_PASSWORD_INCORRECT
                }
            else:
                return {
                    'success': False,
                    'message': f"{MSG_ERROR_CHANGE_PASSWORD_FAILED}: {result['error']}"
                }