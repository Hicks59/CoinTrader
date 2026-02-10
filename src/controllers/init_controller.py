import os
import shutil
from src.utils.db_connection import get_db_connection

class InitController:
    """Controller pour l'initialisation de l'application"""
    
    def __init__(self):
        self.db_path = 'datas/cointrader.db'
        self.sql_init_file = 'init_project/init_database.sql'
        self.log_dir = 'logs'
        self.data_dir = 'datas'
        self.max_init_attempts = 3
    
    def cleanup_cache(self):
        """Nettoie le cache Python"""
        try:
            cache_count = 0
            for root_dir, dirs, files in os.walk('.'):
                if '__pycache__' in dirs:
                    pycache_path = os.path.join(root_dir, '__pycache__')
                    shutil.rmtree(pycache_path)
                    cache_count += 1
            
            return {
                'success': True,
                'message': f"{cache_count} dossier(s) cache supprimé(s)" if cache_count > 0 else "Aucun cache à nettoyer",
                'count': cache_count
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur nettoyage cache: {str(e)}"
            }
    
    def check_database_connection(self):
        """Vérifie la connexion à la base de données"""
        try:
            # Créer le dossier data s'il n'existe pas
            os.makedirs(self.data_dir, exist_ok=True)
            
            # Tester la connexion
            conn = get_db_connection(self.db_path)
            conn.close()
            
            return {
                'success': True,
                'message': f"Connexion réussie à {self.db_path}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur de connexion à la base de données: {str(e)}"
            }
    
    def check_tables_exist(self):
        """Vérifie l'existence des tables dans la base de données"""
        try:
            conn = get_db_connection(self.db_path)
            cursor = conn.cursor()
            
            # Tables requises
            required_tables = ['accounts', 'exchanges', 'api_keys', 'bots', 'orders']
            missing_tables = []
            
            # Vérifier chaque table
            for table in required_tables:
                cursor.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                    (table,)
                )
                if not cursor.fetchone():
                    missing_tables.append(table)
            
            conn.close()
            
            if missing_tables:
                return {
                    'success': True,
                    'message': f"Tables manquantes: {', '.join(missing_tables)}",
                    'missing_tables': missing_tables,
                    'needs_init': True
                }
            
            return {
                'success': True,
                'message': "Toutes les tables existent",
                'needs_init': False
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur vérification tables: {str(e)}",
                'needs_init': False
            }
    
    def initialize_database(self):
        """Initialise la base de données avec le script SQL"""
        try:
            if not os.path.exists(self.sql_init_file):
                return {
                    'success': False,
                    'message': f"Fichier SQL introuvable: {self.sql_init_file}"
                }
            
            # Lire le script SQL
            with open(self.sql_init_file, 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # Exécuter le script
            conn = get_db_connection(self.db_path)
            cursor = conn.cursor()
            
            cursor.executescript(sql_script)
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': "Base de données initialisée avec succès"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur initialisation BDD: {str(e)}"
            }
    
    def check_log_permissions(self):
        """Vérifie les droits d'écriture pour les logs"""
        try:
            # Créer le dossier logs s'il n'existe pas
            os.makedirs(self.log_dir, exist_ok=True)
            
            # Tester l'écriture
            test_file = os.path.join(self.log_dir, '.test_write')
            
            with open(test_file, 'w') as f:
                f.write('test')
            
            # Supprimer le fichier de test
            os.remove(test_file)
            
            return {
                'success': True,
                'message': f"Droits d'écriture OK dans {self.log_dir}"
            }
        except Exception as e:
            return {
                'success': False,
                'message': f"Impossible d'écrire dans le dossier logs: {str(e)}"
            }
    
    def _handle_database_initialization(self, results):
        """Gère l'initialisation de la base de données avec plusieurs tentatives"""
        attempt = 0
        
        while attempt < self.max_init_attempts:
            attempt += 1
            print(f"  → Tentative {attempt}/{self.max_init_attempts} d'initialisation...")
            
            # Initialiser la base de données
            init_result = self.initialize_database()
            init_result['step'] = f"Initialisation de la base de données (tentative {attempt}/{self.max_init_attempts})"
            results.append(init_result)
            
            if not init_result['success']:
                print(f"  ✗ Échec de la tentative {attempt}")
                if attempt >= self.max_init_attempts:
                    return {
                        'success': False,
                        'error': f"Échec de l'initialisation après {self.max_init_attempts} tentatives: {init_result['message']}"
                    }
                continue
            
            print(f"  → {init_result['message']}")
            
            # RE-VÉRIFIER que les tables sont bien créées
            reverify_result = self.check_tables_exist()
            reverify_result['step'] = f"Vérification de la création des tables (tentative {attempt})"
            results.append(reverify_result)
            
            if reverify_result['success'] and not reverify_result.get('needs_init'):
                print(f"  → {reverify_result['message']}")
                return {'success': True}
            
            print(f"  ✗ Les tables n'ont pas été créées correctement (tentative {attempt})")
            if attempt >= self.max_init_attempts:
                return {
                    'success': False,
                    'error': f"Les tables n'ont pas été créées correctement après {self.max_init_attempts} tentatives"
                }
        
        return {'success': False, 'error': 'Erreur inconnue lors de l\'initialisation'}
    
    def _check_and_init_tables(self, results):
        """Vérifie les tables et les initialise si nécessaire"""
        tables_result = self.check_tables_exist()
        tables_result['step'] = "Vérification de la structure de la base de données"
        results.append(tables_result)
        
        if not tables_result['success']:
            return {'success': False, 'error': tables_result['message']}
        
        if tables_result.get('needs_init'):
            print(f"  → {tables_result['message']}")
            return self._handle_database_initialization(results)
        
        print(f"  → {tables_result['message']}")
        return {'success': True}
    
    def run_all_checks(self):
        """Exécute toutes les vérifications dans l'ordre"""
        results = []
        
        # 1. Nettoyage du cache
        cache_result = self.cleanup_cache()
        cache_result['step'] = "Nettoyage du cache"
        results.append(cache_result)
        print(f"  → {cache_result['message']}")
        
        # 2. Vérification connexion BDD
        db_connection_result = self.check_database_connection()
        db_connection_result['step'] = "Vérification de la connexion à la base de données"
        results.append(db_connection_result)
        
        if not db_connection_result['success']:
            return {
                'success': False,
                'results': results,
                'error': db_connection_result['message']
            }
        print(f"  → {db_connection_result['message']}")
        
        # 3. Vérification et initialisation des tables si nécessaire
        tables_check_result = self._check_and_init_tables(results)
        if not tables_check_result['success']:
            return {
                'success': False,
                'results': results,
                'error': tables_check_result['error']
            }
        
        # 4. Vérification des droits d'écriture logs
        log_result = self.check_log_permissions()
        log_result['step'] = "Vérification des droits d'écriture pour les logs"
        results.append(log_result)
        
        if not log_result['success']:
            return {
                'success': False,
                'results': results,
                'error': log_result['message']
            }
        print(f"  → {log_result['message']}")
        
        return {
            'success': True,
            'results': results,
            'message': "Toutes les vérifications ont réussi"
        }