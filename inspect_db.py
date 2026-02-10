import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from src.utils.db_connection import get_db_connection

conn = get_db_connection()
cursor = conn.cursor()

# Récupérer la structure de la table accounts
cursor.execute("PRAGMA table_info(accounts)")
columns = cursor.fetchall()

print("Structure de la table 'accounts':")
print("-" * 60)
for col in columns:
    print(f"Colonne: {col[1]}, Type: {col[2]}, Obligatoire: {col[3]}, Défaut: {col[4]}")

print("\n" + "=" * 60)
print("Tous les comptes:")
print("=" * 60)

cursor.execute("SELECT * FROM accounts")
accounts = cursor.fetchall()

if accounts:
    for row in accounts:
        print(row)
else:
    print("Aucun compte trouvé")

conn.close()
