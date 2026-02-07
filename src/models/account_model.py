import sqlite3
import bcrypt

# Constantes
DB_PATH = 'datas/cointrader.db'

class AccountModel:
    """Modèle pour gérer les comptes utilisateurs en base de données"""
    
    def __init__(self):
        self.db_path = DB_PATH
    
    def _hash_password(self, password):
        """Hash le mot de passe avec bcrypt"""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return password_hash.decode('utf-8')
    
    def _verify_password(self, password, stored_hash):
        """Vérifie le mot de passe avec bcrypt"""
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
    
    def username_exists(self, username):
        """
        Vérifie si un nom d'utilisateur existe déjà
        
        Args:
            username (str): Nom d'utilisateur à vérifier
            
        Returns:
            bool: True si existe, False sinon
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT account_id FROM accounts WHERE username = ?",
                (username,)
            )
            
            result = cursor.fetchone()
            conn.close()
            
            return result is not None
            
        except Exception as e:
            print(f"✗ Erreur vérification username: {e}")
            return False
    
    def create_account(self, username, password, email, nom, prenom):
        """
        Crée un nouveau compte utilisateur
        
        Args:
            username (str): Nom d'utilisateur
            password (str): Mot de passe (sera hashé)
            email (str): Email
            nom (str): Nom
            prenom (str): Prénom
            
        Returns:
            dict: {'success': bool, 'user_id': int or None, 'error': str or None}
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Hasher le mot de passe avec bcrypt
            hashed_password = self._hash_password(password)
            
            # Insérer le nouvel utilisateur
            cursor.execute(
                "INSERT INTO accounts (username, password_hash, email, nom, prenom) VALUES (?, ?, ?, ?, ?)",
                (username, hashed_password, email, nom, prenom)
            )
            
            user_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'user_id': user_id,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'user_id': None,
                'error': str(e)
            }
    
    def authenticate(self, username, password):
        """
        Authentifie un utilisateur
        
        Args:
            username (str): Nom d'utilisateur
            password (str): Mot de passe
            
        Returns:
            dict: {'success': bool, 'user_data': dict or None, 'error': str or None}
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Chercher l'utilisateur
            cursor.execute(
                "SELECT account_id, username, password_hash, email, nom, prenom FROM accounts WHERE username = ?",
                (username,)
            )
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                user_id, username_db, stored_hash, email, nom, prenom = user
                
                # Vérifier le mot de passe avec bcrypt
                if self._verify_password(password, stored_hash):
                    return {
                        'success': True,
                        'user_data': {
                            'id': user_id,
                            'username': username_db,
                            'email': email,
                            'nom': nom,
                            'prenom': prenom
                        },
                        'error': None
                    }
                else:
                    return {
                        'success': False,
                        'user_data': None,
                        'error': 'invalid_credentials'
                    }
            else:
                return {
                    'success': False,
                    'user_data': None,
                    'error': 'invalid_credentials'
                }
                
        except Exception as e:
            return {
                'success': False,
                'user_data': None,
                'error': str(e)
            }
    
    def get_user_by_id(self, account_id):
        """
        Récupère les informations d'un utilisateur par son ID
        
        Args:
            account_id (int): ID du compte
            
        Returns:
            dict or None: Informations de l'utilisateur ou None
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT account_id, username, email, nom, prenom FROM accounts WHERE account_id = ?",
                (account_id,)
            )
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'nom': user[3],
                    'prenom': user[4]
                }
            
            return None
            
        except Exception as e:
            print(f"✗ Erreur récupération utilisateur: {e}")
            return None
    
    def update_profile(self, account_id, username=None, email=None, nom=None, prenom=None):
        """
        Met à jour le profil d'un utilisateur
        
        Args:
            account_id (int): ID du compte
            username (str): Nouveau nom d'utilisateur (optionnel)
            email (str): Nouvel email (optionnel)
            nom (str): Nouveau nom (optionnel)
            prenom (str): Nouveau prénom (optionnel)
            
        Returns:
            dict: {'success': bool, 'error': str or None}
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Construire la requête dynamiquement
            updates = []
            params = []
            
            if username is not None:
                updates.append("username = ?")
                params.append(username)
            
            if email is not None:
                updates.append("email = ?")
                params.append(email)
            
            if nom is not None:
                updates.append("nom = ?")
                params.append(nom)
            
            if prenom is not None:
                updates.append("prenom = ?")
                params.append(prenom)
            
            if not updates:
                return {'success': True, 'error': None}
            
            # Ajouter updated_at
            updates.append("updated_at = CURRENT_TIMESTAMP")
            
            # Ajouter account_id
            params.append(account_id)
            
            # Exécuter la requête
            query = f"UPDATE accounts SET {', '.join(updates)} WHERE account_id = ?"
            cursor.execute(query, params)
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'error': None}
            
        except Exception as e:
            print(f"✗ Erreur mise à jour profil: {e}")
            return {'success': False, 'error': str(e)}
    
    def change_password(self, account_id, current_password, new_password):
        """
        Change le mot de passe d'un utilisateur
        
        Args:
            account_id (int): ID du compte
            current_password (str): Mot de passe actuel
            new_password (str): Nouveau mot de passe
            
        Returns:
            dict: {'success': bool, 'error': str or None}
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Récupérer le hash actuel
            cursor.execute(
                "SELECT password_hash FROM accounts WHERE account_id = ?",
                (account_id,)
            )
            
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return {'success': False, 'error': 'user_not_found'}
            
            stored_hash = result[0]
            
            # Vérifier le mot de passe actuel
            if not self._verify_password(current_password, stored_hash):
                conn.close()
                return {'success': False, 'error': 'invalid_current_password'}
            
            # Hasher le nouveau mot de passe
            new_hash = self._hash_password(new_password)
            
            # Mettre à jour
            cursor.execute(
                "UPDATE accounts SET password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE account_id = ?",
                (new_hash, account_id)
            )
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'error': None}
            
        except Exception as e:
            print(f"✗ Erreur changement mot de passe: {e}")
            return {'success': False, 'error': str(e)}