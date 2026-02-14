import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.exchange_controller import ExchangeController
from src.components.ui_component import Label, FormField, Button, Input, Toast
import threading

FONT_FAMILY = "Segoe UI"

class PlatformsView:
    """Vue pour gérer les plateformes (exchanges) et les API-keys utilisateur"""

    def __init__(self, parent_frame, theme, user_data):
        self.parent_frame = parent_frame
        self.theme = theme
        self.user_data = user_data
        self.controller = ExchangeController()
        self.all_api_keys = []
        self.all_exchanges = []
        self.search_timer = None
        self.current_view = 'list'  # 'list' ou 'form'

        self.container = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        self.container.pack(fill='both', expand=True)

        self._build_ui()
        self._load_exchanges()
        self._load_api_keys()
        # Attendre que le canvas soit prêt avant d'afficher les cartes
        self.container.update_idletasks()
        self._display_cards()

    def _build_ui(self):
        """Construit l'interface utilisateur"""
        # Header
        header = Label.title(self.container, "Mes Plateformes", self.theme)
        header.pack(fill='x', pady=(0, 20))

        # Barre de recherche et bouton d'ajout - tout sur une ligne
        search_frame = tk.Frame(self.container, bg=self.theme['bg_primary'])
        search_frame.pack(fill='x', pady=(0, 20))

        # Label
        tk.Label(
            search_frame,
            text="🔍 Rechercher une plateforme",
            font=(FONT_FAMILY, 10),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(side='left', padx=(0, 10))

        # Champ de recherche (réduit)
        self.search_entry = tk.Entry(
            search_frame,
            font=(FONT_FAMILY, 10),
            bg=self.theme['input_bg'],
            fg=self.theme['text_primary'],
            relief='solid',
            borderwidth=1,
            insertbackground=self.theme['text_primary'],
            width=25
        )
        self.search_entry.pack(side='left', ipady=6, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self._on_search_change)

        # Bouton d'ajout
        add_btn = tk.Button(
            search_frame,
            text="➕ Ajouter",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['accent'],
            fg='#FFFFFF',
            activebackground=self.theme['accent'],
            relief='flat',
            cursor='hand2',
            command=self._show_add_form
        )
        add_btn.pack(side='right', ipady=6, ipadx=15)

        # Conteneur pour les cartes
        cards_container = tk.Frame(self.container, bg=self.theme['bg_primary'])
        cards_container.pack(fill='both', expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(cards_container)
        scrollbar.pack(side='right', fill='y')

        self.cards_canvas = tk.Canvas(
            cards_container,
            bg=self.theme['bg_primary'],
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.cards_canvas.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.cards_canvas.yview)

        self.cards_frame = tk.Frame(self.cards_canvas, bg=self.theme['bg_primary'])
        self.cards_window = self.cards_canvas.create_window(
            0, 0, window=self.cards_frame, anchor='nw'
        )

        # Bind le redimensionnement
        self.cards_frame.bind("<Configure>", self._on_frame_configure)
        self.cards_canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _on_frame_configure(self, event=None):
        """Configure la scroll region du canvas"""
        self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))
        # Adapter la largeur du canvas
        canvas_width = self.cards_canvas.winfo_width()
        if canvas_width > 1:
            self.cards_canvas.itemconfig(self.cards_window, width=canvas_width)

    def _on_mousewheel(self, event):
        """Gère la molette souris"""
        self.cards_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_search_change(self, event=None):
        """Déclenche la recherche lors du changement"""
        search_text = self.search_entry.get().strip()

        # Annuler le timer précédent
        if self.search_timer:
            self.parent_frame.after_cancel(self.search_timer)

        # Déclencher la recherche après 300ms
        self.search_timer = self.parent_frame.after(300, self._filter_and_display, search_text)

    def _load_api_keys(self):
        """Charge les clés API de l'utilisateur"""
        self.all_api_keys = self.controller.get_api_keys_for_user(self.user_data['id'])

    def _load_exchanges(self):
        """Charge les exchanges disponibles"""
        self.all_exchanges = self.controller.list_exchanges()

    def _filter_and_display(self, search_text=""):
        """Filtre et affiche les cartes"""
        self._display_cards(search_text)

    def _display_cards(self, search_text=""):
        """Affiche les cartes des plateformes"""
        # Vider le frame
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        # Filtrer les exchanges selon la recherche
        filtered_exchanges = self.all_exchanges
        if search_text:
            filtered_exchanges = [
                ex for ex in self.all_exchanges
                if search_text.lower() in ex.get('display_name', '').lower()
            ]

        if not filtered_exchanges:
            empty_label = tk.Label(
                self.cards_frame,
                text="Aucune plateforme trouvée",
                font=(FONT_FAMILY, 11),
                bg=self.theme['bg_primary'],
                fg=self.theme['text_secondary']
            )
            empty_label.pack(pady=40)
            return

        # Afficher les cartes en grille pour chaque plateforme
        for idx, exchange in enumerate(filtered_exchanges):
            row = idx // 2
            col = idx % 2

            # Vérifier si l'utilisateur a une clé pour cette plateforme
            user_key = None
            for key in self.all_api_keys:
                if key['exchange_id'] == exchange['exchange_id']:
                    user_key = key
                    break
            
            # Debug: afficher les IDs qui ne matchent pas
            if not user_key and len(self.all_api_keys) > 0:
                print(f"Exchange {exchange.get('display_name')} (ID: {exchange['exchange_id']}) - Pas de clé trouvée")
                print(f"  Clés disponibles: {[(k.get('exchange_display'), k['exchange_id']) for k in self.all_api_keys]}")

            card_frame = self._create_exchange_card(exchange, user_key)
            card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

        # Configurer les poids des colonnes et lignes
        self.cards_frame.grid_columnconfigure(0, weight=1)
        self.cards_frame.grid_columnconfigure(1, weight=1)
        # Configurer tous les poids des lignes dynamiquement
        for i in range((len(filtered_exchanges) + 1) // 2):
            self.cards_frame.grid_rowconfigure(i, weight=1)

    def _create_exchange_card(self, exchange, user_key):
        """Crée une carte pour une plateforme"""
        card = tk.Frame(
            self.cards_frame,
            bg=self.theme['bg_secondary'],
            relief='solid',
            borderwidth=1
        )
        card.config(highlightbackground=self.theme['border'], highlightthickness=1)

        # En-tête de la carte
        header = tk.Frame(card, bg=self.theme['accent'], height=50)
        header.pack(fill='x', padx=1, pady=1)
        header.pack_propagate(False)

        exchange_name = exchange.get('display_name', 'Plateforme inconnue')
        tk.Label(
            header,
            text=exchange_name,
            font=(FONT_FAMILY, 12, 'bold'),
            bg=self.theme['accent'],
            fg='#FFFFFF'
        ).pack(side='left', padx=15, pady=10)

        # Corps de la carte
        body = tk.Frame(card, bg=self.theme['bg_secondary'])
        body.pack(fill='both', expand=True, padx=15, pady=15)

        if user_key:
            # Afficher la clé existante
            # Nom de la clé (label)
            label_text = user_key.get('label', '')
            if label_text:
                tk.Label(
                    body,
                    text=label_text,
                    font=(FONT_FAMILY, 9),
                    bg=self.theme['bg_secondary'],
                    fg=self.theme['text_secondary'],
                    wraplength=250
                ).pack(anchor='w', pady=(0, 10))

            # Clé API
            tk.Label(
                body,
                text="Clé API",
                font=(FONT_FAMILY, 9, 'bold'),
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_secondary']
            ).pack(anchor='w', pady=(0, 4))

            api_key = user_key.get('api_key', '')
            masked_key = self._mask_api_key(api_key)
            tk.Label(
                body,
                text=masked_key,
                font=(FONT_FAMILY, 10),
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_primary'],
                wraplength=250
            ).pack(anchor='w', pady=(0, 15))

            # Status badge
            status_frame = tk.Frame(body, bg=self.theme['bg_secondary'])
            status_frame.pack(fill='x', pady=(0, 15))

            tk.Label(
                status_frame,
                text="✓ Connectée",
                font=(FONT_FAMILY, 9, 'bold'),
                bg=self.theme['bg_secondary'],
                fg='#4CAF50'
            ).pack(anchor='w')

        else:
            # Plateforme non configurée
            tk.Label(
                body,
                text="Non configurée",
                font=(FONT_FAMILY, 9),
                bg=self.theme['bg_secondary'],
                fg=self.theme['text_secondary'],
                wraplength=250
            ).pack(anchor='w', pady=(0, 15))

        # Boutons
        buttons_frame = tk.Frame(body, bg=self.theme['bg_secondary'])
        buttons_frame.pack(fill='x')

        if user_key:
            # Bouton Modifier
            modify_btn = tk.Button(
                buttons_frame,
                text="✏️  Modifier",
                font=(FONT_FAMILY, 9),
                bg=self.theme['accent'],
                fg='#FFFFFF',
                activebackground=self.theme['accent'],
                relief='flat',
                cursor='hand2',
                command=lambda k=user_key: self._modify_api_key(k)
            )
            modify_btn.pack(side='left', fill='x', expand=True, padx=(0, 5))

            # Bouton Supprimer
            delete_btn = tk.Button(
                buttons_frame,
                text="🗑️  Supprimer",
                font=(FONT_FAMILY, 9),
                bg='#F44336',
                fg='#FFFFFF',
                activebackground='#F44336',
                relief='flat',
                cursor='hand2',
                command=lambda k=user_key: self._delete_api_key(k)
            )
            delete_btn.pack(side='right', fill='x', expand=True, padx=(5, 0))
        else:
            # Bouton Ajouter
            add_btn = tk.Button(
                buttons_frame,
                text="➕ Ajouter une clé",
                font=(FONT_FAMILY, 9, 'bold'),
                bg=self.theme['accent'],
                fg='#FFFFFF',
                activebackground=self.theme['accent'],
                relief='flat',
                cursor='hand2',
                command=lambda ex=exchange: self._add_key_for_exchange(ex)
            )
            add_btn.pack(side='left', fill='x', expand=True)

        return card

    def _mask_api_key(self, api_key):
        """Masque la clé API en affichant seulement le début et la fin"""
        if not api_key or len(api_key) <= 8:
            return "••••••••"
        return api_key[:4] + "••••" + api_key[-4:]

    def _modify_api_key(self, key):
        """Affiche la vue de modification de clé API"""
        self.current_view = 'form'
        # Nettoyer le canvas
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Afficher la vue de formulaire
        from src.views.apikey_form_view import ApiKeyFormView
        ApiKeyFormView(
            parent_frame=self.container,
            theme=self.theme,
            user_data=self.user_data,
            on_back_callback=self._show_list_view,
            on_success_callback=self._show_list_view,
            api_key=key
        )

    def _show_add_form(self):
        """Affiche la vue d'ajout de clé API"""
        self.current_view = 'form'
        # Nettoyer le canvas
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Afficher la vue de formulaire
        from src.views.apikey_form_view import ApiKeyFormView
        ApiKeyFormView(
            parent_frame=self.container,
            theme=self.theme,
            user_data=self.user_data,
            on_back_callback=self._show_list_view,
            on_success_callback=self._show_list_view,
            api_key=None
        )

    def _show_list_view(self):
        """Revient à la vue de liste"""
        self.current_view = 'list'
        # Nettoyer le container
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Reconstruire l'interface
        self._build_ui()
        self._load_exchanges()
        self._load_api_keys()
        self._display_cards()

    def _add_key_for_exchange(self, exchange):
        """Affiche le formulaire pour ajouter une clé pour une plateforme spécifique"""
        self.current_view = 'form'
        # Nettoyer le canvas
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Afficher la vue de formulaire avec la plateforme pré-sélectionnée
        from src.views.apikey_form_view import ApiKeyFormView
        
        # Créer un pseudo objet avec la plateforme pré-sélectionnée
        class SelectedExchange:
            def __init__(self, exchange):
                self.exchange_id = exchange['exchange_id']
                self.display_name = exchange.get('display_name', exchange.get('name'))
        
        # On va passer None comme api_key, mais modifier le formulaire pour accepter une plateforme pré-sélectionnée
        # On va simplement afficher le formulaire normal et laisser l'utilisateur choisir
        ApiKeyFormView(
            parent_frame=self.container,
            theme=self.theme,
            user_data=self.user_data,
            on_back_callback=self._show_list_view,
            on_success_callback=self._show_list_view,
            api_key=None
        )

    def _delete_api_key(self, key):
        """Supprime une clé API"""
        exchange_name = key.get('exchange_display', 'cette plateforme')
        if not messagebox.askyesno(
            "Confirmer la suppression",
            f"Êtes-vous sûr de vouloir supprimer la clé API de {exchange_name} ?"
        ):
            return

        success, msg = self.controller.delete_api_key(key['api_key_id'])

        if success:
            Toast.show(self.container, "Clé API supprimée ✓", 'success')
            self.all_api_keys = self.controller.get_api_keys_for_user(self.user_data['id'])
            self.parent_frame.after(1500, self._display_cards)
        else:
            Toast.show(self.container, f"Erreur: {msg}", 'error')
