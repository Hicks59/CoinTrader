import bcrypt
import sqlite3
from datetime import datetime
import time

def connect_with_retry(db_path, max_retries=3):
    """Tente de se connecter à la BDD avec retry"""
    for attempt in range(max_retries):
        try:
            conn = sqlite3.connect(db_path, timeout=10.0)
            return conn
        except sqlite3.OperationalError as e:
            if "locked" in str(e):
                if attempt < max_retries - 1:
                    print(f"⏳ BDD verrouillée, nouvelle tentative dans 2s... ({attempt + 1}/{max_retries})")
                    time.sleep(2)
                else:
                    raise Exception("❌ ERREUR: Base de données verrouillée!\n\n"
                                  "➡️ Fermez l'application Kipacoin et réessayez.\n"
                                  "➡️ Vérifiez qu'aucun processus Python ne tourne (Gestionnaire des tâches)")
            else:
                raise
    return None


def analyze_account():
    """Analyse le compte problématique"""
    print("=== ANALYSE COMPTE KIPACOIN ===\n")
    
    try:
        conn = connect_with_retry('datas/kipacoin.db')
        cursor = conn.cursor()
        
        # Récupérer tous les comptes
        cursor.execute("SELECT id, username, password_hash, email FROM accounts")
        accounts = cursor.fetchall()
        
        if not accounts:
            print("❌ Aucun compte trouvé dans la base")
            conn.close()
            return
        
        print(f"📊 {len(accounts)} compte(s) trouvé(s)\n")
        
        for account_id, username, password_hash, email in accounts:
            print(f"--- Compte: {username} (ID: {account_id}) ---")
            print(f"Email: {email}")
            print(f"Type hash: {type(password_hash)}")
            print(f"Longueur hash: {len(password_hash)} caractères")
            print(f"Hash complet: {password_hash}")
            
            # Vérifier si c'est un hash bcrypt valide
            is_valid_format = password_hash.startswith('$2b$') or password_hash.startswith('$2a$') or password_hash.startswith('$2y$')
            print(f"Format bcrypt valide: {'✅' if is_valid_format else '❌'}")
            
            if is_valid_format:
                print(f"Hash bcrypt détecté (commence par: {password_hash[:4]})")
            else:
                print("⚠️ PROBLÈME: Le hash ne ressemble pas à un hash bcrypt!")
                print("   Un hash bcrypt doit commencer par $2b$, $2a$ ou $2y$")
            
            print()
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def fix_account_password():
    """Corrige le mot de passe d'un compte"""
    print("\n=== CORRECTION MOT DE PASSE ===\n")
    
    try:
        conn = connect_with_retry('datas/kipacoin.db')
        cursor = conn.cursor()
        
        # Lister les comptes
        cursor.execute("SELECT id, username, email FROM accounts")
        accounts = cursor.fetchall()
        
        if not accounts:
            print("❌ Aucun compte à corriger")
            conn.close()
            return
        
        print("Comptes disponibles:")
        for account_id, username, email in accounts:
            print(f"  {account_id}. {username} ({email})")
        
        # Choisir le compte
        account_id = input("\nID du compte à corriger: ")
        
        cursor.execute("SELECT username FROM accounts WHERE id = ?", (account_id,))
        result = cursor.fetchone()
        
        if not result:
            print("❌ Compte introuvable")
            conn.close()
            return
        
        username = result[0]
        
        # Demander le nouveau mot de passe
        print(f"\n👤 Compte: {username}")
        new_password = input("Nouveau mot de passe: ")
        confirm_password = input("Confirmer le mot de passe: ")
        
        if new_password != confirm_password:
            print("❌ Les mots de passe ne correspondent pas")
            conn.close()
            return
        
        # Générer le hash correct
        print("\n⏳ Génération du hash bcrypt...")
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        password_hash_str = password_hash.decode('utf-8')
        
        print(f"✅ Hash généré: {password_hash_str[:30]}...")
        print(f"   Longueur: {len(password_hash_str)} caractères")
        
        # Mettre à jour la base
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(
            "UPDATE accounts SET password_hash = ?, updated_at = ? WHERE id = ?",
            (password_hash_str, current_time, account_id)
        )
        conn.commit()
        
        print(f"\n✅ Mot de passe mis à jour pour '{username}'")
        
        # Tester immédiatement
        print("\n--- TEST DE VÉRIFICATION ---")
        cursor.execute("SELECT password_hash FROM accounts WHERE id = ?", (account_id,))
        stored_hash = cursor.fetchone()[0]
        
        is_match = bcrypt.checkpw(new_password.encode('utf-8'), stored_hash.encode('utf-8'))
        
        if is_match:
            print("✅ SUCCÈS! Le mot de passe fonctionne correctement")
        else:
            print("❌ ÉCHEC! Le problème persiste")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def create_test_account():
    """Crée un compte de test avec un hash correct"""
    print("\n=== CRÉATION COMPTE DE TEST ===\n")
    
    try:
        conn = connect_with_retry('datas/kipacoin.db')
        cursor = conn.cursor()
        
        # Vérifier si le compte test existe
        cursor.execute("SELECT id FROM accounts WHERE username = 'test'")
        if cursor.fetchone():
            print("⚠️ Le compte 'test' existe déjà")
            delete = input("Voulez-vous le supprimer et le recréer? (o/n): ")
            if delete.lower() == 'o':
                cursor.execute("DELETE FROM accounts WHERE username = 'test'")
                conn.commit()
                print("✅ Compte 'test' supprimé")
            else:
                conn.close()
                return
        
        # Créer le compte test
        username = "test"
        password = "test123"
        email = "test@kipacoin.com"
        nom = "Test"
        prenom = "User"
        
        print(f"Création du compte:")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  Email: {email}")
        
        # Hasher le mot de passe
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_hash_str = password_hash.decode('utf-8')
        
        print(f"\n✅ Hash généré: {password_hash_str[:30]}...")
        
        # Insérer
        cursor.execute(
            """INSERT INTO accounts (username, password_hash, email, nom, prenom)
               VALUES (?, ?, ?, ?, ?)""",
            (username, password_hash_str, email, nom, prenom)
        )
        conn.commit()
        
        account_id = cursor.lastrowid
        print(f"✅ Compte créé (ID: {account_id})")
        
        # Tester immédiatement
        print("\n--- TEST DE VÉRIFICATION ---")
        cursor.execute("SELECT password_hash FROM accounts WHERE id = ?", (account_id,))
        stored_hash = cursor.fetchone()[0]
        
        is_match = bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))
        
        if is_match:
            print("✅ SUCCÈS! Le compte test fonctionne")
            print("\n💡 Essayez de vous connecter avec:")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
        else:
            print("❌ ÉCHEC! Problème de configuration")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erreur: {e}")


def main_menu():
    """Menu principal"""
    while True:
        print("\n" + "="*50)
        print("KIPACOIN - DIAGNOSTIC & CORRECTION BCRYPT")
        print("="*50)
        print("\n1. Analyser les comptes existants")
        print("2. Corriger le mot de passe d'un compte")
        print("3. Créer un compte de test")
        print("4. Quitter")
        
        choice = input("\nVotre choix: ")
        
        if choice == "1":
            analyze_account()
        elif choice == "2":
            fix_account_password()
        elif choice == "3":
            create_test_account()
        elif choice == "4":
            print("\n👋 Au revoir!")
            break
        else:
            print("❌ Choix invalide")


if __name__ == "__main__":
    main_menu()