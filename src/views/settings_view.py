import os
import tkinter as tk
from tkinter import messagebox
from typing import Dict
from datetime import datetime, timedelta
from pathlib import Path

FONT_FAMILY = "Segoe UI"

class SettingsView:
    """Vue des paramètres"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        
        self.render()
    
    def render(self):
        """Affiche les paramètres"""
        tk.Label(
            self.parent_frame,
            text="Paramètres",
            font=(FONT_FAMILY, 20, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 30))
        
        # Section Nettoyage
        section_frame = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        section_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            section_frame,
            text="Nettoyage du cache",
            font=(FONT_FAMILY, 14, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 15))
        
        tk.Label(
            section_frame,
            text="Libérez de l'espace en supprimant les fichiers temporaires et les anciens logs.",
            font=(FONT_FAMILY, 9),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_secondary'],
            anchor='w',
            wraplength=600
        ).pack(anchor='w', pady=(0, 15))
        
        # Boutons de nettoyage
        buttons_frame = tk.Frame(section_frame, bg=self.theme['bg_primary'])
        buttons_frame.pack(anchor='w', fill='x')
        
        tk.Button(
            buttons_frame,
            text="Nettoyer le cache Python",
            font=(FONT_FAMILY, 10),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary'],
            activebackground=self.theme['bg_primary'],
            relief='flat',
            cursor='hand2',
            command=self.clean_pycache
        ).pack(side='left', padx=(0, 10), ipadx=15, ipady=8)
        
        tk.Button(
            buttons_frame,
            text="Nettoyer les logs (>7 jours)",
            font=(FONT_FAMILY, 10),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary'],
            activebackground=self.theme['bg_primary'],
            relief='flat',
            cursor='hand2',
            command=self.clean_logs
        ).pack(side='left', padx=(0, 10), ipadx=15, ipady=8)
        
        tk.Button(
            buttons_frame,
            text="Nettoyer tout",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['accent'],
            fg=self.theme['button_text'],
            activebackground=self.theme['accent'],
            relief='flat',
            cursor='hand2',
            command=self.clean_all_cache
        ).pack(side='left', ipadx=15, ipady=8)
        
        # Message de statut
        self.clean_status_label = tk.Label(
            section_frame,
            text="",
            font=(FONT_FAMILY, 9),
            bg=self.theme['bg_primary'],
            fg='#4CAF50',
            anchor='w'
        )
        self.clean_status_label.pack(anchor='w', pady=(15, 0))
    
    def clean_pycache(self):
        """Nettoie le cache Python"""
        try:
            stats = self._remove_pycache_dirs()
            size_mb = stats['size'] / (1024 * 1024)
            
            self.clean_status_label.config(
                text=f"✓ {stats['count']} dossier(s) cache supprimé(s) - {size_mb:.2f} MB libérés",
                fg='#4CAF50'
            )
        except Exception as e:
            self.clean_status_label.config(text=f"✗ Erreur: {str(e)}", fg='#F44336')
    
    def _remove_pycache_dirs(self) -> Dict[str, int]:
        """Supprime tous les dossiers __pycache__"""
        import shutil
        count = 0
        total_size = 0
        
        for root, dirs, files in os.walk('.'):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                
                for dirpath, dirnames, filenames in os.walk(pycache_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                
                shutil.rmtree(pycache_path)
                count += 1
        
        return {'count': count, 'size': total_size}
    
    def clean_logs(self):
        """Nettoie les anciens logs"""
        try:
            stats = self._remove_old_logs(days=7)
            size_mb = stats['size'] / (1024 * 1024)
            
            self.clean_status_label.config(
                text=f"✓ {stats['count']} fichier(s) log supprimé(s) - {size_mb:.2f} MB libérés",
                fg='#4CAF50'
            )
        except Exception as e:
            self.clean_status_label.config(text=f"✗ Erreur: {str(e)}", fg='#F44336')
    
    def _remove_old_logs(self, days: int = 7) -> Dict[str, int]:
        """Supprime les logs plus anciens que X jours"""
        count = 0
        total_size = 0
        cutoff_date = datetime.now() - timedelta(days=days)
        logs_dir = Path('logs')
        
        if not logs_dir.exists():
            return {'count': 0, 'size': 0}
        
        stats_main = self._remove_files_older_than(logs_dir, '*.log', cutoff_date)
        count += stats_main['count']
        total_size += stats_main['size']
        
        archives_dir = logs_dir / 'archives'
        if archives_dir.exists():
            stats_archives = self._remove_files_older_than(archives_dir, '*', cutoff_date)
            count += stats_archives['count']
            total_size += stats_archives['size']
        
        return {'count': count, 'size': total_size}
    
    def _remove_files_older_than(self, directory, pattern: str, cutoff_date) -> Dict[str, int]:
        """Supprime les fichiers correspondant au pattern et plus anciens que cutoff_date"""
        count = 0
        total_size = 0
        
        for file_path in Path(directory).glob(pattern):
            if not file_path.is_file():
                continue
            
            file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            if file_time < cutoff_date:
                total_size += file_path.stat().st_size
                file_path.unlink()
                count += 1
        
        return {'count': count, 'size': total_size}
    
    def clean_all_cache(self):
        """Nettoie tout le cache"""
        if not messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment nettoyer tout le cache ?\n\n"
            "Cela supprimera :\n"
            "- Le cache Python (__pycache__)\n"
            "- Les logs de plus de 7 jours\n"
            "- Les fichiers temporaires"
        ):
            return
        
        try:
            pycache_stats = self._remove_pycache_dirs()
            logs_stats = self._remove_old_logs(days=7)
            
            total_count = pycache_stats['count'] + logs_stats['count']
            total_size_mb = (pycache_stats['size'] + logs_stats['size']) / (1024 * 1024)
            
            self.clean_status_label.config(
                text=f"✓ Nettoyage complet : {total_count} élément(s) supprimé(s) - {total_size_mb:.2f} MB libérés",
                fg='#4CAF50'
            )
        except Exception as e:
            self.clean_status_label.config(text=f"✗ Erreur: {str(e)}", fg='#F44336')