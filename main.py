import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Constantes
FONT_FAMILY = "Segoe UI"
APP_NAME = "CoinTrader"
APP_VERSION = "1.0.0"
WINDOW_BG = '#1E1E1E'
ACCENT_COLOR = '#4CAF50'
TEXT_SECONDARY = '#A0A0A0'
TEXT_TERTIARY = '#666666'
PROGRESS_BG = '#2D2D2D'

class LoaderScreen:
    """Écran de chargement au démarrage"""
    
    def __init__(self, root, on_complete):
        self.root = root
        self.on_complete = on_complete
        self.error_occurred = False
        
        # Configuration de la fenêtre
        self.root.title(APP_NAME)
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        self.root.configure(bg=WINDOW_BG)
        
        # Centrer la fenêtre
        self.root.eval("tk::PlaceWindow . center")
        
        # Retirer la bordure de la fenêtre
        self.root.overrideredirect(True)
        
        self.create_ui()
        self.start_loading()
    
    def create_ui(self):
        """Crée l'interface du loader"""
        # Frame principal
        main_frame = tk.Frame(self.root, bg=WINDOW_BG)
        main_frame.pack(expand=True, fill='both')
        
        # Logo / Titre
        title_label = tk.Label(
            main_frame,
            text=APP_NAME,
            font=(FONT_FAMILY, 32, 'bold'),
            bg=WINDOW_BG,
            fg=ACCENT_COLOR
        )
        title_label.pack(pady=(60, 10))
        
        # Sous-titre
        subtitle_label = tk.Label(
            main_frame,
            text="Trading Bot Platform",
            font=(FONT_FAMILY, 10),
            bg=WINDOW_BG,
            fg=TEXT_SECONDARY
        )
        subtitle_label.pack(pady=(0, 40))
        
        # Barre de progression
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=PROGRESS_BG,
            bordercolor=WINDOW_BG,
            background=ACCENT_COLOR,
            lightcolor=ACCENT_COLOR,
            darkcolor=ACCENT_COLOR
        )
        
        self.progress = ttk.Progressbar(
            main_frame,
            style="Custom.Horizontal.TProgressbar",
            length=300,
            mode='indeterminate'
        )
        self.progress.pack(pady=(0, 20))
        
        # Texte de chargement
        self.loading_label = tk.Label(
            main_frame,
            text="Chargement...",
            font=(FONT_FAMILY, 9),
            bg=WINDOW_BG,
            fg=TEXT_SECONDARY
        )
        self.loading_label.pack()
        
        # Version
        version_label = tk.Label(
            main_frame,
            text=f"v{APP_VERSION}",
            font=(FONT_FAMILY, 8),
            bg=WINDOW_BG,
            fg=TEXT_TERTIARY
        )
        version_label.pack(side='bottom', pady=10)
    
    def start_loading(self):
        """Démarre l'animation de chargement"""
        self.progress.start(10)
        
        # Lancer le chargement dans un thread séparé
        thread = threading.Thread(target=self.load_application)
        thread.daemon = True
        thread.start()
    
    def load_application(self):
        """Charge l'application en utilisant le controller"""
        try:
            from src.controllers.init_controller import InitController
            
            init_controller = InitController()
            
            # Exécuter toutes les vérifications
            self.update_status("Initialisation...")
            time.sleep(0.3)
            
            result = init_controller.run_all_checks()
            
            # Afficher chaque étape
            for check_result in result['results']:
                self.update_status(check_result['step'] + "...")
                time.sleep(0.4)
                
                if not check_result['success']:
                    self.show_error(check_result['message'])
                    return
            
            # Si tout est OK
            if result['success']:
                self.update_status("Chargement des modules...")
                time.sleep(0.4)
                
                self.update_status("Préparation de l'interface...")
                time.sleep(0.3)
                
                # Terminer le chargement
                self.root.after(0, self.finish_loading)
            else:
                self.show_error(result.get('error', 'Erreur inconnue'))
            
        except Exception as e:
            self.show_error(f"Erreur lors du chargement : {str(e)}")
    
    def update_status(self, message):
        """Met à jour le message de statut"""
        self.root.after(0, lambda: self.loading_label.config(text=message))
        print(f"✓ {message}")
    
    def show_error(self, message):
        """Affiche une erreur et quitte"""
        self.error_occurred = True
        print(f"\n✗ ERREUR: {message}\n")
        
        def show_message():
            self.progress.stop()
            self.root.destroy()
            
            error_root = tk.Tk()
            error_root.withdraw()
            
            messagebox.showerror(
                "Erreur de chargement",
                f"{message}\n\nL'application va se fermer."
            )
            
            error_root.destroy()
            sys.exit(1)
        
        self.root.after(0, show_message)
    
    def finish_loading(self):
        """Termine le chargement et lance l'application"""
        if self.error_occurred:
            return
        
        self.progress.stop()
        self.loading_label.config(text="Prêt !")
        time.sleep(0.3)
        
        # Détruire le loader
        self.root.destroy()
        
        # Lancer l'application principale
        self.on_complete()

def launch_login():
    """Lance l'écran de connexion"""
    root = tk.Tk()
    
    # Importer les classes nécessaires
    from src.views.main_ui import MainApplication, Theme
    from src.views.login_view import LoginView
    from src.views.signup_view import SignupView
    
    # Callback après connexion réussie
    def on_login_success(user_data):
        for widget in root.winfo_children():
            widget.destroy()
        MainApplication(root, user_data, 'dark')
    
    # Callback pour afficher l'inscription
    def show_signup():
        for widget in root.winfo_children():
            widget.destroy()
        SignupView(root, Theme.get('dark'), on_login_success, show_login)
    
    # Callback pour afficher la connexion
    def show_login():
        for widget in root.winfo_children():
            widget.destroy()
        LoginView(root, Theme.get('dark'), on_login_success, show_signup)
    
    # Afficher l'écran de connexion
    LoginView(root, Theme.get('dark'), on_login_success, show_signup)
    
    # Lancer la boucle principale
    root.mainloop()

def main():
    """Point d'entrée principal de l'application"""
    print("=" * 60)
    print(f"🚀 Démarrage de {APP_NAME} v{APP_VERSION}")
    print("=" * 60)
    
    # Créer la fenêtre du loader
    loader_root = tk.Tk()
    
    # Lancer le loader
    LoaderScreen(loader_root, on_complete=launch_login)
    
    # Boucle principale du loader
    loader_root.mainloop()

if __name__ == "__main__":
    main()