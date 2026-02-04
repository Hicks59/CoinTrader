import tkinter as tk

class BotListView:
    """Vue de la liste des bots"""
    
    def __init__(self, parent_frame, theme, on_add_bot_callback):
        self.parent_frame = parent_frame
        self.theme = theme
        self.on_add_bot_callback = on_add_bot_callback
        self.FONT_FAMILY = "Segoe UI"
        
        self.render()
    
    def render(self):
        """Affiche la liste des bots"""
        # Titre avec bouton ajouter
        header_frame = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(
            header_frame,
            text="Mes bots de trading",
            font=(self.FONT_FAMILY, 20, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(side='left')
        
        tk.Button(
            header_frame,
            text="➕ Ajouter un bot",
            font=(self.FONT_FAMILY, 10, 'bold'),
            bg=self.theme['accent'],
            fg=self.theme['button_text'],
            activebackground=self.theme['accent'],
            relief='flat',
            cursor='hand2',
            command=self.on_add_bot_callback
        ).pack(side='right', ipadx=20, ipady=10)
        
        # Zone pour afficher les bots
        bots_list_frame = tk.Frame(self.parent_frame, bg=self.theme['bg_primary'])
        bots_list_frame.pack(fill='both', expand=True)
        
        # Message temporaire (à remplacer par la liste réelle des bots)
        tk.Label(
            bots_list_frame,
            text="Aucun bot configuré.\nCliquez sur 'Ajouter un bot' pour commencer.",
            font=(self.FONT_FAMILY, 11),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_secondary'],
            justify='center'
        ).pack(expand=True)