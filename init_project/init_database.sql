-- KIPACOIN - Initialisation de la base de données

CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS exchanges (
    exchange_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_account_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    display_name TEXT NOT NULL,
    logo TEXT DEFAULT '💱',
    endpoint_url TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    UNIQUE(fk_account_id, name)
);

CREATE TABLE IF NOT EXISTS api_keys (
    api_key_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_account_id INTEGER NOT NULL,
    fk_exchange_id INTEGER NOT NULL,
    api_key TEXT NOT NULL,
    api_secret TEXT NOT NULL,
    api_passphrase TEXT,
    label TEXT,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_exchange_id) REFERENCES exchanges(exchange_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bots (
    bot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_account_id INTEGER NOT NULL,
    fk_exchange_id INTEGER NOT NULL,
    crypto_source TEXT NOT NULL,
    crypto_target TEXT NOT NULL,
    product_id TEXT NOT NULL,
    prix_achat_cible REAL,
    pourcentage_gain REAL NOT NULL,
    montant_trade REAL NOT NULL,
    type_ordre TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_exchange_id) REFERENCES exchanges(exchange_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bot_id INTEGER,
    fk_account_id INTEGER NOT NULL,
    fk_exchange_id INTEGER NOT NULL,
    product_id TEXT NOT NULL,
    type TEXT NOT NULL,
    prix_execution REAL,
    quantite REAL,
    montant_usdc REAL,
    frais REAL,
    status TEXT NOT NULL,
    order_id_exchange TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    executed_at TIMESTAMP,
    FOREIGN KEY (bot_id) REFERENCES bots(bot_id) ON DELETE SET NULL,
    FOREIGN KEY (fk_account_id) REFERENCES accounts(account_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_exchange_id) REFERENCES exchanges(exchange_id) ON DELETE CASCADE
);

INSERT OR IGNORE INTO exchanges (name, display_name, logo, endpoint_url) 
VALUES ('coinbase', 'Coinbase', '🟦', 'https://api.exchange.coinbase.com');

INSERT OR IGNORE INTO exchanges (name, display_name, logo, endpoint_url) 
VALUES ('binance', 'Binance', '🟨', 'https://api.binance.com');

INSERT OR IGNORE INTO exchanges (name, display_name, logo, endpoint_url) 
VALUES ('kraken', 'Kraken', '🟪', 'https://api.kraken.com');