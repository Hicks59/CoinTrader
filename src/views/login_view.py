import tkinter as tk
from src.controllers.account_controller import AccountController
from src.components.ui_component import Button

class LoginView:
    """Vue de connexion"""
    
    def __init__(self, root, theme, on_login_success, on_show_signup):
        self.root = root
        self.theme = theme
        self.on_login_success = on_login_success
        self.on_show_signup = on_show_signup
        
        self.FONT_FAMILY = "Segoe UI"
        self.APP_NAME = "CoinTrader"
        self.APP_VERSION = "1.0.0"
        
        self.render()
    
    def render(self):
        """Affiche l'écran de connexion"""
        self.root.title(f"{self.APP_NAME} - Connexion")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.root.configure(bg=self.theme['bg_primary'])
        self.root.eval("tk::PlaceWindow . center")
        
        main_frame = tk.Frame(self.root, bg=self.theme['bg_primary'])
        main_frame.pack(expand=True, fill='both', padx=40, pady=40)
        
        # Logo / Titre
        tk.Label(
            main_frame,
            text=self.APP_NAME,
            font=(self.FONT_FAMILY, 28, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['accent']
        ).pack(pady=(0, 10))
        
        tk.Label(
            main_frame,
            text=f"v{self.APP_VERSION}",
            font=(self.FONT_FAMILY, 9),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_secondary']
        ).pack(pady=(0, 40))
        
        # Formulaire
        form_frame = tk.Frame(main_frame, bg=self.theme['bg_primary'])
        form_frame.pack(fill='x')
        
        # Username
        tk.Label(
            form_frame,
            text="Nom d'utilisateur",
            font=(self.FONT_FAMILY, 10),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary'],
            anchor='w'
        ).pack(fill='x', pady=(0, 5))
        
        self.username_entry = tk.Entry(
            form_frame,
            font=(self.FONT_FAMILY, 11),
            bg=self.theme['input_bg'],
            fg=self.theme['text_primary'],
            relief='solid',
            borderwidth=1,
            insertbackground=self.theme['text_primary']
        )
        self.username_entry.pack(fill='x', ipady=8)
        
        # Password
        tk.Label(
            form_frame,
            text="Mot de passe",
            font=(self.FONT_FAMILY, 10),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary'],
            anchor='w'
        ).pack(fill='x', pady=(20, 5))
        
        self.password_entry = tk.Entry(
            form_frame,
            font=(self.FONT_FAMILY, 11),
            bg=self.theme['input_bg'],
            fg=self.theme['text_primary'],
            show='•',
            relief='solid',
            borderwidth=1,
            insertbackground=self.theme['text_primary']
        )
        self.password_entry.pack(fill='x', ipady=8)
        self.password_entry.bind('<Return>', lambda e: self.login())
        
        # Message d'erreur
        self.error_label = tk.Label(
            form_frame,
            text="",
            font=(self.FONT_FAMILY, 9),
            bg=self.theme['bg_primary'],
            fg='#F44336',
            anchor='w'
        )
        self.error_label.pack(fill='x', pady=(10, 0))
        
        # Bouton connexion
        tk.Button(
            form_frame,
            text="Se connecter",
            font=(self.FONT_FAMILY, 11, 'bold'),
            bg=self.theme['accent'],
            fg=self.theme['button_text'],
            activebackground=self.theme['accent'],
            relief='flat',
            cursor='hand2',
            command=self.login
        ).pack(fill='x', pady=(30, 0), ipady=14)
        
        # Lien créer un compte
        signup_frame = tk.Frame(form_frame, bg=self.theme['bg_primary'])
        signup_frame.pack(pady=(20, 0))
        
        signup_label = tk.Label(
            signup_frame,
            text="Créer un compte",
            font=(self.FONT_FAMILY, 9),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_secondary'],
            cursor='hand2'
        )
        signup_label.pack()
        signup_label.bind('<Button-1>', lambda e: self.on_show_signup())
    
    def login(self):
        """Traite la connexion"""
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        account_controller = AccountController()
        result = account_controller.login(username, password)
        
        if result['success']:
            self.on_login_success(result['user_data'])
        else:
            self.error_label.config(text=result['message'])