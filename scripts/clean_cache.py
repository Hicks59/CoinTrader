#!/usr/bin/env python3
"""
Script de nettoyage du cache de l'application Kipacoin
Usage: python clean_cache.py [options]
"""
import os
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta

class CacheCleaner:
    """Nettoyeur de cache pour Kipacoin"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.stats = {
            'pycache_deleted': 0,
            'logs_deleted': 0,
            'temp_deleted': 0,
            'size_freed': 0
        }
    
    def log(self, message):
        """Affiche un message si verbose activé"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def get_dir_size(self, path):
        """Calcule la taille d'un dossier en octets"""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
        except Exception:
            pass
        return total_size
    
    def format_size(self, size_bytes):
        """Formate une taille en octets vers une chaîne lisible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def clean_pycache(self):
        """Nettoie tous les fichiers __pycache__ et .pyc"""
        self.log("Nettoyage des fichiers Python cache...")
        
        # Trouver tous les dossiers __pycache__
        for root, dirs, files in os.walk('.'):
            # Nettoyer les dossiers __pycache__
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                size = self.get_dir_size(pycache_path)
                try:
                    shutil.rmtree(pycache_path)
                    self.stats['pycache_deleted'] += 1
                    self.stats['size_freed'] += size
                    self.log(f"  ✓ Supprimé: {pycache_path} ({self.format_size(size)})")
                except Exception as e:
                    self.log(f"  ✗ Erreur: {pycache_path} - {e}")
            
            # Nettoyer les fichiers .pyc
            for filename in files:
                if filename.endswith('.pyc'):
                    pyc_path = os.path.join(root, filename)
                    size = os.path.getsize(pyc_path)
                    try:
                        os.remove(pyc_path)
                        self.stats['pycache_deleted'] += 1
                        self.stats['size_freed'] += size
                        self.log(f"  ✓ Supprimé: {pyc_path}")
                    except Exception as e:
                        self.log(f"  ✗ Erreur: {pyc_path} - {e}")
    
    def clean_logs(self, keep_days=7):
        """
        Nettoie les anciens fichiers de logs
        
        Args:
            keep_days (int): Nombre de jours à conserver
        """
        self.log(f"Nettoyage des logs (conservation: {keep_days} jours)...")
        
        logs_dir = Path('logs')
        if not logs_dir.exists():
            self.log("  ℹ  Dossier logs inexistant")
            return
        
        cutoff_date = datetime.now() - timedelta(days=keep_days)
        
        for log_file in logs_dir.glob('*.log'):
            try:
                file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                
                if file_time < cutoff_date:
                    size = log_file.stat().st_size
                    log_file.unlink()
                    self.stats['logs_deleted'] += 1
                    self.stats['size_freed'] += size
                    self.log(f"  ✓ Supprimé: {log_file} ({self.format_size(size)})")
            except Exception as e:
                self.log(f"  ✗ Erreur: {log_file} - {e}")
        
        # Nettoyer les archives
        archives_dir = logs_dir / 'archives'
        if archives_dir.exists():
            for archive_file in archives_dir.glob('*'):
                try:
                    file_time = datetime.fromtimestamp(archive_file.stat().st_mtime)
                    
                    if file_time < cutoff_date:
                        size = archive_file.stat().st_size
                        archive_file.unlink()
                        self.stats['logs_deleted'] += 1
                        self.stats['size_freed'] += size
                        self.log(f"  ✓ Supprimé: {archive_file} ({self.format_size(size)})")
                except Exception as e:
                    self.log(f"  ✗ Erreur: {archive_file} - {e}")
    
    def clean_temp_files(self):
        """Nettoie les fichiers temporaires"""
        self.log("Nettoyage des fichiers temporaires...")
        
        temp_patterns = ['*.tmp', '*.temp', '*~', '.DS_Store', 'Thumbs.db']
        
        for root, dirs, files in os.walk('.'):
            for filename in files:
                for pattern in temp_patterns:
                    if Path(filename).match(pattern):
                        temp_path = os.path.join(root, filename)
                        try:
                            size = os.path.getsize(temp_path)
                            os.remove(temp_path)
                            self.stats['temp_deleted'] += 1
                            self.stats['size_freed'] += size
                            self.log(f"  ✓ Supprimé: {temp_path}")
                        except Exception as e:
                            self.log(f"  ✗ Erreur: {temp_path} - {e}")
    
    def archive_logs(self):
        """Archive les logs actuels dans le dossier archives"""
        self.log("Archivage des logs actuels...")
        
        logs_dir = Path('logs')
        if not logs_dir.exists():
            self.log("  ℹ  Dossier logs inexistant")
            return
        
        archives_dir = logs_dir / 'archives'
        archives_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for log_file in logs_dir.glob('*.log'):
            try:
                archive_name = f"{log_file.stem}_{timestamp}.log"
                archive_path = archives_dir / archive_name
                
                # Copier le fichier
                shutil.copy2(log_file, archive_path)
                
                # Vider le fichier original
                with open(log_file, 'w') as f:
                    f.write(f"# Log archivé le {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                
                self.log(f"  ✓ Archivé: {log_file} → {archive_path}")
            except Exception as e:
                self.log(f"  ✗ Erreur: {log_file} - {e}")
    
    def print_summary(self):
        """Affiche un résumé des opérations"""
        print("\n" + "="*60)
        print("RÉSUMÉ DU NETTOYAGE")
        print("="*60)
        print(f"Python cache supprimés:  {self.stats['pycache_deleted']}")
        print(f"Logs supprimés:          {self.stats['logs_deleted']}")
        print(f"Fichiers temp supprimés: {self.stats['temp_deleted']}")
        print(f"Espace libéré:           {self.format_size(self.stats['size_freed'])}")
        print("="*60)
    
    def clean_all(self, keep_logs_days=7, archive=False):
        """
        Nettoie tout le cache
        
        Args:
            keep_logs_days (int): Nombre de jours de logs à conserver
            archive (bool): Archiver les logs avant nettoyage
        """
        self.log("\n🧹 NETTOYAGE DU CACHE KIPACOIN\n")
        
        if archive:
            self.archive_logs()
        
        self.clean_pycache()
        self.clean_logs(keep_days=keep_logs_days)
        self.clean_temp_files()
        
        self.print_summary()


def main():
    parser = argparse.ArgumentParser(
        description='Nettoie le cache de l\'application Kipacoin'
    )
    parser.add_argument(
        '--pycache-only',
        action='store_true',
        help='Nettoyer uniquement le cache Python'
    )
    parser.add_argument(
        '--logs-only',
        action='store_true',
        help='Nettoyer uniquement les logs'
    )
    parser.add_argument(
        '--keep-logs',
        type=int,
        default=7,
        help='Nombre de jours de logs à conserver (défaut: 7)'
    )
    parser.add_argument(
        '--archive',
        action='store_true',
        help='Archiver les logs actuels avant nettoyage'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Mode silencieux (pas de sortie détaillée)'
    )
    
    args = parser.parse_args()
    
    cleaner = CacheCleaner(verbose=not args.quiet)
    
    if args.pycache_only:
        cleaner.clean_pycache()
        cleaner.print_summary()
    elif args.logs_only:
        if args.archive:
            cleaner.archive_logs()
        cleaner.clean_logs(keep_days=args.keep_logs)
        cleaner.print_summary()
    else:
        cleaner.clean_all(keep_logs_days=args.keep_logs, archive=args.archive)


if __name__ == "__main__":
    main()