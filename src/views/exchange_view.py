import tkinter as tk
from tkinter import messagebox
from src.controllers.exchange_controller import ExchangeController
from src.components.ui_component import Label, FormField, Button, Card, Toast

FONT_FAMILY = "Segoe UI"

class ExchangeView:
    """Vue pour gérer les plateformes d'échange (exchanges uniquement)"""
    
    def __init__(self, parent_frame, theme, user_data):
        self.parent_frame = parent_frame
        self.theme = theme
        self.user_data = user_data
        self.controller = ExchangeController(account_id=user_data['id'])
        self.current_view = 'list'  # 'list' ou 'form'
        self.editing_exchange = None
        
        self.container = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        self.container.pack(fill='both', expand=True)
        
        self.show_list_view()
    
    def show_list_view(self):
        """Affiche la liste des exchanges"""
        self.current_view = 'list'
        self.editing_exchange = None
        
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Header avec titre et bouton ajouter
        header_frame = tk.Frame(self.container, bg=self.theme['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        # Titre
        tk.Label(
            header_frame,
            text="Mes plateformes",
            font=(FONT_FAMILY, 20, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(side='left')

        # Bouton ajouter (style identique aux bots)
        tk.Button(
            header_frame,
            text="➕ Ajouter une plateforme",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['accent'],
            fg=self.theme['button_text'],
            activebackground=self.theme['accent'],
            relief='flat',
            cursor='hand2',
            command=self.show_add_form
        ).pack(side='right', ipadx=20, ipady=10)
        
        # Liste des exchanges
        self._display_exchanges_list()
    
    def _display_exchanges_list(self):
        """Affiche la liste des exchanges sous forme de cartes"""
        list_container = tk.Frame(self.container, bg=self.theme['bg_primary'])
        list_container.pack(fill='both', expand=True)

        exchanges = self.controller.list_exchanges()

        if not exchanges:
            tk.Label(
                list_container,
                text="Aucune plateforme configurée.\nCliquez sur 'Ajouter une plateforme' pour commencer.",
                font=(FONT_FAMILY, 11),
                bg=self.theme['bg_primary'],
                fg=self.theme['text_secondary'],
                justify='center'
            ).pack(expand=True)
            return

        # Canvas avec scrollbar conditionnelle
        canvas = tk.Canvas(list_container, bg=self.theme['bg_primary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_container, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.theme['bg_primary'])
        win_id = canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')

        def _on_frame_configure(_e):
            canvas.configure(scrollregion=canvas.bbox('all'))
            w = canvas.winfo_width()
            if w > 1:
                canvas.itemconfigure(win_id, width=w)

        def _on_yscroll(first, last):
            if float(first) <= 0.0 and float(last) >= 1.0:
                scrollbar.pack_forget()
            else:
                scrollbar.pack(side='right', fill='y', before=canvas)
            scrollbar.set(first, last)

        scrollable_frame.bind('<Configure>', _on_frame_configure)
        canvas.configure(yscrollcommand=_on_yscroll)

        for idx, exchange in enumerate(exchanges):
            row = idx // 3
            col = idx % 3
            card = self._create_exchange_card(scrollable_frame, exchange)
            card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        for i in range(3):
            scrollable_frame.grid_columnconfigure(i, weight=1)

        canvas.pack(side='left', fill='both', expand=True)
        canvas.bind('<MouseWheel>', lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), 'units'))
    
    def _create_exchange_card(self, parent, exchange):
        """Crée une carte pour un exchange (affichage simple)"""
        card = Card(parent, self.theme)

        # Padding interne
        inner_frame = tk.Frame(card.frame, bg=self.theme['bg_secondary'])
        inner_frame.pack(fill='both', expand=True, padx=25, pady=25)
        
        # Logo centré
        logo = exchange.get('logo', '💱')
        logo_label = tk.Label(
            inner_frame,
            text=logo,
            font=(FONT_FAMILY, 48),
            bg=self.theme['bg_secondary']
        )
        logo_label.pack(pady=(0, 15))
        
        # Nom de l'exchange centré
        name_label = tk.Label(
            inner_frame,
            text=exchange.get('display_name', exchange.get('name', 'Sans nom')),
            font=(FONT_FAMILY, 14, 'bold'),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary']
        )
        name_label.pack(pady=(0, 5))
        
        # ID technique (plus petit)
        tk.Label(
            inner_frame,
            text=exchange.get('name', ''),
            font=(FONT_FAMILY, 8),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_secondary']
        ).pack(pady=(0, 15))
        
        # Séparateur
        separator = tk.Frame(inner_frame, bg=self.theme['border'], height=1)
        separator.pack(fill='x', pady=(0, 15))
        
        # URL endpoint (si disponible)
        endpoint = exchange.get('endpoint_url', '')
        if endpoint:
            # Frame pour l'icône et l'URL
            endpoint_frame = tk.Frame(inner_frame, bg=self.theme['bg_secondary'])
            endpoint_frame.pack(fill='x', pady=(0, 15))
            
            tk.Label(
                endpoint_frame,
                text="🌐",
                font=(FONT_FAMILY, 12),
                bg=self.theme['bg_secondary']
            ).pack(side='left', padx=(0, 5))
            
            tk.Label(
                endpoint_frame,
                text=endpoint,
                font=(FONT_FAMILY, 8),
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_secondary'],
                anchor='w',
                wraplength=200
            ).pack(side='left', fill='x', expand=True)
        
        # Boutons d'action
        buttons_frame = tk.Frame(inner_frame, bg=self.theme['bg_secondary'])
        buttons_frame.pack(fill='x', side='bottom')
        
        # Bouton Modifier
        edit_btn = tk.Button(
            buttons_frame,
            text="✏️",
            font=(FONT_FAMILY, 14),
            bg=self.theme['bg_secondary'],
            fg=self.theme['accent'],
            activebackground=self.theme['bg_primary'],
            relief='flat',
            cursor='hand2',
            command=lambda: self.show_edit_form(exchange),
            width=3
        )
        edit_btn.pack(side='left', expand=True, fill='x')
        
        # Bouton Supprimer
        delete_btn = tk.Button(
            buttons_frame,
            text="🗑️",
            font=(FONT_FAMILY, 14),
            bg=self.theme['bg_secondary'],
            fg='#F44336',
            activebackground=self.theme['bg_primary'],
            relief='flat',
            cursor='hand2',
            command=lambda: self._delete_exchange(exchange),
            width=3
        )
        delete_btn.pack(side='right', expand=True, fill='x')
        
        return card
    
    def show_add_form(self):
        """Affiche le formulaire d'ajout d'exchange"""
        self.current_view = 'form'
        self.editing_exchange = None
        self._show_form()
    
    def show_edit_form(self, exchange):
        """Affiche le formulaire de modification d'exchange"""
        self.current_view = 'form'
        self.editing_exchange = exchange
        self._show_form()
    
    def _show_form(self):
        """Affiche le formulaire (ajout ou modification)"""
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Header avec bouton retour
        header_frame = tk.Frame(self.container, bg=self.theme['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 15))
        
        # Bouton retour
        back_btn = tk.Button(
            header_frame,
            text="←",
            font=(FONT_FAMILY, 18, 'bold'),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary'],
            relief='flat',
            cursor='hand2',
            command=self.show_list_view
        )
        back_btn.pack(side='left', padx=(0, 20), ipadx=10, ipady=8)
        
        # Titre
        title_text = "Modifier la plateforme" if self.editing_exchange else "Nouvelle plateforme"
        tk.Label(
            header_frame,
            text=title_text,
            font=(FONT_FAMILY, 22, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(side='left')
        
        # Formulaire
        form_card = tk.Frame(
            self.container,
            bg=self.theme['bg_secondary'],
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.theme['border']
        )
        form_card.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Container avec padding
        form_container = tk.Frame(form_card, bg=self.theme['bg_secondary'])
        form_container.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Champs du formulaire
        self.form_fields = {}
        
        # Nom de la plateforme
        field_name = FormField(
            form_container,
            "Nom de la plateforme *",
            self.theme,
            icon="🏷️",
            help_text="Nom affiché de la plateforme (ex: Coinbase, Binance)"
        )
        field_name.pack(fill='x', pady=(0, 20))
        self.form_fields['display_name'] = field_name
        
        # Logo (emoji ou URL)
        field_logo = FormField(
            form_container,
            "Logo",
            self.theme,
            icon="🎨",
            help_text="Emoji ou URL de l'image (ex: 🟦, https://...) — optionnel"
        )
        field_logo.pack(fill='x', pady=(0, 20))
        self.form_fields['logo'] = field_logo
        
        # URL endpoint
        field_endpoint = FormField(
            form_container,
            "URL endpoint *",
            self.theme,
            icon="🌐",
            help_text="URL de l'API de la plateforme (ex: https://api.exchange.com)"
        )
        field_endpoint.pack(fill='x', pady=(0, 30))
        self.form_fields['endpoint_url'] = field_endpoint
        
        # Si modification, pré-remplir les champs
        if self.editing_exchange:
            field_name.set(self.editing_exchange.get('display_name', ''))
            field_logo.set(self.editing_exchange.get('logo', ''))
            field_endpoint.set(self.editing_exchange.get('endpoint_url', ''))
        
        # Label de statut
        self.form_status_label = Label.status(form_container, self.theme)
        self.form_status_label.pack(fill='x', pady=(0, 10))
        
        # Boutons
        buttons_frame = tk.Frame(form_container, bg=self.theme['bg_secondary'])
        buttons_frame.pack(fill='x')
        
        # Bouton Enregistrer
        save_btn = Button.primary(
            buttons_frame,
            "💾 Enregistrer",
            self._save_exchange,
            self.theme,
            font=(FONT_FAMILY, 11, 'bold')
        )
        save_btn.pack(side='right', ipadx=25, ipady=12)
        
        # Bouton Annuler
        cancel_btn = Button.secondary(
            buttons_frame,
            "Annuler",
            self.show_list_view,
            self.theme,
            font=(FONT_FAMILY, 11, 'bold')
        )
        cancel_btn.pack(side='right', padx=(0, 10), ipadx=25, ipady=12)
    
    def _save_exchange(self):
        """Enregistre l'exchange (création ou modification)"""
        # Récupérer les valeurs
        display_name = self.form_fields['display_name'].get().strip()
        logo = self.form_fields['logo'].get().strip()
        endpoint_url = self.form_fields['endpoint_url'].get().strip()
        
        # Logo par défaut si vide
        if not logo:
            logo = '💱'

        # Validation
        if not display_name or not endpoint_url:
            self.form_status_label.config(
                text="✗ Veuillez remplir tous les champs obligatoires",
                fg='#F44336'
            )
            return
        
        if self.editing_exchange:
            # Modification
            success, message = self.controller.update_exchange(
                self.editing_exchange['exchange_id'],
                display_name=display_name,
                logo=logo,
                endpoint_url=endpoint_url
            )
            
            if success:
                Toast.show(self.container, "Plateforme modifiée ✓", 'success')
                self.container.after(1500, self.show_list_view)
            else:
                self.form_status_label.config(
                    text=f"✗ {message}",
                    fg='#F44336'
                )
        else:
            # Création
            # Générer un identifiant technique (name) à partir du display_name
            name = display_name.lower().replace(' ', '_').replace('-', '_')
            name = ''.join(c for c in name if c.isalnum() or c == '_')
            
            success, message = self.controller.add_exchange(
                name, display_name, logo, endpoint_url
            )
            
            if success:
                Toast.show(self.container, "Plateforme ajoutée ✓", 'success')
                self.container.after(1500, self.show_list_view)
            else:
                self.form_status_label.config(
                    text=f"✗ {message}",
                    fg='#F44336'
                )
    
    def _delete_exchange(self, exchange):
        """Supprime un exchange"""
        # Confirmation
        confirm = messagebox.askyesno(
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer la plateforme '{exchange.get('display_name', 'cette plateforme')}' ?\n\n"
            "⚠️ Cette action est irréversible."
        )
        
        if not confirm:
            return
        
        # Supprimer
        success, message = self.controller.delete_exchange(exchange['exchange_id'])
        
        if success:
            Toast.show(self.container, "Plateforme supprimée ✓", 'success')
            self.container.after(1500, self.show_list_view)
        else:
            messagebox.showerror("Erreur", message)