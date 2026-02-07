import tkinter as tk

class DashboardView:
    """Vue du tableau de bord"""
    
    def __init__(self, parent_frame, theme):
        self.parent_frame = parent_frame
        self.theme = theme
        self.FONT_FAMILY = "Segoe UI"
        
        self.render()
    
    def render(self):
        """Affiche le tableau de bord"""
        tk.Label(
            self.parent_frame,
            text="Tableau de bord",
            font=(self.FONT_FAMILY, 20, 'bold'),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_primary']
        ).pack(anchor='w', pady=(0, 20))
        
        # Contenu du dashboard à implémenter
        tk.Label(
            self.parent_frame,
            text="Bienvenue sur CoinTrader !\n\nVotre tableau de bord sera bientôt disponible.",
            font=(self.FONT_FAMILY, 11),
            bg=self.theme['bg_primary'],
            fg=self.theme['text_secondary'],
            justify='center'
        ).pack(expand=True)