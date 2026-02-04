import tkinter as tk

class HistoryView:
    """Vue de l'historique des transactions"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.FONT_FAMILY = "Segoe UI"
        
        self.render()
    
    def render(self):
        """Affiche l'historique"""
        tk.Label(
            self.parent_frame,
            text="Historique des transactions",
            font=(self.FONT_FAMILY, 20, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 20))
        
        # Contenu de l'historique à implémenter
        tk.Label(
            self.parent_frame,
            text="Aucune transaction pour le moment.",
            font=(self.FONT_FAMILY, 11),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_secondary'],
            justify='center'
        ).pack(expand=True)