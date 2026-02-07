import tkinter as tk
from src.controllers.account_controller import AccountController
from src.components.ui_component import FormField, Label, Button

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
        # Titre - TAILLE RÉDUITE
        title_label = tk.Label(
            self.parent_frame,
            text="Mon profil",
            font=(FONT_FAMILY, 18, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        )
        title_label.pack(anchor='w', pady=(0, 15))
        
        # Container pour les deux colonnes
        main_container = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        main_container.pack(fill='both', expand=True)
        
        # COLONNE GAUCHE: Informations personnelles
        self._create_personal_info_column(main_container)
        
        # COLONNE DROITE: Sécurité
        self._create_security_column(main_container)
    
    def _create_personal_info_column(self, parent):
        """Crée la colonne des informations personnelles"""
        left_column = tk.Frame(parent, bg=self.theme['bg_primary'])
        left_column.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        info_card = tk.Frame(
            left_column, 
            bg=self.theme['bg_secondary'], 
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.theme['border']
        )
        info_card.pack(fill='both', expand=True)
        
        # En-tête
        header = Label.subtitle(info_card, "📋  Informations personnelles", self.theme)
        header.pack(anchor='w', padx=20, pady=(15, 10))
        
        # Container des champs
        fields_container = tk.Frame(info_card, bg=self.theme['bg_secondary'])
        fields_container.pack(fill='x', padx=20, pady=(0, 10))
        
        # Créer les 4 champs AVEC ASTÉRISQUES
        self.profile_fields = {}
        
        fields_data = [
            ("Nom d'utilisateur *", self.user_data['username'], 'username'),
            ("Email *", self.user_data['email'], 'email'),
            ("Prénom *", self.user_data['prenom'], 'prenom'),
            ("Nom *", self.user_data['nom'], 'nom')
        ]
        
        for label_text, value, field_key in fields_data:
            field = FormField(fields_container, label_text, self.theme)
            field.pack(fill='x', pady=4)
            field.set(value)
            self.profile_fields[field_key] = field
        
        # Bouton - Utilisation du composant Button
        save_btn = Button.primary(
            info_card,
            "💾 Sauvegarder les modifications",
            self.save_profile,
            self.theme,
            font=(FONT_FAMILY, 11, 'bold')
        )
        save_btn.pack(side='bottom', anchor='e', padx=20, pady=20, ipadx=25, ipady=12)
        
        # Label de statut - PACK APRÈS
        self.profile_status_label = Label.status(info_card, self.theme, anchor='e')
        self.profile_status_label.pack(side='bottom', fill='x', padx=20, pady=(10, 0))
    
    def _create_security_column(self, parent):
        """Crée la colonne de sécurité"""
        right_column = tk.Frame(parent, bg=self.theme['bg_primary'])
        right_column.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        password_card = tk.Frame(
            right_column, 
            bg=self.theme['bg_secondary'], 
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.theme['border']
        )
        password_card.pack(fill='both', expand=True)
        
        # En-tête
        header = Label.subtitle(password_card, "🔒  Sécurité", self.theme)
        header.pack(anchor='w', padx=20, pady=(15, 10))
        
        # Container des champs
        password_fields_container = tk.Frame(password_card, bg=self.theme['bg_secondary'])
        password_fields_container.pack(fill='x', padx=20, pady=(0, 10))
        
        # Créer les 3 champs de mot de passe AVEC ASTÉRISQUES
        self.password_fields = {}
        
        password_fields_data = [
            ("Ancien mot de passe *", "old_password"),
            ("Nouveau mot de passe *", "new_password"),
            ("Confirmer le nouveau mot de passe *", "confirm_password")
        ]
        
        for label_text, field_key in password_fields_data:
            field = FormField(password_fields_container, label_text, self.theme, input_type="password")
            field.pack(fill='x', pady=4)
            self.password_fields[field_key] = field
        
        # Spacer pour compenser le 4e champ manquant - HAUTEUR 75px
        spacer_frame = tk.Frame(password_fields_container, bg=self.theme['bg_secondary'], height=75)
        spacer_frame.pack(fill='x', pady=4)
        spacer_frame.pack_propagate(False)
        
        # Bouton - Utilisation du composant Button
        change_pwd_btn = Button.primary(
            password_card,
            "🔐 Changer le mot de passe",
            self.change_password,
            self.theme,
            font=(FONT_FAMILY, 11, 'bold')
        )
        change_pwd_btn.pack(side='bottom', anchor='e', padx=20, pady=20, ipadx=25, ipady=12)
        
        # Label de statut - PACK APRÈS
        self.password_status_label = Label.status(password_card, self.theme, anchor='e')
        self.password_status_label.pack(side='bottom', fill='x', padx=20, pady=(10, 0))
    
    def save_profile(self):
        """Sauvegarde les modifications du profil"""
        new_username = self.profile_fields['username'].get().strip()
        new_email = self.profile_fields['email'].get().strip()
        new_prenom = self.profile_fields['prenom'].get().strip()
        new_nom = self.profile_fields['nom'].get().strip()
        
        # Validation : tous les champs obligatoires
        if not new_username or not new_email or not new_prenom or not new_nom:
            self.profile_status_label.config(
                text="✗ Tous les champs sont obligatoires",
                fg='#F44336'
            )
            return
        
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
                self.profile_status_label.config(text=f"✓ {result['message']}", fg='#4CAF50')
            else:
                color = '#F44336' if 'modification' not in result['message'] else '#FF9800'
                self.profile_status_label.config(text=f"✗ {result['message']}", fg=color)
                
        except Exception as e:
            self.profile_status_label.config(text=f"✗ Erreur: {str(e)}", fg='#F44336')
    
    def change_password(self):
        """Change le mot de passe"""
        old_password = self.password_fields['old_password'].get()
        new_password = self.password_fields['new_password'].get()
        confirm_password = self.password_fields['confirm_password'].get()
        
        try:
            account_controller = AccountController()
            result = account_controller.change_password(
                account_id=self.user_data['id'],
                current_password=old_password,
                new_password=new_password,
                confirm_password=confirm_password
            )
            
            if result['success']:
                # Vider les champs
                for field in self.password_fields.values():
                    field.clear()
                
                self.password_status_label.config(text=f"✓ {result['message']}", fg='#4CAF50')
            else:
                self.password_status_label.config(text=f"✗ {result['message']}", fg='#F44336')
                
        except Exception as e:
            self.password_status_label.config(text=f"✗ Erreur: {str(e)}", fg='#F44336')