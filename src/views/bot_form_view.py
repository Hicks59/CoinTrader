import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.bot_controller import BotController
from src.models.crypto_model import CryptoModel
from src.components.ui_component import Label, FormField, Separator, Input, Button

FONT_FAMILY = "Segoe UI"

# Messages d'affichage
MSG_PRICE_LOADING = "Prix: --"
MSG_PRICE_UNAVAILABLE = "Prix: Indisponible"
MSG_QUANTITY_LOADING = "Quantité: --"
MSG_QUANTITY_UNAVAILABLE = "Quantité: Prix indisponible"
MSG_BALANCE_LOADING = "Disponible: --"
MSG_BALANCE_UNAVAILABLE = "Disponible: Non connecté"

# Messages d'erreur
MSG_ERROR_PRICE_FETCH = "⚠ Impossible de récupérer le prix actuel. Vérifiez votre connexion."
MSG_ERROR_BALANCE_FETCH = "⚠ Connectez vos clés API Coinbase pour voir vos soldes"
MSG_ERROR_NO_CRYPTO = "✗ Veuillez sélectionner une crypto à acheter"
MSG_ERROR_CREATE_BOT_NO_PRICE = "✗ Impossible de créer le bot : prix indisponible. Réessayez dans quelques instants."
MSG_WARNING_AMOUNT_LIMITED = "⚠ Montant limité à {balance:.2f} (solde disponible)"
MSG_INFO_SAVE_DEV = "⚠ Fonctionnalité d'enregistrement en cours de développement"

class BotFormView:
    """Vue du formulaire d'ajout de bot"""
    
    def __init__(self, parent_frame, theme, user_data, on_back_callback, on_success_callback):
        self.parent_frame = parent_frame
        self.theme = theme
        self.user_data = user_data
        self.on_back_callback = on_back_callback
        self.on_success_callback = on_success_callback
        self.bot_entries = {}
        
        # Labels pour afficher les prix et quantités
        self.price_labels = {}
        self.available_balance = 0.0
        
        # Charger les cryptos disponibles
        try:
            self.crypto_model = CryptoModel()
            self.crypto_list = self.crypto_model.get_all_symbols()
            
            if not self.crypto_list:
                print("⚠ Aucune crypto chargée, utilisation d'une liste par défaut")
                self.crypto_list = ['BTC', 'ETH', 'USDC', 'USDT']
            
            print(f"✓ {len(self.crypto_list)} cryptos chargées pour le formulaire")
        except Exception as e:
            print(f"✗ Erreur chargement cryptos: {e}")
            self.crypto_list = ['BTC', 'ETH', 'USDC', 'USDT']
        
        self.render()
    
    def render(self):
        """Affiche le formulaire d'ajout de bot"""
        # Header avec titre et bouton retour
        self._create_header()
        
        # Carte du formulaire
        self._create_form_card()
    
    def _create_header(self):
        """Crée le header avec titre et bouton retour"""
        header_frame = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
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
            command=self.on_back_callback
        )
        back_btn.pack(side='left', padx=(0, 20), ipadx=10, ipady=8)
        
        # Titre avec icône
        title_frame = tk.Frame(header_frame, bg=self.theme['bg_primary'])
        title_frame.pack(side='left')
        
        tk.Label(
            title_frame,
            text="🤖",
            font=(FONT_FAMILY, 24),
            bg=self.theme['bg_primary'],
            fg=self.theme['accent']
        ).pack(side='left', padx=(0, 10))
        
        tk.Label(
            title_frame,
            text="Nouveau bot de trading",
            font=(FONT_FAMILY, 22, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(side='left')
        
        # Sous-titre
        help_text = Label.help_text(
            header_frame,
            "Configurez votre stratégie de trading automatisée",
            self.theme,
            bg=self.theme['bg_primary'],
            font=(FONT_FAMILY, 9)
        )
        help_text.pack(side='left', padx=(15, 0))
    
    def _create_form_card(self):
        """Crée la carte contenant le formulaire"""
        # Container avec effet de profondeur
        card_container = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        card_container.pack(fill='both', expand=True)
        
        # Carte principale
        form_card = tk.Frame(
            card_container,
            bg=self.theme['bg_secondary'],
            relief='flat',
            highlightthickness=1,
            highlightbackground=self.theme['border']
        )
        form_card.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Container avec padding REDUIT
        form_container = tk.Frame(form_card, bg=self.theme['bg_secondary'])
        form_container.pack(fill='both', expand=True, padx=40, pady=20)
        
        # Section 1: Configuration de base
        self._create_section_header(form_container, "⚙️ Configuration de base")
        self._create_base_config_fields(form_container)
        
        # Séparateur
        sep = Separator.horizontal(form_container, self.theme)
        sep.pack(fill='x', pady=15)
        
        # Section 2: Stratégie de trading
        self._create_section_header(form_container, "📈 Stratégie de trading")
        self._create_strategy_fields(form_container)
        
        # Footer avec boutons
        self._create_form_footer(form_container)
    
    def _create_section_header(self, parent, text):
        """Crée un en-tête de section"""
        header = Label.subtitle(parent, text, self.theme)
        header.pack(fill='x', pady=(10, 10))  # Réduit de 15 à 10
    
    def _create_base_config_fields(self, parent):
        """Crée les 3 champs de base sur une seule ligne"""
        row = tk.Frame(parent, bg=self.theme['bg_secondary'])
        row.pack(fill='x', pady=(0, 0))
        
        # Colonne 1 - Exchange
        col1 = tk.Frame(row, bg=self.theme['bg_secondary'])
        col1.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        label1 = Label.field_label(col1, "Exchange", self.theme, icon="🏦")
        label1.pack(fill='x', pady=(0, 8))
        
        # Charger les exchanges dynamiquement
        from src.controllers.exchange_controller import ExchangeController
        exch_ctrl = ExchangeController()
        exchanges = exch_ctrl.list_exchanges()
        exchange_display = [(e.get('display_name') or e.get('name')) for e in exchanges]

        self.bot_entries['exchange'] = ttk.Combobox(
            col1,
            values=exchange_display or ["Coinbase"],
            state='readonly',
            font=(FONT_FAMILY, 11),
            height=12
        )
        if exchange_display:
            self.bot_entries['exchange'].set(exchange_display[0])
        else:
            self.bot_entries['exchange'].set("Coinbase")
        self.bot_entries['exchange'].pack(fill='x', ipady=10)
        
        # Colonne 2 - Crypto à acheter
        col2 = tk.Frame(row, bg=self.theme['bg_secondary'])
        col2.pack(side='left', fill='both', expand=True, padx=(10, 10))
        
        label2 = Label.field_label(col2, "Crypto à acheter", self.theme, icon="💰")
        label2.pack(fill='x', pady=(0, 8))
        
        self.bot_entries['crypto_source'] = ttk.Combobox(
            col2,
            values=self.crypto_list,
            font=(FONT_FAMILY, 11),
            state='normal',
            height=12
        )
        self.bot_entries['crypto_source'].pack(fill='x', ipady=10)
        self.bot_entries['crypto_source'].bind('<<ComboboxSelected>>', self._on_crypto_source_change)
        
        self.price_labels['source'] = Label.help_text(col2, MSG_PRICE_LOADING, self.theme, fg=self.theme['accent'])
        self.price_labels['source'].pack(anchor='w', pady=(5, 0))
        
        # Colonne 3 - Payer avec
        col3 = tk.Frame(row, bg=self.theme['bg_secondary'])
        col3.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        label3 = Label.field_label(col3, "Payer avec", self.theme, icon="💵")
        label3.pack(fill='x', pady=(0, 8))
        
        self.bot_entries['crypto_target'] = ttk.Combobox(
            col3,
            values=self.crypto_list,
            font=(FONT_FAMILY, 11),
            state='normal',
            height=12
        )
        self.bot_entries['crypto_target'].set("USDC")
        self.bot_entries['crypto_target'].pack(fill='x', ipady=10)
        self.bot_entries['crypto_target'].bind('<<ComboboxSelected>>', self._on_crypto_target_change)
        
        self.price_labels['target'] = Label.help_text(col3, MSG_BALANCE_LOADING, self.theme, fg=self.theme['accent'])
        self.price_labels['target'].pack(anchor='w', pady=(5, 0))
    
    def _create_strategy_fields(self, parent):
        """Crée les 3 champs de stratégie sur une seule ligne"""
        row = tk.Frame(parent, bg=self.theme['bg_secondary'])
        row.pack(fill='x', pady=(0, 0))
        
        # Colonne 1 - Prix d'achat cible
        col1 = tk.Frame(row, bg=self.theme['bg_secondary'])
        col1.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        field1 = FormField(
            col1, 
            "Prix d'achat cible", 
            self.theme, 
            icon="🎯",
            help_text="Optionnel - Prix marché par défaut"
        )
        field1.pack(fill='x', pady=0)
        self.bot_entries['prix_achat'] = field1.input
        
        # Colonne 2 - Pourcentage de gain
        col2 = tk.Frame(row, bg=self.theme['bg_secondary'])
        col2.pack(side='left', fill='both', expand=True, padx=(10, 10))
        
        field2 = FormField(
            col2,
            "Objectif de gain (%)",
            self.theme,
            icon="📊",
            help_text="Profit visé avant revente"
        )
        field2.pack(fill='x', pady=0)
        field2.set("5")
        self.bot_entries['pourcentage_gain'] = field2.input
        
        # Colonne 3 - Montant du trade
        col3 = tk.Frame(row, bg=self.theme['bg_secondary'])
        col3.pack(side='left', fill='both', expand=True, padx=(10, 0))
        
        label3 = Label.field_label(col3, "Montant à investir", self.theme, icon="💎")
        label3.pack(fill='x', pady=(0, 8))
        
        amount_frame = tk.Frame(col3, bg=self.theme['input_bg'], relief='solid', borderwidth=1)
        amount_frame.pack(fill='x')
        
        self.bot_entries['montant_trade'] = Input.text(
            amount_frame,
            self.theme,
            relief='flat',
            borderwidth=0
        )
        self.bot_entries['montant_trade'].pack(fill='x', ipady=10, padx=8)
        self.bot_entries['montant_trade'].insert(0, "100")
        self.bot_entries['montant_trade'].bind('<KeyRelease>', self._validate_amount)
        
        self.price_labels['quantity'] = Label.help_text(col3, MSG_QUANTITY_LOADING, self.theme, fg=self.theme['accent'])
        self.price_labels['quantity'].pack(anchor='w', pady=(5, 0))
    
    def _create_form_footer(self, parent):
        """Crée le footer avec message de statut et boutons"""
        footer = tk.Frame(parent, bg=self.theme['bg_secondary'])
        footer.pack(fill='x', pady=(20, 0))  # Réduit de 30 à 20
        
        # Message de statut
        self.bot_status_label = Label.status(footer, self.theme)
        self.bot_status_label.pack(fill='x', pady=(0, 10))
        
        # Boutons avec composants Button
        # Bouton Enregistrer (unique)
        register_btn = Button.primary(
            footer,
            "💾 Enregistrer",
            self.register_bot,
            self.theme,
            font=(FONT_FAMILY, 11, 'bold')
        )
        register_btn.pack(side='right', ipadx=25, ipady=12)
    
    def _on_crypto_source_change(self, event=None):
        """Met à jour le prix quand la crypto source change"""
        crypto = self.bot_entries['crypto_source'].get()
        if crypto:
            price = self._get_crypto_price(crypto)
            
            if price is not None:
                self.price_labels['source'].config(text=f"Prix: ${price:,.2f}", fg=self.theme['accent'])
            else:
                self.price_labels['source'].config(text=MSG_PRICE_UNAVAILABLE, fg='#F44336')
                self.bot_status_label.config(text=MSG_ERROR_PRICE_FETCH, fg='#FF9800')
            
            self._update_quantity_estimate()
    
    def _on_crypto_target_change(self, event=None):
        """Met à jour le solde disponible quand la crypto target change"""
        crypto = self.bot_entries['crypto_target'].get()
        if crypto:
            balance = self._get_available_balance(crypto)
            
            if balance is not None:
                self.price_labels['target'].config(
                    text=f"Disponible: {balance:.2f} {crypto}",
                    fg=self.theme['accent']
                )
                self.available_balance = balance
            else:
                self.price_labels['target'].config(text=MSG_BALANCE_UNAVAILABLE, fg='#FF9800')
                self.available_balance = 0.0
                self.bot_status_label.config(text=MSG_ERROR_BALANCE_FETCH, fg='#FF9800')
    
    def _validate_amount(self, event=None):
        """Valide et limite le montant du trade"""
        try:
            amount = float(self.bot_entries['montant_trade'].get())
            
            if amount > self.available_balance and self.available_balance > 0:
                self.bot_entries['montant_trade'].delete(0, tk.END)
                self.bot_entries['montant_trade'].insert(0, str(self.available_balance))
                self.bot_status_label.config(
                    text=MSG_WARNING_AMOUNT_LIMITED.format(balance=self.available_balance),
                    fg='#FF9800'
                )
            else:
                self.bot_status_label.config(text="")
            
            self._update_quantity_estimate()
        except ValueError:
            pass
    
    def _update_quantity_estimate(self):
        """Met à jour l'estimation de la quantité de crypto à acheter"""
        try:
            crypto = self.bot_entries['crypto_source'].get()
            amount_str = self.bot_entries['montant_trade'].get()
            
            if not amount_str:
                self.price_labels['quantity'].config(text=MSG_QUANTITY_LOADING)
                return
            
            amount = float(amount_str)
            
            if crypto and amount > 0:
                price = self._get_crypto_price(crypto)
                
                if price is not None and price > 0:
                    quantity = amount / price
                    self.price_labels['quantity'].config(
                        text=f"≈ {quantity:.8f} {crypto}",
                        fg=self.theme['accent']
                    )
                else:
                    self.price_labels['quantity'].config(text=MSG_QUANTITY_UNAVAILABLE, fg='#F44336')
            else:
                self.price_labels['quantity'].config(text=MSG_QUANTITY_LOADING)
                
        except (ValueError, ZeroDivisionError):
            self.price_labels['quantity'].config(text=MSG_QUANTITY_LOADING)
    
    def _get_crypto_price(self, symbol):
        """Récupère le prix actuel d'une crypto"""
        exchange = self.bot_entries['exchange'].get().lower()
        price = self.crypto_model.get_crypto_price(symbol, exchange, 'USDC')
        
        if price is None:
            print(f"⚠ Prix non disponible pour {symbol}")
        
        return price
    
    def _get_available_balance(self, symbol):
        """Récupère le solde disponible d'une crypto"""
        exchange = self.bot_entries['exchange'].get().lower()
        balance = self.crypto_model.get_available_balance(
            symbol, 
            exchange, 
            self.user_data['id']
        )
        
        if balance is None:
            print(f"⚠ Solde non disponible pour {symbol}")
        
        return balance
    
    def save_bot(self):
        """Enregistre le bot sans l'activer"""
        self.bot_status_label.config(text=MSG_INFO_SAVE_DEV, fg='#FF9800')
    
    def register_bot(self):
        """Enregistre le bot et demande si l'activer"""
        crypto_source = self.bot_entries['crypto_source'].get()
        
        if not crypto_source:
            self.bot_status_label.config(text=MSG_ERROR_NO_CRYPTO, fg='#F44336')
            return
        
        price = self._get_crypto_price(crypto_source)
        if price is None:
            self.bot_status_label.config(text=MSG_ERROR_CREATE_BOT_NO_PRICE, fg='#F44336')
            return
        
        exchange = self.bot_entries['exchange'].get()
        crypto_target = self.bot_entries['crypto_target'].get()
        prix_achat = self.bot_entries['prix_achat'].get()
        pourcentage_gain = self.bot_entries['pourcentage_gain'].get()
        montant_trade = self.bot_entries['montant_trade'].get()
        product_id = f"{crypto_source}-{crypto_target}"
        type_ordre = "Market"
        
        try:
            bot_controller = BotController()
            result = bot_controller.create_bot(
                user_id=self.user_data['id'],
                exchange=exchange,
                product_id=product_id,
                crypto_source=crypto_source,
                crypto_target=crypto_target,
                prix_achat=prix_achat,
                pourcentage_gain=pourcentage_gain,
                montant_trade=montant_trade,
                type_ordre=type_ordre
            )
            
            if result['success']:
                # Afficher popup de confirmation d'activation
                self._show_activation_popup(result['bot_id'])
            else:
                self.bot_status_label.config(text=f"✗ {result['message']}", fg='#F44336')
                
        except Exception as e:
            print(f"✗ Erreur création bot: {e}")
            self.bot_status_label.config(text=f"✗ Erreur: {str(e)}", fg='#F44336')
    
    def _show_activation_popup(self, bot_id):
        """Affiche une popup pour demander l'activation du bot"""
        # Créer une fenêtre popup
        popup = tk.Toplevel(self.parent_frame)
        popup.title("Activer le bot")
        popup.resizable(False, False)
        popup.attributes('-topmost', True)
        
        # Centrer la popup
        popup.geometry("350x150")
        popup.configure(bg=self.theme['bg_primary'])
        
        # Message
        msg_frame = tk.Frame(popup, bg=self.theme['bg_primary'])
        msg_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        msg_label = tk.Label(
            msg_frame,
            text="Voulez-vous activer ce bot maintenant ?",
            font=(FONT_FAMILY, 11),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary'],
            wraplength=300
        )
        msg_label.pack(pady=(0, 20))
        
        # Boutons
        btn_frame = tk.Frame(msg_frame, bg=self.theme['bg_primary'])
        btn_frame.pack(fill='x')
        
        def activate():
            popup.destroy()
            # Activer le bot
            bot_controller = BotController()
            result = bot_controller.toggle_bot(bot_id, True)
            if result['success']:
                self.bot_status_label.config(text="✓ Bot enregistré et activé", fg='#4CAF50')
            else:
                self.bot_status_label.config(text=f"✗ {result['message']}", fg='#F44336')
            self.parent_frame.after(1500, self.on_success_callback)
        
        def deactivate():
            popup.destroy()
            # Bot reste désactivé (déjà l'état par défaut)
            self.bot_status_label.config(text="✓ Bot enregistré (désactivé)", fg='#4CAF50')
            self.parent_frame.after(1500, self.on_success_callback)
        
        yes_btn = Button.primary(
            btn_frame,
            "✓ Oui",
            activate,
            self.theme
        )
        yes_btn.pack(side='left', padx=(0, 10))
        
        no_btn = Button.secondary(
            btn_frame,
            "✗ Non",
            deactivate,
            self.theme
        )
        no_btn.pack(side='right', padx=(10, 0))