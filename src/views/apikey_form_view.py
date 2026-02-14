import tkinter as tk
from tkinter import messagebox
from src.controllers.exchange_controller import ExchangeController
from src.components.ui_component import Label, Toast, Button

FONT_FAMILY = "Segoe UI"


class ApiKeyFormView:
    """Vue du formulaire d'ajout/modification de clé API"""

    def __init__(self, parent_frame, theme, user_data, on_back_callback, on_success_callback, api_key=None):
        self.parent_frame = parent_frame
        self.theme = theme
        self.user_data = user_data
        self.on_back_callback = on_back_callback
        self.on_success_callback = on_success_callback
        self.controller = ExchangeController()
        self.api_key = api_key  # None si création, dict si modification
        self.exchanges = []

        self.container = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        self.container.pack(fill='both', expand=True)

        self._build_ui()
        self._load_exchanges()

    def _build_ui(self):
        """Construit l'interface du formulaire"""
        # En-tête
        header_frame = tk.Frame(self.container, bg=self.theme['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))

        # Titre
        title = "Modifier une clé API" if self.api_key else "Ajouter une clé API"
        tk.Label(
            header_frame,
            text=title,
            font=(FONT_FAMILY, 18, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w')

        # Frame principal du formulaire
        form_frame = tk.Frame(self.container, bg=self.theme['bg_secondary'], relief='solid', borderwidth=1)
        form_frame.pack(fill='x', pady=(0, 20))

        # Conteneur avec scroll
        inner_frame = tk.Frame(form_frame, bg=self.theme['bg_secondary'])
        inner_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Sélection de la plateforme (désactivée si modification)
        tk.Label(
            inner_frame,
            text="Plateforme *",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 5))

        self.exchange_combo_values = []
        self.exchange_var = tk.StringVar()
        self.exchange_combo = tk.ttk.Combobox(
            inner_frame,
            textvariable=self.exchange_var,
            state='readonly',
            font=(FONT_FAMILY, 10)
        )
        self.exchange_combo.pack(fill='x', ipady=8, pady=(0, 15))

        # Nom de la clé
        tk.Label(
            inner_frame,
            text="Nom de la clé",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 5))

        self.label_entry = tk.Entry(
            inner_frame,
            font=(FONT_FAMILY, 10),
            bg=self.theme['input_bg'],
            fg=self.theme['text_primary'],
            relief='solid',
            borderwidth=1,
            insertbackground=self.theme['text_primary']
        )
        self.label_entry.pack(fill='x', ipady=8, pady=(0, 15))

        # Clé API
        tk.Label(
            inner_frame,
            text="Clé API *",
            font=(FONT_FAMILY, 10, 'bold'),
            bg=self.theme['bg_secondary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 5))

        self.api_key_entry = tk.Entry(
            inner_frame,
            font=(FONT_FAMILY, 10),
            bg=self.theme['input_bg'],
            fg=self.theme['text_primary'],
            relief='solid',
            borderwidth=1,
            insertbackground=self.theme['text_primary']
        )
        self.api_key_entry.pack(fill='x', ipady=8, pady=(0, 20))

        # Boutons dans le même frame que le formulaire
        buttons_frame = tk.Frame(form_frame, bg=self.theme['bg_secondary'])
        buttons_frame.pack(fill='x', padx=20, pady=(0, 20))

        # Bouton Annuler (aligné à droite, packé en dernier)
        cancel_btn = Button.secondary(
            buttons_frame,
            "❌ Annuler",
            self.on_back_callback,
            self.theme,
            font=(FONT_FAMILY, 11, 'bold')
        )
        cancel_btn.pack(side='right', padx=(10, 0), ipady=10, ipadx=20)

        # Bouton Enregistrer (aligné à droite, packé avant annuler)
        save_btn = Button.primary(
            buttons_frame,
            "💾 Enregistrer",
            self._save,
            self.theme,
            font=(FONT_FAMILY, 11, 'bold')
        )
        save_btn.pack(side='right', padx=(0, 10), ipady=10, ipadx=20)

        # Si modification, pré-remplir les champs
        if self.api_key:
            self.api_key_entry.insert(0, self.api_key.get('api_key', '') or '')
            self.label_entry.insert(0, self.api_key.get('label', '') or '')
            self.exchange_var.set(self.api_key.get('exchange_display', '') or '')
            self.exchange_combo.config(state='disabled')

    def _load_exchanges(self):
        """Charge les exchanges disponibles"""
        try:
            self.exchanges = self.controller.list_exchanges()
            self.exchange_combo_values = [ex.get('display_name', ex.get('name')) for ex in self.exchanges]
            self.exchange_combo['values'] = self.exchange_combo_values
        except Exception as e:
            Toast.show(self.container, f"Impossible de charger les plateformes: {str(e)}", 'error')

    def _save(self):
        """Enregistre la clé API"""
        exchange_display = self.exchange_var.get().strip()
        api_key = self.api_key_entry.get().strip()
        label = self.label_entry.get().strip()

        print(f"[DEBUG FORM SAVE] exchange_display={exchange_display}, api_key length={len(api_key)}, label={label}")

        # Validation
        if not exchange_display or not api_key:
            Toast.show(self.container, "Veuillez remplir tous les champs obligatoires", 'warning')
            return

        if self.api_key:
            # Modification
            self._update_api_key(api_key, label)
        else:
            # Création
            self._create_api_key(exchange_display, api_key, label)

    def _create_api_key(self, exchange_display, api_key, label):
        """Crée une nouvelle clé API"""
        # Trouver l'exchange_id
        exchange_id = None
        for ex in self.exchanges:
            if (ex.get('display_name') or ex.get('name')) == exchange_display:
                exchange_id = ex.get('exchange_id')
                break

        if not exchange_id:
            Toast.show(self.container, "Plateforme introuvable", 'error')
            return

        print(f"[DEBUG FORM _CREATE] user_id={self.user_data['id']}, exchange_id={exchange_id}, api_key length={len(api_key)}, label={label}")
        
        success, msg = self.controller.add_api_key(
            self.user_data['id'],
            exchange_id,
            api_key,
            "",  # Pas de secret, juste la clé
            label
        )

        print(f"[DEBUG FORM _CREATE] success={success}, msg={msg}")

        if success:
            Toast.show(self.container, "Clé API enregistrée ✓", 'success')
            self.parent_frame.after(1500, self.on_success_callback)
        else:
            Toast.show(self.container, f"Impossible d'enregistrer la clé: {msg}", 'error')

    def _update_api_key(self, api_key, label):
        """Met à jour une clé API existante"""
        success, msg = self.controller.update_api_key(
            self.api_key['api_key_id'],
            api_key,
            "",  # Pas de secret, juste la clé
            label
        )

        if success:
            Toast.show(self.container, "Clé API modifiée ✓", 'success')
            self.parent_frame.after(1500, self.on_success_callback)
        else:
            Toast.show(self.container, f"Impossible de modifier la clé: {msg}", 'error')
