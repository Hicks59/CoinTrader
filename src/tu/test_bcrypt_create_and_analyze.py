import sys
from pathlib import Path

# Ajouter le répertoire racine du projet au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from test_bcrypt import create_test_account, analyze_account

if __name__ == "__main__":
    print("Création d'un compte de test...\n")
    create_test_account()
    
    print("\n" + "="*60)
    print("Analyse des comptes:\n")
    analyze_account()
