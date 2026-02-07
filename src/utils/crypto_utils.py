"""
Utilitaires pour chiffrer/déchiffrer les secrets API avec Fernet
La clé est lue/écrite dans `configs/app_config.json` sous la clé `fernet_key`.
"""
import json
import os
from cryptography.fernet import Fernet

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'configs', 'app_config.json')
CONFIG_PATH = os.path.normpath(CONFIG_PATH)


def _read_config():
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def _write_config(cfg):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2)


def get_fernet():
    cfg = _read_config()
    key = cfg.get('fernet_key')
    if not key:
        # Générer et sauvegarder
        key_bytes = Fernet.generate_key()
        key = key_bytes.decode('utf-8')
        cfg['fernet_key'] = key
        try:
            _write_config(cfg)
        except Exception:
            pass
    else:
        key_bytes = key.encode('utf-8')
    return Fernet(key_bytes)


def encrypt_secret(secret: str) -> str:
    f = get_fernet()
    token = f.encrypt(secret.encode('utf-8'))
    return token.decode('utf-8')


def decrypt_secret(token: str) -> str:
    f = get_fernet()
    try:
        data = f.decrypt(token.encode('utf-8'))
        return data.decode('utf-8')
    except Exception:
        return ''
