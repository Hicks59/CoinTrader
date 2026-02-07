"""
Composants UI réutilisables pour l'application CoinTrader
"""
import tkinter as tk
from tkinter import ttk

FONT_FAMILY = "Segoe UI"


class Button:
    """Composant Button avec styles prédéfinis"""
    
    @staticmethod
    def primary(parent, text, command, theme, **kwargs):
        """
        Bouton principal (accent color)
        
        Args:
            parent: Widget parent
            text (str): Texte du bouton
            command: Fonction à exécuter
            theme (dict): Thème de l'application
            **kwargs: Arguments supplémentaires pour le bouton
        """
        default_config = {
            'font': (FONT_FAMILY, 10, 'bold'),
            'bg': theme['accent'],
            'fg': theme['button_text'],
            'activebackground': theme['accent'],
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 6  # Hauteur réduite
        }
        
        config = {**default_config, **kwargs}
        btn = tk.Button(parent, text=text, command=command, **config)
        return btn
    
    @staticmethod
    def secondary(parent, text, command, theme, **kwargs):
        """
        Bouton secondaire (style bordure)
        
        Args:
            parent: Widget parent
            text (str): Texte du bouton
            command: Fonction à exécuter
            theme (dict): Thème de l'application
            **kwargs: Arguments supplémentaires pour le bouton
        """
        default_config = {
            'font': (FONT_FAMILY, 10, 'bold'),
            'bg': theme['bg_secondary'],
            'fg': theme['text_primary'],
            'activebackground': theme['bg_primary'],
            'relief': 'solid',
            'borderwidth': 1,
            'cursor': 'hand2',
            'padx': 20,
            'pady': 6  # Hauteur réduite
        }
        
        config = {**default_config, **kwargs}
        btn = tk.Button(parent, text=text, command=command, **config)
        return btn
    
    @staticmethod
    def danger(parent, text, command, theme, **kwargs):
        """
        Bouton danger (rouge)
        
        Args:
            parent: Widget parent
            text (str): Texte du bouton
            command: Fonction à exécuter
            theme (dict): Thème de l'application
            **kwargs: Arguments supplémentaires pour le bouton
        """
        default_config = {
            'font': (FONT_FAMILY, 10, 'bold'),
            'bg': '#F44336',
            'fg': '#FFFFFF',
            'activebackground': '#D32F2F',
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 6  # Hauteur réduite
        }
        
        config = {**default_config, **kwargs}
        btn = tk.Button(parent, text=text, command=command, **config)
        return btn
    
    @staticmethod
    def warning(parent, text, command, theme, **kwargs):
        """
        Bouton warning (orange)
        
        Args:
            parent: Widget parent
            text (str): Texte du bouton
            command: Fonction à exécuter
            theme (dict): Thème de l'application
            **kwargs: Arguments supplémentaires pour le bouton
        """
        default_config = {
            'font': (FONT_FAMILY, 10, 'bold'),
            'bg': '#FF9800',
            'fg': '#FFFFFF',
            'activebackground': '#F57C00',
            'relief': 'flat',
            'cursor': 'hand2',
            'padx': 20,
            'pady': 6  # Hauteur réduite
        }
        
        config = {**default_config, **kwargs}
        btn = tk.Button(parent, text=text, command=command, **config)
        return btn
    
    @staticmethod
    def icon(parent, text, command, theme, **kwargs):
        """
        Bouton icône (petit, carré)
        
        Args:
            parent: Widget parent
            text (str): Icône/texte du bouton
            command: Fonction à exécuter
            theme (dict): Thème de l'application
            **kwargs: Arguments supplémentaires pour le bouton
        """
        default_config = {
            'font': (FONT_FAMILY, 16),
            'bg': theme['bg_secondary'],
            'fg': theme['text_primary'],
            'activebackground': theme['bg_primary'],
            'relief': 'flat',
            'cursor': 'hand2',
            'width': 3,
            'height': 1
        }
        
        config = {**default_config, **kwargs}
        btn = tk.Button(parent, text=text, command=command, **config)
        return btn


class ButtonGroup:
    """Groupe de boutons avec layout automatique"""
    
    def __init__(self, parent, theme, orientation='horizontal'):
        """
        Initialise un groupe de boutons
        
        Args:
            parent: Widget parent
            theme (dict): Thème de l'application
            orientation (str): 'horizontal' ou 'vertical'
        """
        self.frame = tk.Frame(parent, bg=theme['bg_secondary'])
        self.theme = theme
        self.orientation = orientation
        self.buttons = []
    
    def add_primary(self, text, command, side='right', **kwargs):
        """Ajoute un bouton primary"""
        btn = Button.primary(self.frame, text, command, self.theme, **kwargs)
        btn.pack(side=side, padx=5, pady=2)
        self.buttons.append(btn)
        return btn
    
    def add_secondary(self, text, command, side='left', **kwargs):
        """Ajoute un bouton secondary"""
        btn = Button.secondary(self.frame, text, command, self.theme, **kwargs)
        btn.pack(side=side, padx=5, pady=2)
        self.buttons.append(btn)
        return btn
    
    def add_danger(self, text, command, side='right', **kwargs):
        """Ajoute un bouton danger"""
        btn = Button.danger(self.frame, text, command, self.theme, **kwargs)
        btn.pack(side=side, padx=5, pady=2)
        self.buttons.append(btn)
        return btn
    
    def add_warning(self, text, command, side='right', **kwargs):
        """Ajoute un bouton warning"""
        btn = Button.warning(self.frame, text, command, self.theme, **kwargs)
        btn.pack(side=side, padx=5, pady=2)
        self.buttons.append(btn)
        return btn
    
    def pack(self, **kwargs):
        """Pack le frame contenant les boutons"""
        self.frame.pack(**kwargs)
        return self.frame
    
    def grid(self, **kwargs):
        """Grid le frame contenant les boutons"""
        self.frame.grid(**kwargs)
        return self.frame


class Input:
    """Composant Input avec styles prédéfinis"""
    
    @staticmethod
    def text(parent, theme, placeholder="", **kwargs):
        """
        Input texte standard
        
        Args:
            parent: Widget parent
            theme (dict): Thème de l'application
            placeholder (str): Texte placeholder
            **kwargs: Arguments supplémentaires
        """
        default_config = {
            'font': (FONT_FAMILY, 11),
            'bg': theme['input_bg'],
            'fg': theme['text_primary'],
            'relief': 'solid',
            'borderwidth': 1,
            'insertbackground': theme['text_primary']
        }
        
        config = {**default_config, **kwargs}
        entry = tk.Entry(parent, **config)
        
        if placeholder:
            entry.insert(0, placeholder)
        
        return entry
    
    @staticmethod
    def password(parent, theme, **kwargs):
        """
        Input mot de passe
        
        Args:
            parent: Widget parent
            theme (dict): Thème de l'application
            **kwargs: Arguments supplémentaires
        """
        return Input.text(parent, theme, show='•', **kwargs)


class Label:
    """Composant Label avec styles prédéfinis"""
    
    @staticmethod
    def title(parent, text, theme, **kwargs):
        """Label titre principal"""
        default_config = {
            'font': (FONT_FAMILY, 24, 'bold'),
            'bg': theme['bg_primary'],
            'fg': theme['text_primary']
        }
        
        config = {**default_config, **kwargs}
        return tk.Label(parent, text=text, **config)
    
    @staticmethod
    def subtitle(parent, text, theme, **kwargs):
        """Label sous-titre"""
        default_config = {
            'font': (FONT_FAMILY, 14, 'bold'),
            'bg': theme['bg_secondary'],
            'fg': theme['text_primary']
        }
        
        config = {**default_config, **kwargs}
        return tk.Label(parent, text=text, **config)
    
    @staticmethod
    def field_label(parent, text, theme, icon="", **kwargs):
        """
        Label de champ de formulaire avec astérisque rouge pour champs obligatoires
        
        Args:
            parent: Widget parent
            text (str): Texte du label (ajouter " *" à la fin pour champ obligatoire)
            theme (dict): Thème de l'application
            icon (str): Icône optionnelle
            **kwargs: Arguments supplémentaires
        """
        frame = tk.Frame(parent, bg=theme['bg_secondary'])
        
        # Icône si fournie
        if icon:
            tk.Label(
                frame,
                text=icon,
                font=(FONT_FAMILY, 11),
                bg=theme['bg_secondary'],
                fg=theme['accent']
            ).pack(side='left', padx=(0, 8))
        
        # Séparer le texte et l'astérisque
        if text.endswith(' *'):
            text_without_star = text[:-2]
            has_star = True
        else:
            text_without_star = text
            has_star = False
        
        default_config = {
            'font': (FONT_FAMILY, 10, 'bold'),
            'bg': theme['bg_secondary'],
            'fg': theme['text_primary'],
            'anchor': 'w'
        }
        
        config = {**default_config, **kwargs}
        
        # Label principal
        tk.Label(frame, text=text_without_star, **config).pack(side='left')
        
        # Astérisque en rouge
        if has_star:
            tk.Label(
                frame,
                text=" *",
                font=(FONT_FAMILY, 10, 'bold'),
                bg=theme['bg_secondary'],
                fg='#F44336',
                anchor='w'
            ).pack(side='left')
        
        return frame
    
    @staticmethod
    def status(parent, theme, **kwargs):
        """Label de statut (messages success/error)"""
        default_config = {
            'font': (FONT_FAMILY, 9),
            'bg': theme['bg_secondary'],
            'fg': '#4CAF50',
            'anchor': 'w'
        }
        
        config = {**default_config, **kwargs}
        return tk.Label(parent, text="", **config)
    
    @staticmethod
    def help_text(parent, text, theme, **kwargs):
        """Texte d'aide sous un champ"""
        default_config = {
            'font': (FONT_FAMILY, 8),
            'bg': theme['bg_secondary'],
            'fg': theme['text_secondary'],
            'anchor': 'w'
        }
        
        config = {**default_config, **kwargs}
        return tk.Label(parent, text=text, **config)


class Card:
    """Composant Card (conteneur avec style)"""
    
    def __init__(self, parent, theme, **kwargs):
        """
        Initialise une card
        
        Args:
            parent: Widget parent
            theme (dict): Thème de l'application
            **kwargs: Arguments supplémentaires
        """
        default_config = {
            'bg': theme['bg_secondary'],
            'relief': 'flat',
            'highlightthickness': 1,
            'highlightbackground': theme['border']
        }
        
        config = {**default_config, **kwargs}
        self.frame = tk.Frame(parent, **config)
        self.theme = theme
    
    def pack(self, **kwargs):
        """Pack la card"""
        self.frame.pack(**kwargs)
        return self.frame
    
    def grid(self, **kwargs):
        """Grid la card"""
        self.frame.grid(**kwargs)
        return self.frame


class Separator:
    """Composant Separator (ligne de séparation)"""
    
    @staticmethod
    def horizontal(parent, theme, **kwargs):
        """Séparateur horizontal"""
        default_config = {
            'bg': theme['border'],
            'height': 1
        }
        
        config = {**default_config, **kwargs}
        return tk.Frame(parent, **config)


class FormField:
    """Composant FormField complet (label + input + help)"""
    
    def __init__(self, parent, label_text, theme, icon="", help_text="", input_type="text"):
        """
        Initialise un champ de formulaire complet
        
        Args:
            parent: Widget parent
            label_text (str): Texte du label (ajouter " *" pour champ obligatoire)
            theme (dict): Thème de l'application
            icon (str): Icône optionnelle
            help_text (str): Texte d'aide optionnel
            input_type (str): 'text' ou 'password'
        """
        self.container = tk.Frame(parent, bg=theme['bg_secondary'])
        self.theme = theme
        
        # Label avec astérisque rouge automatique
        label_frame = Label.field_label(self.container, label_text, theme, icon=icon)
        label_frame.pack(fill='x', pady=(0, 8))
        
        # Input avec frame pour la bordure
        input_frame = tk.Frame(self.container, bg=theme['input_bg'], relief='solid', borderwidth=1)
        input_frame.pack(fill='x')
        
        if input_type == "password":
            self.input = Input.password(input_frame, theme, relief='flat', borderwidth=0)
        else:
            self.input = Input.text(input_frame, theme, relief='flat', borderwidth=0)
        
        self.input.pack(fill='x', ipady=10, padx=8)
        
        # Help text
        if help_text:
            help_label = Label.help_text(self.container, help_text, theme)
            help_label.pack(anchor='w', pady=(5, 0))
    
    def pack(self, **kwargs):
        """Pack le champ"""
        self.container.pack(**kwargs)
        return self.container
    
    def get(self):
        """Récupère la valeur de l'input"""
        return self.input.get()
    
    def set(self, value):
        """Définit la valeur de l'input"""
        self.input.delete(0, tk.END)
        self.input.insert(0, value)
    
    def clear(self):
        """Vide l'input"""
        self.input.delete(0, tk.END)