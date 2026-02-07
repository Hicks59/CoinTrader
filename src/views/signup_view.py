import tkinter as tk
from tkinter import messagebox
from src.controllers.account_controller import AccountController

class SignupView:
    """Vue d'inscription"""
    
    def __init__(self, root, theme, on_success, on_show_login):
        self.root = root
        self.theme = theme
        self.on_success = on_success
        self.on_show_login = on_show_login
        
        self.FONT_FAMILY = "Segoe UI"
        self.APP_NAME = "CoinTrader"
        
        self.render()
    
    def render(self):
        """Affiche l'écran d'inscription"""
        self.root.title(f"{self.APP_NAME} - Inscription")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        self.root.configure(bg=self.theme['bg_primary'])
        self.root.eval("tk::PlaceWindow . center")
        
        main_frame = tk.Frame(self.root, bg=self.theme['bg_primary'])
        main_frame.pack(expand=True, fill='both', padx=40, pady=30)
        
        # Titre
        tk.Label(
            main_frame,
            text="Créer un compte",
            font=(self.FONT_FAMILY, 20, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['accent']
        ).pack(pady=(0, 30))
        
        # Formulaire
        form_frame = tk.Frame(main_frame, bg=self.theme['bg_primary'])
        form_frame.pack(fill='x')
        
        # Champs avec astérisques
        self.username_entry = self._create_field(form_frame, "Nom d'utilisateur *")
        self.email_entry = self._create_field(form_frame, "Email *")
        self.nom_entry = self._create_field(form_frame, "Nom *")
        self.prenom_entry = self._create_field(form_frame, "Prénom *")
        self.password_entry = self._create_field(form_frame, "Mot de passe *", show='•')
        self.confirm_password_entry = self._create_field(form_frame, "Confirmer le mot de passe *", show='•')
        
        # Message d'erreur
        self.error_label = tk.Label(
            form_frame,
            text="",
            font=(self.FONT_FAMILY, 9),
            bg=self.theme['bg_primary'],
            fg='#F44336',
            anchor='w',
            wraplength=370
        )
        self.error_label.pack(fill='x', pady=(10, 0))
        
        # Bouton inscription
        tk.Button(
            form_frame,
            text="S'inscrire",
            font=(self.FONT_FAMILY, 11, 'bold'),
            bg=self.theme['accent'],
            fg=self.theme['button_text'],
            activebackground=self.theme['accent'],
            relief='flat',
            cursor='hand2',
            command=self.signup
        ).pack(fill='x', pady=(20, 0), ipady=14)
        
        # Lien retour connexion
        back_frame = tk.Frame(form_frame, bg=self.theme['bg_primary'])
        back_frame.pack(pady=(15, 0))
        
        back_label = tk.Label(
            back_frame,
            text="Déjà un compte ? Se connecter",
            font=(self.FONT_FAMILY, 9),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_secondary'],
            cursor='hand2'
        )
        back_label.pack()
        back_label.bind('<Button-1>', lambda e: self.on_show_login())
    
    def _create_field(self, parent, label_text, show=None):
        """Crée un champ de formulaire"""
        # Frame pour le label avec astérisque
        label_frame = tk.Frame(parent, bg=self.theme['bg_primary'])
        label_frame.pack(fill='x', pady=(10, 5))
        
        # Séparer le texte et l'astérisque
        if label_text.endswith(' *'):
            text_without_star = label_text[:-2]
            has_star = True
        else:
            text_without_star = label_text
            has_star = False
        
        # Label principal
        tk.Label(
            label_frame,
            text=text_without_star,
            font=(self.FONT_FAMILY, 10),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary'],
            anchor='w'
        ).pack(side='left')
        
        # Astérisque en rouge
        if has_star:
            tk.Label(
                label_frame,
                text=" *",
                font=(self.FONT_FAMILY, 10, 'bold'),
                bg=self.theme['bg_primary'],
                fg='#F44336',
                anchor='w'
            ).pack(side='left')
        
        entry = tk.Entry(
            parent,
            font=(self.FONT_FAMILY, 11),
            bg=self.theme['input_bg'],
            fg=self.theme['text_primary'],
            show=show,
            relief='solid',
            borderwidth=1,
            insertbackground=self.theme['text_primary']
        )
        entry.pack(fill='x', ipady=8)
        return entry
    
    def signup(self):
        """Traite l'inscription"""
        account_controller = AccountController()
        result = account_controller.register(
            username=self.username_entry.get(),
            password=self.password_entry.get(),
            confirm_password=self.confirm_password_entry.get(),
            email=self.email_entry.get(),
            nom=self.nom_entry.get(),
            prenom=self.prenom_entry.get()
        )
        
        if result['success']:
            messagebox.showinfo("Succès", result['message'])
            # Se connecter automatiquement avec le compte créé
            login_result = account_controller.login(
                username=self.username_entry.get(),
                password=self.password_entry.get()
            )
            if login_result['success']:
                self.on_success(login_result['user_data'])
        else:
            self.error_label.config(text=result['message'])