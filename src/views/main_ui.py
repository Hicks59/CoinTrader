import os
import tkinter as tk
from tkinter import messagebox

APP_NAME = "CoinTrader"
APP_VERSION = "1.0.0"
FONT_FAMILY = "Segoe UI"
TK_CENTER_WINDOW = "tk::PlaceWindow . center"

class Theme:
    """Gestion des thèmes clair/sombre"""
    
    LIGHT = {
        'bg_primary': '#FFFFFF',
        'bg_secondary': '#F5F5F5',
        'bg_header': '#FAFAFA',
        'text_primary': '#1A1A1A',
        'text_secondary': '#666666',
        'accent': '#2E7D32',
        'border': '#E0E0E0',
        'button_bg': '#2E7D32',
        'button_text': '#FFFFFF',
        'input_bg': '#FFFFFF',
        'input_border': '#CCCCCC'
    }
    
    DARK = {
        'bg_primary': '#1E1E1E',
        'bg_secondary': '#2D2D2D',
        'bg_header': '#252525',
        'text_primary': '#E0E0E0',
        'text_secondary': '#A0A0A0',
        'accent': '#4CAF50',
        'border': '#3A3A3A',
        'button_bg': '#4CAF50',
        'button_text': '#FFFFFF',
        'input_bg': '#2D2D2D',
        'input_border': '#4A4A4A'
    }
    
    @staticmethod
    def get(theme_name='dark'):
        return Theme.DARK if theme_name == 'dark' else Theme.LIGHT

class MainApplication:
    """Application principale - Gère la navigation et l'interface"""
    
    def __init__(self, root, user_data, theme_name='dark', window_geometry=None):
        self.root = root
        self.user_data = user_data
        self.current_theme = theme_name
        self.theme = Theme.get(self.current_theme)
        self.window_geometry = window_geometry
        self.current_page = 'dashboard'
        
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface principale"""
        self.root.title(f"{APP_NAME} - Tableau de bord")
        
        if self.window_geometry:
            self.root.geometry(self.window_geometry)
        else:
            self.root.geometry("1200x700")
            self.root.eval(TK_CENTER_WINDOW)
        
        self.root.resizable(True, True)
        self.root.configure(bg=self.theme['bg_primary'])
        
        # Header
        self.create_header()
        
        # Container principal
        main_container = tk.Frame(self.root, bg=self.theme['bg_primary'])
        main_container.pack(fill='both', expand=True)
        
        # Zone centrale pour le contenu
        self.content_frame = tk.Frame(
            main_container,
            bg=self.theme['bg_primary']
        )
        self.content_frame.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        
        # Menu à droite
        self.create_right_menu(main_container)
        
        # Afficher le dashboard par défaut
        self.show_dashboard()
    
    def create_header(self):
        """Crée le header de l'application"""
        header = tk.Frame(
            self.root,
            bg=self.theme['bg_header'],
            height=60
        )
        header.pack(fill='x')
        header.pack_propagate(False)
        
        # Logo / Nom app
        tk.Label(
            header,
            text=APP_NAME,
            font=(FONT_FAMILY, 16, 'bold'),
            bg=self.theme['bg_header'],
            fg=self.theme['accent']
        ).pack(side='left', padx=20)
        
        # Nom de l'utilisateur
        self.user_label = tk.Label(
            header,
            text=f"👤 {self.user_data['prenom']} {self.user_data['nom']}",
            font=(FONT_FAMILY, 10),
            bg=self.theme['bg_header'],
            fg=self.theme['text_secondary']
        )
        self.user_label.pack(side='right', padx=20)
        
        # Bouton toggle thème
        self.theme_button = tk.Button(
            header,
            text=self.get_theme_icon(),
            font=(FONT_FAMILY, 14),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary'],
            activebackground=self.theme['bg_primary'],
            relief='flat',
            cursor='hand2',
            command=self.toggle_theme
        )
        self.theme_button.pack(side='right', padx=5)
    
    def create_right_menu(self, parent):
        """Crée le menu latéral"""
        menu_frame = tk.Frame(
            parent,
            bg=self.theme['bg_secondary'],
            width=200
        )
        menu_frame.pack(side='right', fill='y')
        menu_frame.pack_propagate(False)
        
        tk.Label(
            menu_frame,
            text="MENU",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_secondary']
        ).pack(pady=(20, 10), padx=20, anchor='w')
        
        # Items du menu
        menu_items = [
            ("📊  Tableau de bord", self.show_dashboard),
            ("🤖  Mes bots", self.show_bots),
            ("🏦  Plateformes", self.show_platforms),
            ("📜  Historique", self.show_history),
            ("👤  Mon profil", self.show_profile),
            ("⚙️  Paramètres", self.show_settings)
        ]
        
        for item_text, command in menu_items:
            tk.Button(
                menu_frame,
                text=item_text,
                font=(FONT_FAMILY, 10),
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_primary'],
                activebackground=self.theme['bg_primary'],
                relief='flat',
                anchor='w',
                cursor='hand2',
                command=command
            ).pack(fill='x', padx=10, pady=2)
        
        # Bouton Déconnexion
        tk.Button(
            menu_frame,
            text="🚪  Déconnexion",
            font=(FONT_FAMILY, 10),
            bg=self.theme['bg_secondary'],
            fg='#FF9800',
            activebackground=self.theme['bg_primary'],
            relief='flat',
            anchor='w',
            cursor='hand2',
            command=self.logout
        ).pack(fill='x', padx=10, pady=(20, 2))
        
        # Bouton Quitter
        tk.Button(
            menu_frame,
            text="❌  Quitter",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['bg_secondary'],
            fg='#F44336',
            activebackground=self.theme['bg_primary'],
            relief='flat',
            anchor='w',
            cursor='hand2',
            command=self.quit_application
        ).pack(fill='x', padx=10, pady=2)
    
    def clear_content(self):
        """Vide le contenu de la zone centrale"""
        self.root.unbind_all("<MouseWheel>")
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_dashboard(self):
        """Affiche le tableau de bord"""
        self.current_page = 'dashboard'
        self.clear_content()
        
        from src.views.dashboard_view import DashboardView
        DashboardView(self.content_frame, self.theme)
    
    def show_bots(self):
        """Affiche la liste des bots"""
        self.current_page = 'bots'
        self.clear_content()
        
        from src.views.bot_list_view import BotListView
        BotListView(
            parent_frame=self.content_frame,
            theme=self.theme,
            on_add_bot_callback=self.show_add_bot_form
        )
    
    def show_add_bot_form(self):
        """Affiche le formulaire d'ajout de bot"""
        self.current_page = 'add_bot'
        self.clear_content()
        
        from src.views.bot_form_view import BotFormView
        BotFormView(
            parent_frame=self.content_frame,
            theme=self.theme,
            user_data=self.user_data,
            on_back_callback=self.show_bots,
            on_success_callback=self.show_bots
        )
    
    def show_history(self):
        """Affiche l'historique des transactions"""
        self.current_page = 'history'
        self.clear_content()
        
        from src.views.history_view import HistoryView
        HistoryView(self.content_frame, self.theme)
    
    def show_profile(self):
        """Affiche le profil utilisateur"""
        self.current_page = 'profile'
        self.clear_content()
        
        from src.views.profile_view import ProfileView
        ProfileView(
            parent_frame=self.content_frame,
            theme=self.theme,
            user_data=self.user_data,
            on_update_callback=self.update_user_header
        )
    
    def show_settings(self):
        """Affiche les paramètres"""
        self.current_page = 'settings'
        self.clear_content()
        
        from src.views.settings_view import SettingsView
        SettingsView(self.content_frame, self.theme)

    def show_platforms(self):
        """Affiche la gestion des plateformes/exchanges"""
        self.current_page = 'platforms'
        self.clear_content()

        from src.views.platforms_view import PlatformsView
        PlatformsView(
            parent_frame=self.content_frame,
            theme=self.theme,
            user_data=self.user_data
        )
    
    def update_user_header(self, user_data):
        """Met à jour le nom dans le header"""
        self.user_data.update(user_data)
        if hasattr(self, 'user_label'):
            self.user_label.config(
                text=f"👤 {self.user_data['prenom']} {self.user_data['nom']}"
            )
    
    def get_theme_icon(self):
        """Retourne l'icône du thème"""
        return '🌙' if self.current_theme == 'light' else '☀'
    
    def toggle_theme(self):
        """Bascule entre thème clair et sombre"""
        self.current_theme = 'light' if self.current_theme == 'dark' else 'dark'
        self.theme = Theme.get(self.current_theme)
        
        self.update_all_colors()
        
        if hasattr(self, 'theme_button'):
            self.theme_button.config(text=self.get_theme_icon())
    
    def update_all_colors(self):
        """Met à jour les couleurs de tous les widgets"""
        self.root.config(bg=self.theme['bg_primary'])
        self._update_widget_colors(self.root)
    
    def _update_widget_colors(self, widget):
        """Met à jour les couleurs d'un widget récursivement"""
        widget_class = widget.winfo_class()
        
        try:
            if widget_class == 'Frame':
                self._update_frame_colors(widget)
            elif widget_class == 'Label':
                self._update_label_colors(widget)
            elif widget_class == 'Button':
                self._update_button_colors(widget)
            elif widget_class == 'Entry':
                self._update_entry_colors(widget)
        except tk.TclError:
            pass
        
        for child in widget.winfo_children():
            self._update_widget_colors(child)
    
    def _is_header_bg(self, bg_color):
        return bg_color in [Theme.DARK['bg_header'], Theme.LIGHT['bg_header']]
    
    def _is_secondary_bg(self, bg_color):
        return bg_color in [Theme.DARK['bg_secondary'], Theme.LIGHT['bg_secondary']]
    
    def _is_accent_color(self, color):
        return color in [Theme.DARK['accent'], Theme.LIGHT['accent']]
    
    def _is_button_bg(self, bg_color):
        return bg_color in [Theme.DARK['accent'], Theme.LIGHT['accent'], 
                           Theme.DARK['button_bg'], Theme.LIGHT['button_bg']]
    
    def _update_frame_colors(self, widget):
        current_bg = widget.cget('bg')
        if self._is_header_bg(current_bg):
            widget.config(bg=self.theme['bg_header'])
        elif self._is_secondary_bg(current_bg):
            widget.config(bg=self.theme['bg_secondary'])
        else:
            widget.config(bg=self.theme['bg_primary'])
    
    def _update_label_colors(self, widget):
        current_fg = widget.cget('fg')
        current_bg = widget.cget('bg')
        
        if self._is_header_bg(current_bg):
            widget.config(bg=self.theme['bg_header'])
        elif self._is_secondary_bg(current_bg):
            widget.config(bg=self.theme['bg_secondary'])
        else:
            widget.config(bg=self.theme['bg_primary'])
        
        if current_fg in ['#F44336', '#4CAF50', '#FF9800']:
            return
        
        if self._is_accent_color(current_fg):
            widget.config(fg=self.theme['accent'])
        elif current_fg in [Theme.DARK['text_secondary'], Theme.LIGHT['text_secondary'], 'gray']:
            widget.config(fg=self.theme['text_secondary'])
        else:
            widget.config(fg=self.theme['text_primary'])
    
    def _update_button_colors(self, widget):
        current_bg = widget.cget('bg')
        current_fg = widget.cget('fg')
        
        if self._is_button_bg(current_bg):
            widget.config(
                bg=self.theme['button_bg'],
                fg=self.theme['button_text'],
                activebackground=self.theme['accent']
            )
        elif current_fg == '#F44336':
            widget.config(
                bg=self.theme['bg_secondary'],
                fg='#F44336',
                activebackground=self.theme['bg_primary']
            )
        elif current_fg == '#FF9800':
            widget.config(
                bg=self.theme['bg_secondary'],
                fg='#FF9800',
                activebackground=self.theme['bg_primary']
            )
        else:
            widget.config(
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_primary'],
                activebackground=self.theme['bg_primary']
            )
    
    def _update_entry_colors(self, widget):
        state = widget.cget('state')
        if state == 'readonly':
            widget.config(
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_primary']
            )
        else:
            widget.config(
                bg=self.theme['input_bg'],
                fg=self.theme['text_primary'],
                insertbackground=self.theme['text_primary']
            )
    
    def logout(self):
        """Déconnexion"""
        if messagebox.askyesno(
            "Déconnexion",
            "Voulez-vous vous déconnecter ?\n\nℹ️ Les bots de trading continueront de fonctionner en arrière-plan."
        ):
            current_geometry = self.root.geometry()
            
            for widget in self.root.winfo_children():
                widget.destroy()
            
            def on_login_success(user_data):
                for widget in self.root.winfo_children():
                    widget.destroy()
                MainApplication(self.root, user_data, self.current_theme, current_geometry)
            
            from src.views.login_view import LoginView
            
            def show_signup():
                for widget in self.root.winfo_children():
                    widget.destroy()
                from src.views.signup_view import SignupView
                SignupView(self.root, Theme.get(self.current_theme), on_login_success, show_login)
            
            def show_login():
                for widget in self.root.winfo_children():
                    widget.destroy()
                LoginView(self.root, Theme.get(self.current_theme), on_login_success, show_signup)
            
            LoginView(self.root, Theme.get(self.current_theme), on_login_success, show_signup)
    
    def quit_application(self):
        """Quitte l'application"""
        if messagebox.askyesno("Quitter", "Voulez-vous vraiment quitter l'application ?"):
            self.root.quit()
            self.root.destroy()

# Point d'entrée de l'application
if __name__ == "__main__":
    # Nettoyage automatique du cache
    print("🧹 Nettoyage du cache...")
    import shutil
    try:
        cache_count = 0
        for root, dirs, files in os.walk('.'):
            if '__pycache__' in dirs:
                pycache_path = os.path.join(root, '__pycache__')
                shutil.rmtree(pycache_path)
                cache_count += 1
        if cache_count > 0:
            print(f"✓ {cache_count} dossier(s) cache supprimés")
        else:
            print("✓ Aucun cache à nettoyer")
    except Exception as e:
        print(f"⚠ Erreur nettoyage cache: {e}")
    
    print("🚀 Démarrage de l'application...")
    
    root = tk.Tk()
    
    def on_login_success(user_data):
        for widget in root.winfo_children():
            widget.destroy()
        MainApplication(root, user_data, 'dark')
    
    from src.views.login_view import LoginView
    
    def show_signup():
        for widget in root.winfo_children():
            widget.destroy()
        from src.views.signup_view import SignupView
        SignupView(root, Theme.get('dark'), on_login_success, show_login)
    
    def show_login():
        for widget in root.winfo_children():
            widget.destroy()
        LoginView(root, Theme.get('dark'), on_login_success, show_signup)
    
    LoginView(root, Theme.get('dark'), on_login_success, show_signup)
    root.mainloop()