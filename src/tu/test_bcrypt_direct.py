import sys
from pathlib import Path

# Ajouter le répertoire racine du projet au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from test_bcrypt import analyze_account

if __name__ == "__main__":
    print("Test direct - Analyse des comptes:\n")
    analyze_account()
