import os
import json
import zipfile
from datetime import datetime

class DbLogger:
    """Gestion des logs pour la base de données avec rotation et archivage"""
    
    def __init__(self, log_file="logs/database.log", config_file="configs/app_config.json"):
        self.log_file = log_file
        self.config_file = config_file
        self.archive_dir = "logs/archives"
        self.max_size_bytes = 25 * 1024 * 1024  # 25 Mo par défaut
        
        # Créer les dossiers si nécessaire
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
        
        # Charger la configuration
        self.debug_mode = self._load_config()
        
        # Vérifier la taille avant d'écrire
        self._check_and_rotate()
    
    def _load_config(self):
        """Charge la configuration et retourne le mode debug"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.max_size_bytes = config.get('log_max_size_mb', 25) * 1024 * 1024
                    return config.get('debug_mode', False)
            else:
                self._create_default_config()
                return False
        except (IOError, json.JSONDecodeError, KeyError):
            return False
    
    def _create_default_config(self):
        """Crée un fichier de configuration par défaut"""
        default_config = {
            "debug_mode": False,
            "log_max_size_mb": 25
        }
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)
    
    def _check_and_rotate(self):
        """Vérifie la taille du log et archive si nécessaire"""
        if not os.path.exists(self.log_file):
            return
        
        file_size = os.path.getsize(self.log_file)
        if file_size >= self.max_size_bytes:
            self._archive_log()
    
    def _archive_log(self):
        """Archive le fichier log actuel en ZIP avec nommage daté"""
        try:
            # Vérifier les permissions d'écriture sur le dossier archives
            if not os.access(self.archive_dir, os.W_OK):
                self._write_log('ERROR', f'Pas de permission d\'écriture sur {self.archive_dir}')
                return
            
            with open(self.log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if not lines:
                return
            
            first_date = self._extract_timestamp(lines[0])
            last_date = self._extract_timestamp(lines[-1])
            
            archive_name = f"database_{first_date}_to_{last_date}.zip"
            archive_path = os.path.join(self.archive_dir, archive_name)
            
            # Créer l'archive ZIP
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.log_file, os.path.basename(self.log_file))
            
            # Vérifier que le ZIP est valide avant de supprimer l'original
            if zipfile.is_zipfile(archive_path):
                os.remove(self.log_file)
            else:
                self._write_log('ERROR', f'Archive ZIP invalide: {archive_path}')
            
        except (IOError, OSError, zipfile.BadZipFile) as e:
            self._write_log('ERROR', f'Erreur archivage log: {e}')
            
            if not lines:
                return
            
            # Extraire les dates
            first_date = self._extract_timestamp(lines[0])
            last_date = self._extract_timestamp(lines[-1])
            
            # Nom de l'archive
            archive_name = f"database_{first_date}_to_{last_date}.zip"
            archive_path = os.path.join(self.archive_dir, archive_name)
            
            # Créer l'archive ZIP
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(self.log_file, os.path.basename(self.log_file))
            
            # Supprimer l'ancien fichier log
            os.remove(self.log_file)
            
            print(f"Log archivé : {archive_name}")
            
        except Exception as e:
            print(f"Erreur lors de l'archivage : {e}")
    
    def _extract_timestamp(self, line):
        """Extrait le timestamp d'une ligne de log"""
        try:
            timestamp_str = line.split(']')[0].replace('[', '').strip()
            dt = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
            return dt.strftime('%Y%m%d_%H%M%S')
        except (ValueError, IndexError):
            return datetime.now().strftime('%Y%m%d_%H%M%S')
    
    def _write_log(self, level, message):
        """Écrit dans le fichier log"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def log_connection(self, db_path):
        """Log une connexion à la BDD (mode debug uniquement)"""
        if self.debug_mode:
            self._write_log('INFO', f'Connexion établie à {db_path}')
    
    def log_disconnection(self):
        """Log une déconnexion (mode debug uniquement)"""
        if self.debug_mode:
            self._write_log('INFO', 'Déconnexion de la base de données')
    
    def log_query(self, query):
        """Log une requête SQL (mode debug uniquement)"""
        if self.debug_mode:
            clean_query = ' '.join(query.split())
            self._write_log('QUERY', clean_query)
    
    def log_error(self, error_message):
        """Log une erreur (tous modes)"""
        self._write_log('ERROR', error_message)
    
    def log_query_error(self, query, error):
        """Log une erreur de requête (tous modes)"""
        clean_query = ' '.join(query.split())
        self._write_log('ERROR', f'Requête: {clean_query} | Erreur: {error}')