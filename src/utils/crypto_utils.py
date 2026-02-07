"""crypto_utils

Gestion du chiffrement Fernet pour secrets. La clé est générée au premier
lancement et sauvegardée dans `configs/.secret.key`. À chaque démarrage,
elle est chargée en mémoire et utilisée pour toutes les opérations de
chiffrement/déchiffrement.

À l'avenir : revoir le stockage de la clé (SSL/TLS ou autre).
"""
import os
import json
from cryptography.fernet import Fernet

# Chemins
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_DIR = os.path.normpath(os.path.join(BASE_DIR, '..', 'configs'))
CONFIG_PLAIN = os.path.join(CONFIG_DIR, 'app_config.json')
CONFIG_ENC = CONFIG_PLAIN + '.enc'
SECRET_KEY_FILE = os.path.join(CONFIG_DIR, '.secret.key')

# Cache en mémoire pour la clé
_fernet_cache = None


def _init_fernet():
    """Initialise ou charge la clé Fernet depuis le fichier .secret.key.
    Si le fichier n'existe pas, génère une nouvelle clé et la sauvegarde.
    """
    global _fernet_cache
    if _fernet_cache is not None:
        return _fernet_cache

    # Créer le répertoire configs s'il n'existe pas
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # Vérifier si le fichier .secret.key existe
    if os.path.exists(SECRET_KEY_FILE):
        try:
            with open(SECRET_KEY_FILE, 'rb') as f:
                key = f.read()
            _fernet_cache = Fernet(key)
            return _fernet_cache
        except Exception as e:
            raise RuntimeError(f"Impossible de charger la clé Fernet : {e}")

    # Générer une nouvelle clé
    key = Fernet.generate_key()
    try:
        with open(SECRET_KEY_FILE, 'wb') as f:
            f.write(key)
        # Restreindre les permissions (Unix-like)
        try:
            os.chmod(SECRET_KEY_FILE, 0o600)
        except Exception:
            pass
        _fernet_cache = Fernet(key)
        return _fernet_cache
    except Exception as e:
        raise RuntimeError(f"Impossible de générer/sauvegarder la clé Fernet : {e}")


def _read_plain_config():
    if not os.path.exists(CONFIG_PLAIN):
        return {}
    try:
        with open(CONFIG_PLAIN, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def read_config():
    """Lit la configuration depuis app_config.json ou app_config.json.enc
    (si existant). Ne fait QUE lire, pas d'écriture.
    """
    fernet = _init_fernet()
    if os.path.exists(CONFIG_ENC):
        try:
            with open(CONFIG_ENC, 'rb') as f:
                token = f.read()
            data = fernet.decrypt(token)
            return json.loads(data.decode('utf-8'))
        except Exception:
            pass

    # fallback plain
    return _read_plain_config()


def write_config(cfg):
    """Écrit la configuration chiffrée dans app_config.json.enc
    avec la clé conservée en mémoire.
    """
    fernet = _init_fernet()
    try:
        os.makedirs(CONFIG_DIR, exist_ok=True)
        data = json.dumps(cfg, indent=2).encode('utf-8')
        token = fernet.encrypt(data)
        with open(CONFIG_ENC, 'wb') as f:
            f.write(token)
        # Nettoyer le fichier plaintext s'il existe
        try:
            if os.path.exists(CONFIG_PLAIN):
                os.remove(CONFIG_PLAIN)
        except Exception:
            pass
        return True
    except Exception:
        return False


def encrypt_secret(secret: str) -> str:
    """Chiffre un secret avec la clé Fernet en mémoire."""
    fernet = _init_fernet()
    token = fernet.encrypt(secret.encode('utf-8'))
    return token.decode('utf-8')


def decrypt_secret(token: str) -> str:
    """Déchiffre un secret avec la clé Fernet en mémoire."""
    fernet = _init_fernet()
    try:
        data = fernet.decrypt(token.encode('utf-8'))
        return data.decode('utf-8')
    except Exception:
        return ''
