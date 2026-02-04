import tkinter as tk
from src.controllers.account_controller import AccountController

FONT_FAMILY = "Segoe UI"

class ProfileView:
    """Vue du profil utilisateur"""
    
    def __init__(self, parent_frame, theme, user_data, on_update_callback):
        self.parent_frame = parent_frame
        self.theme = theme
        self.user_data = user_data
        self.on_update_callback = on_update_callback
        
        self.render()
    
    def render(self):
        """Affiche le profil utilisateur"""
        # Titre
        tk.Label(
            self.parent_frame,
            text="Mon profil",
            font=(FONT_FAMILY, 24, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 30))
        
        # Container pour les deux colonnes
        main_container = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        main_container.pack(fill='both', expand=True)
        
        # COLONNE GAUCHE: Informations personnelles
        left_column = tk.Frame(main_container, bg=self.theme['bg_primary'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        info_card = tk.Frame(left_column, bg=self.theme['bg_secondary'], relief='flat')
        info_card.pack(fill='both', expand=True)
        
        tk.Label(
            info_card,
            text="📋  Informations personnelles",
            font=(FONT_FAMILY, 14, 'bold'),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary'],
            anchor='w'
        ).pack(anchor='w', padx=20, pady=(20, 15))
        
        fields_container = tk.Frame(info_card, bg=self.theme['bg_secondary'])
        fields_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.profile_entries = {}
        
        fields = [
            ("Nom d'utilisateur", self.user_data['username'], 'username'),
            ("Email", self.user_data['email'], 'email'),
            ("Prénom", self.user_data['prenom'], 'prenom'),
            ("Nom", self.user_data['nom'], 'nom')
        ]
        
        for label_text, value, field_key in fields:
            field_frame = tk.Frame(fields_container, bg=self.theme['bg_secondary'])
            field_frame.pack(fill='x', pady=8)
            
            tk.Label(
                field_frame,
                text=label_text,
                font=(FONT_FAMILY, 10),
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_secondary'],
                anchor='w'
            ).pack(anchor='w', pady=(0, 5))
            
            entry = tk.Entry(
                field_frame,
                font=(FONT_FAMILY, 11),
                bg=self.theme['input_bg'],
                fg=self.theme['text_primary'],
                relief='solid',
                borderwidth=1,
                insertbackground=self.theme['text_primary']
            )
            entry.insert(0, value)
            entry.pack(fill='x', ipady=8)
            
            self.profile_entries[field_key] = entry
        
        self.profile_status_label = tk.Label(
            info_card,
            text="",
            font=(FONT_FAMILY, 9),
            bg=self.theme['bg_secondary'],
            fg='#4CAF50',
            anchor='e'
        )
        self.profile_status_label.pack(fill='x', padx=20, pady=(10, 5))
        
        button_frame = tk.Frame(info_card, bg=self.theme['bg_secondary'])
        button_frame.pack(fill='x', padx=20, pady=(5, 20))
        
        tk.Button(
            button_frame,
            text="💾 Sauvegarder les modifications",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['accent'],
            fg=self.theme['button_text'],
            activebackground=self.theme['accent'],
            relief='flat',
            cursor='hand2',
            command=self.save_profile
        ).pack(side='right', ipadx=25, ipady=12)
        
        # COLONNE DROITE: Sécurité
        right_column = tk.Frame(main_container, bg=self.theme['bg_primary'])
        right_column.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        password_card = tk.Frame(right_column, bg=self.theme['bg_secondary'], relief='flat')
        password_card.pack(fill='both', expand=True)
        
        tk.Label(
            password_card,
            text="🔒  Sécurité",
            font=(FONT_FAMILY, 14, 'bold'),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary'],
            anchor='w'
        ).pack(anchor='w', padx=20, pady=(20, 15))
        
        password_fields_container = tk.Frame(password_card, bg=self.theme['bg_secondary'])
        password_fields_container.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        self.password_entries = {}
        
        password_fields = [
            ("Ancien mot de passe", "old_password"),
            ("Nouveau mot de passe", "new_password"),
            ("Confirmer le nouveau mot de passe", "confirm_password")
        ]
        
        for label_text, field_key in password_fields:
            field_frame = tk.Frame(password_fields_container, bg=self.theme['bg_secondary'])
            field_frame.pack(fill='x', pady=8)
            
            tk.Label(
                field_frame,
                text=label_text,
                font=(FONT_FAMILY, 10),
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_secondary'],
                anchor='w'
            ).pack(anchor='w', pady=(0, 5))
            
            entry = tk.Entry(
                field_frame,
                font=(FONT_FAMILY, 11),
                bg=self.theme['input_bg'],
                fg=self.theme['text_primary'],
                show='•',
                relief='solid',
                borderwidth=1,
                insertbackground=self.theme['text_primary']
            )
            entry.pack(fill='x', ipady=8)
            
            self.password_entries[field_key] = entry
        
        # Spacer pour équilibrer les deux colonnes
        spacer_frame = tk.Frame(password_fields_container, bg=self.theme['bg_secondary'], height=70)
        spacer_frame.pack(fill='x', pady=8)
        spacer_frame.pack_propagate(False)
        
        self.password_status_label = tk.Label(
            password_card,
            text="",
            font=(FONT_FAMILY, 9),
            bg=self.theme['bg_secondary'],
            fg='#4CAF50',
            anchor='e'
        )
        self.password_status_label.pack(fill='x', padx=20, pady=(10, 5))
        
        password_button_frame = tk.Frame(password_card, bg=self.theme['bg_secondary'])
        password_button_frame.pack(fill='x', padx=20, pady=(5, 20))
        
        tk.Button(
            password_button_frame,
            text="🔐 Changer le mot de passe",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['accent'],
            fg=self.theme['button_text'],
            activebackground=self.theme['accent'],
            relief='flat',
            cursor='hand2',
            command=self.change_password
        ).pack(side='right', ipadx=25, ipady=12)
    
    def save_profile(self):
        """Sauvegarde les modifications du profil"""
        new_username = self.profile_entries['username'].get()
        new_email = self.profile_entries['email'].get()
        new_prenom = self.profile_entries['prenom'].get()
        new_nom = self.profile_entries['nom'].get()
        
        try:
            account_controller = AccountController()
            result = account_controller.update_profile(
                account_id=self.user_data['id'],
                username=new_username,
                email=new_email,
                prenom=new_prenom,
                nom=new_nom,
                current_username=self.user_data['username'],
                current_email=self.user_data['email'],
                current_prenom=self.user_data['prenom'],
                current_nom=self.user_data['nom']
            )
            
            if result['success']:
                self.on_update_callback(result['updated_data'])
                self.profile_status_label.config(text=result['message'], fg='#4CAF50')
            else:
                color = '#F44336' if 'modification' not in result['message'] else '#FF9800'
                self.profile_status_label.config(text=f"✗ {result['message']}", fg=color)
                
        except Exception as e:
            self.profile_status_label.config(text=f"✗ Erreur: {str(e)}", fg='#F44336')
    
    def change_password(self):
        """Change le mot de passe"""
        old_password = self.password_entries['old_password'].get()
        new_password = self.password_entries['new_password'].get()
        confirm_password = self.password_entries['confirm_password'].get()
        
        try:
            account_controller = AccountController()
            result = account_controller.change_password(
                account_id=self.user_data['id'],
                old_password=old_password,
                new_password=new_password,
                confirm_password=confirm_password
            )
            
            if result['success']:
                self.password_entries['old_password'].delete(0, tk.END)
                self.password_entries['new_password'].delete(0, tk.END)
                self.password_entries['confirm_password'].delete(0, tk.END)
                self.password_status_label.config(text=result['message'], fg='#4CAF50')
            else:
                self.password_status_label.config(text=f"✗ {result['message']}", fg='#F44336')
                
        except Exception as e:
            self.password_status_label.config(text=f"✗ Erreur: {str(e)}", fg='#F44336')