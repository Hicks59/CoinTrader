import tkinter as tk
from tkinter import ttk, messagebox
from src.controllers.exchange_controller import ExchangeController
from src.components.ui_component import Label, FormField, Button, Input

FONT_FAMILY = "Segoe UI"

class PlatformsView:
    """Vue pour gérer les plateformes (exchanges) et les API-keys utilisateur"""

    def __init__(self, parent_frame, theme, user_data):
        self.parent_frame = parent_frame
        self.theme = theme
        self.user_data = user_data
        self.controller = ExchangeController()

        self.container = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        self.container.pack(fill='both', expand=True)

        self._build_ui()
        self._load_exchanges()
        self._load_api_keys()

    def _build_ui(self):
        header = Label.title(self.container, "Plateformes", self.theme)
        header.pack(fill='x', pady=(0, 12))

        main_row = tk.Frame(self.container, bg=self.theme['bg_primary'])
        main_row.pack(fill='both', expand=True)

        # Left: liste des exchanges + ajout manuel
        left = tk.Frame(main_row, bg=self.theme['bg_secondary'])
        left.pack(side='left', fill='both', expand=True, padx=(0, 10), pady=10)

        Label.subtitle(left, "Exchanges", self.theme).pack(anchor='w', padx=10, pady=(6, 6))

        self.exchange_listbox = tk.Listbox(left, height=10)
        self.exchange_listbox.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.exchange_listbox.bind('<<ListboxSelect>>', self._on_exchange_select)

        add_frame = tk.Frame(left, bg=self.theme['bg_secondary'])
        add_frame.pack(fill='x', padx=10)

        self.new_exchange_name = Input.text(add_frame, self.theme, placeholder="identifiant (ex: coinbase)")
        self.new_exchange_name.pack(fill='x', pady=(0,6))
        self.new_exchange_display = Input.text(add_frame, self.theme, placeholder="Nom affiché (ex: Coinbase)")
        self.new_exchange_display.pack(fill='x', pady=(0,6))

        add_btn = Button.primary(add_frame, "➕ Ajouter plateforme", self._add_exchange, self.theme)
        add_btn.pack(fill='x')

        # Right: API keys pour l'utilisateur
        right = tk.Frame(main_row, bg=self.theme['bg_secondary'])
        right.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)

        Label.subtitle(right, "Mes clés API", self.theme).pack(anchor='w', padx=10, pady=(6,6))

        self.api_keys_tree = ttk.Treeview(right, columns=("exchange","key"), show='headings')
        self.api_keys_tree.heading('exchange', text='Exchange')
        self.api_keys_tree.heading('key', text='API Key (partielle)')
        self.api_keys_tree.pack(fill='both', expand=True, padx=10, pady=(0,6))

        form_frame = tk.Frame(right, bg=self.theme['bg_secondary'])
        form_frame.pack(fill='x', padx=10)

        Label.field_label(form_frame, "Exchange *", self.theme).pack(anchor='w')
        self.api_exchange_combo = ttk.Combobox(form_frame, values=[], state='readonly')
        self.api_exchange_combo.pack(fill='x', pady=(4,6))

        Label.field_label(form_frame, "API Key *", self.theme).pack(anchor='w')
        self.api_key_entry = Input.text(form_frame, self.theme, placeholder="API Key")
        self.api_key_entry.pack(fill='x', pady=(4,6))

        Label.field_label(form_frame, "API Secret *", self.theme).pack(anchor='w')
        self.api_secret_entry = Input.password(form_frame, self.theme)
        self.api_secret_entry.pack(fill='x', pady=(4,6))

        action_frame = tk.Frame(form_frame, bg=self.theme['bg_secondary'])
        action_frame.pack(fill='x', pady=(6,0))

        save_key_btn = Button.primary(action_frame, "💾 Enregistrer clé", self._add_api_key, self.theme)
        save_key_btn.pack(side='left')

        del_key_btn = Button.danger(action_frame, "🗑 Supprimer clé", self._delete_selected_key, self.theme)
        del_key_btn.pack(side='right')

    def _load_exchanges(self):
        exchanges = self.controller.list_exchanges()
        self.exchange_listbox.delete(0, tk.END)
        combo_values = []
        for ex in exchanges:
            display = ex.get('display_name') or ex.get('name')
            self.exchange_listbox.insert(tk.END, display)
            combo_values.append(display)
        self.api_exchange_combo['values'] = combo_values

    def _load_api_keys(self):
        keys = self.controller.get_api_keys_for_user(self.user_data['id'])
        for row in self.api_keys_tree.get_children():
            self.api_keys_tree.delete(row)
        for k in keys:
            short = (k['api_key'][:6] + '...') if k['api_key'] else ''
            self.api_keys_tree.insert('', tk.END, iid=k['api_key_id'], values=(k['exchange_display'], short))

    def _on_exchange_select(self, event=None):
        sel = self.exchange_listbox.curselection()
        if not sel:
            return
        idx = sel[0]
        display = self.exchange_listbox.get(idx)
        # pré-remplir le combobox d'ajout de clé
        self.api_exchange_combo.set(display)

    def _add_exchange(self):
        name = self.new_exchange_name.get().strip()
        display = self.new_exchange_display.get().strip()
        if not name or not display:
            messagebox.showwarning("Champs manquants", "Veuillez renseigner l'identifiant et le nom affiché de la plateforme")
            return
        success, msg = self.controller.add_exchange(name, display)
        if success:
            messagebox.showinfo("Succès", "Plateforme ajoutée")
            self.new_exchange_name.delete(0, tk.END)
            self.new_exchange_display.delete(0, tk.END)
            self._load_exchanges()
        else:
            messagebox.showerror("Erreur", f"Impossible d'ajouter la plateforme: {msg}")

    def _add_api_key(self):
        exchange_display = self.api_exchange_combo.get()
        key = self.api_key_entry.get().strip()
        secret = self.api_secret_entry.get().strip()
        if not exchange_display or not key or not secret:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs pour enregistrer la clé API")
            return
        # Trouver exchange_id par display
        exchanges = self.controller.list_exchanges()
        exchange_id = None
        for ex in exchanges:
            if (ex.get('display_name') or ex.get('name')) == exchange_display:
                exchange_id = ex.get('exchange_id')
                break
        if not exchange_id:
            messagebox.showerror("Erreur", "Exchange introuvable")
            return
        success, msg = self.controller.add_api_key(self.user_data['id'], exchange_id, key, secret)
        if success:
            messagebox.showinfo("Succès", "Clé API enregistrée")
            self.api_key_entry.delete(0, tk.END)
            self.api_secret_entry.delete(0, tk.END)
            self._load_api_keys()
        else:
            messagebox.showerror("Erreur", f"Impossible d'ajouter la clé: {msg}")

    def _delete_selected_key(self):
        sel = self.api_keys_tree.selection()
        if not sel:
            messagebox.showwarning("Sélectionner", "Veuillez sélectionner une clé à supprimer")
            return
        api_key_id = int(sel[0])
        ok = messagebox.askyesno("Confirmer", "Supprimer la clé sélectionnée ?")
        if not ok:
            return
        success, msg = self.controller.delete_api_key(api_key_id)
        if success:
            messagebox.showinfo("Supprimé", "Clé supprimée")
            self._load_api_keys()
        else:
            messagebox.showerror("Erreur", f"Impossible de supprimer la clé: {msg}")
