import tkinter as tk
from tkinter import ttk
from src.models.database_model import DatabaseModel

FONT_FAMILY = "Segoe UI"

FILTERS = [
    ("Tous",           None),
    ("Plateformes",     "PLATFORM_ADDED"),
    ("Bots",            "BOT_ADDED"),
    ("Transactions",    "ORDER_ADDED"),
    ("Sécurité",       "SECURITY_UPDATE"),
]

ACTION_LABELS = {
    "PLATFORM_ADDED": "Plateforme",
    "BOT_ADDED":      "Bot",
    "ORDER_ADDED":    "Transaction",
    "SECURITY_UPDATE": "Sécurité",
}

_TREE_STYLE = "History.Treeview"


class HistoryView:
    """Vue de l'historique d'activité utilisateur"""

    def __init__(self, parent_frame, theme, user_data):
        self.parent_frame = parent_frame
        self.theme = theme
        self.user_data = user_data
        self.db = DatabaseModel()
        self.active_filter = None

        self._build()

    def _build(self):
        # Titre
        tk.Label(
            self.parent_frame,
            text="Historique d'activité",
            font=(FONT_FAMILY, 20, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 16))

        # Barre de filtres
        filter_bar = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        filter_bar.pack(anchor='w', pady=(0, 16))

        self.filter_buttons = {}
        for label, action_type in FILTERS:
            btn = tk.Button(
                filter_bar,
                text=label,
                font=(FONT_FAMILY, 9, 'bold'),
                relief='flat',
                cursor='hand2',
                command=lambda at=action_type: self._apply_filter(at)
            )
            btn.pack(side='left', padx=(0, 8), ipadx=12, ipady=6)
            self.filter_buttons[action_type] = btn

        self._style_filter_buttons()

        # Tableau (Treeview)
        table_frame = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        table_frame.pack(fill='both', expand=True)

        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            _TREE_STYLE,
            background=self.theme['bg_secondary'],
            foreground=self.theme['text_primary'],
            fieldbackground=self.theme['bg_secondary'],
            rowheight=32,
            font=(FONT_FAMILY, 10),
            borderwidth=0
        )
        style.configure(
            _TREE_STYLE + ".Heading",
            background=self.theme.get('bg_header', self.theme['bg_secondary']),
            foreground=self.theme['text_secondary'],
            font=(FONT_FAMILY, 9, 'bold'),
            relief='flat'
        )
        style.map(_TREE_STYLE, background=[('selected', self.theme['accent'])])

        columns = ('date', 'type', 'description')
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show='headings',
            style=_TREE_STYLE,
            selectmode='browse'
        )

        self.tree.heading('date',        text='Date')
        self.tree.heading('type',        text='Type')
        self.tree.heading('description', text='Description')

        self.tree.column('date',        width=160, anchor='center', stretch=False)
        self.tree.column('type',        width=180, anchor='center', stretch=False)
        self.tree.column('description', width=400, anchor='w',      stretch=True)

        self.scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)

        def _on_yscroll(first, last):
            if float(first) <= 0.0 and float(last) >= 1.0:
                self.scrollbar.pack_forget()
            else:
                self.scrollbar.pack(side='right', fill='y', before=self.tree)
            self.scrollbar.set(first, last)

        self.tree.configure(yscrollcommand=_on_yscroll)
        self.tree.pack(side='left', fill='both', expand=True)

        self._load_logs()

    def _apply_filter(self, action_type):
        self.active_filter = action_type
        self._style_filter_buttons()
        self._load_logs()

    def _style_filter_buttons(self):
        for at, btn in self.filter_buttons.items():
            if at == self.active_filter:
                btn.config(
                    bg=self.theme['accent'],
                    fg=self.theme['button_text'],
                    activebackground=self.theme['accent']
                )
            else:
                btn.config(
                    bg=self.theme['bg_secondary'],
                    fg=self.theme['text_primary'],
                    activebackground=self.theme['bg_secondary']
                )

    def _load_logs(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        logs = self.db.get_activity_logs(self.user_data['id'], self.active_filter)

        if not logs:
            self.tree.insert('', 'end', values=('—', '—', 'Aucune activité enregistrée'))
            return

        for log in logs:
            date_str = str(log['created_at'])[:16].replace('T', ' ')
            type_label = ACTION_LABELS.get(log['action_type'], log['action_type'])
            self.tree.insert('', 'end', values=(date_str, type_label, log['description']))
