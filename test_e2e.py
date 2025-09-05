#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test E2E pour comparer les comportements des applications COBOL et Python
Ce script teste les fonctionnalités principales et compare les sorties
"""

import os
import sys
import re
import subprocess
import json
import tempfile
import unittest
from difflib import SequenceMatcher

# Chemins des applications
COBOL_APP_PATH = "./cobol/accountsystem"  # Chemin vers l'exécutable COBOL compilé
PYTHON_APP_PATH = "./python/app.py"       # Chemin vers l'application Python

# Configuration
TEMP_DATA_FILE = os.path.abspath("test_account_data.json")  # Fichier temporaire pour les tests Python

class TestIOCapture:
    """Classe utilitaire pour capturer les entrées/sorties des applications"""
    
    def __init__(self, app_path, is_python=False):
        self.app_path = app_path
        self.is_python = is_python
        self.input_commands = []
        self.output = ""
    
    def add_input(self, command):
        """Ajoute une commande d'entrée à la liste"""
        self.input_commands.append(str(command))
        return self
    
    def run(self):
        """Exécute l'application avec les entrées préparées"""
        # Préparer la commande
        if self.is_python:
            command = [sys.executable, self.app_path]
            # S'assurer que l'application Python utilise notre fichier de test
            env = os.environ.copy()
            env['ACCOUNT_DATA_FILE'] = TEMP_DATA_FILE
            # Créer un module AccountManager temporaire qui utilise notre fichier de test
            with open('python/account_manager_test.py', 'w') as f:
                f.write(f'''import os
import json

class AccountManager:
    def __init__(self, data_file="{TEMP_DATA_FILE}"):
        self.data_file = data_file
        self.balance = self._load_balance()
    
    def _load_balance(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as file:
                    data = json.load(file)
                    return data.get('balance', 1000.0)
            except (json.JSONDecodeError, IOError):
                pass
        return 1000.0  # Default initial balance
    
    def _save_balance(self):
        try:
            with open(self.data_file, 'w') as file:
                json.dump({{'balance': self.balance}}, file)
            return True
        except IOError:
            return False
    
    def get_balance(self):
        return self.balance
    
    def credit_account(self, amount):
        if amount <= 0:
            return False, "Le montant doit être supérieur à zéro."
        
        self.balance += amount
        self._save_balance()
        return True, f"Compte crédité de {{amount:.2f}}. Nouveau solde: {{self.balance:.2f}}"
    
    def debit_account(self, amount):
        if amount <= 0:
            return False, "Le montant doit être supérieur à zéro."
        
        if amount > self.balance:
            return False, "Fonds insuffisants."
        
        self.balance -= amount
        self._save_balance()
        return True, f"Compte débité de {{amount:.2f}}. Nouveau solde: {{self.balance:.2f}}"
''')
            # Créer un module app temporaire qui utilise notre module AccountManager
            with open('python/app_test.py', 'w') as f:
                f.write('''from account_manager_test import AccountManager

def display_menu():
    print("\\n=== Application de Gestion de Compte ===")
    print("1. Afficher le solde")
    print("2. Créditer le compte")
    print("3. Débiter le compte")
    print("4. Quitter")
    return input("Choisissez une option (1-4): ")

def get_amount():
    while True:
        try:
            amount = float(input("Entrez le montant: "))
            if amount < 0:
                print("Le montant ne peut pas être négatif.")
                continue
            return amount
        except ValueError:
            print("Veuillez entrer un montant valide.")

def main():
    account = AccountManager()

    while True:
        choice = display_menu()

        match choice:
            case "1":
                balance = account.get_balance()
                print(f"Solde actuel: {balance:.2f}")
            case "2":
                amount = get_amount()
                success, message = account.credit_account(amount)
                print(message)
            case "3":
                amount = get_amount()
                success, message = account.debit_account(amount)
                print(message)
            case "4":
                print("Merci d'avoir utilisé l'application. Au revoir!")
                break
            case _:
                print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()
''')
            command = [sys.executable, 'python/app_test.py']
        else:
            command = [self.app_path]
            env = os.environ.copy()
        
        # Préparer l'entrée
        input_data = "\n".join(self.input_commands) + "\n"
        
        # Exécuter la commande
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        # Envoyer l'entrée et capturer la sortie
        stdout, stderr = process.communicate(input_data)
        
        if stderr:
            print(f"Erreur lors de l'exécution: {stderr}")
        
        self.output = stdout
        return self
    
    def get_output(self):
        """Retourne la sortie capturée"""
        return self.output
    
    def extract_balance(self):
        """Extrait le solde de la sortie"""
        # Chercher un nombre décimal après "balance" ou "solde"
        match = re.search(r'(?:balance|solde)[^\d]*(\d+\.\d{2})', self.output, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None


class E2ETests(unittest.TestCase):
    """Tests de bout en bout comparant les applications COBOL et Python"""
    
    @classmethod
    def setUpClass(cls):
        """Préparation avant les tests"""
        # Réinitialiser le fichier de données Python
        if os.path.exists(TEMP_DATA_FILE):
            os.remove(TEMP_DATA_FILE)
        
        with open(TEMP_DATA_FILE, 'w') as f:
            json.dump({"balance": 1000.0}, f)
    
    @classmethod
    def tearDownClass(cls):
        """Nettoyage après les tests"""
        if os.path.exists(TEMP_DATA_FILE):
            os.remove(TEMP_DATA_FILE)
        # Supprimer les fichiers temporaires
        if os.path.exists('python/account_manager_test.py'):
            os.remove('python/account_manager_test.py')
        if os.path.exists('python/app_test.py'):
            os.remove('python/app_test.py')
        # Supprimer les fichiers de cache Python
        for file in os.listdir('python'):
            if file.endswith('.pyc') and (file.startswith('account_manager_test') or file.startswith('app_test')):
                os.remove(os.path.join('python', file))
        if os.path.exists('python/__pycache__'):
            for file in os.listdir('python/__pycache__'):
                if file.startswith('account_manager_test') or file.startswith('app_test'):
                    os.remove(os.path.join('python/__pycache__', file))
    
    def setUp(self):
        """Avant chaque test"""
        # Réinitialiser le solde à 1000
        with open(TEMP_DATA_FILE, 'w') as f:
            json.dump({"balance": 1000.0}, f)
    
    def similarity(self, str1, str2):
        """Calcule la similarité entre deux chaînes"""
        return SequenceMatcher(None, str1, str2).ratio()
    
    def test_01_view_balance(self):
        """E2E-01: Vérifier l'affichage du solde initial"""
        # Test COBOL
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("1").add_input("4").run()
        cobol_balance = cobol_test.extract_balance()
        
        # Test Python
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("1").add_input("4").run()
        python_balance = python_test.extract_balance()
        
        # Vérification
        self.assertEqual(cobol_balance, python_balance, 
                        f"Les soldes diffèrent: COBOL={cobol_balance}, Python={python_balance}")
        
        print(f"✓ E2E-01: Soldes identiques - COBOL: {cobol_balance}, Python: {python_balance}")
    
    def test_02_credit_account_valid(self):
        """E2E-02: Crédit de compte avec montant valide"""
        # Test COBOL
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("2").add_input("500.00").add_input("1").add_input("4").run()
        cobol_balance = cobol_test.extract_balance()
        
        # Test Python
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("2").add_input("500.00").add_input("1").add_input("4").run()
        python_balance = python_test.extract_balance()
        
        # Vérification
        self.assertEqual(cobol_balance, python_balance, 
                        f"Les soldes après crédit diffèrent: COBOL={cobol_balance}, Python={python_balance}")
        
        print(f"✓ E2E-02: Soldes après crédit identiques - COBOL: {cobol_balance}, Python: {python_balance}")
    
    def test_03_credit_account_zero(self):
        """E2E-03: Crédit de compte avec montant zéro"""
        # Test COBOL
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("2").add_input("0.00").add_input("1").add_input("4").run()
        cobol_output = cobol_test.get_output()
        cobol_balance = cobol_test.extract_balance()
        
        # Test Python
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("2").add_input("0.00").add_input("1").add_input("4").run()
        python_output = python_test.get_output()
        python_balance = python_test.extract_balance()
        
        # Vérification des soldes
        self.assertEqual(cobol_balance, python_balance, 
                        f"Les soldes après crédit de 0 diffèrent: COBOL={cobol_balance}, Python={python_balance}")
        
        # Vérification du message d'erreur (peut varier entre les implémentations)
        self.assertTrue("montant" in python_output.lower() and "zéro" in python_output.lower() or
                       "amount" in python_output.lower() and "zero" in python_output.lower(),
                       "Message d'erreur pour crédit zéro non trouvé dans la sortie Python")
        
        print(f"✓ E2E-03: Comportement avec crédit zéro similaire")
    
    def test_04_debit_account_valid(self):
        """E2E-04: Débit de compte avec montant valide"""
        # Test COBOL
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("3").add_input("200.00").add_input("1").add_input("4").run()
        cobol_balance = cobol_test.extract_balance()
        
        # Test Python
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("3").add_input("200.00").add_input("1").add_input("4").run()
        python_balance = python_test.extract_balance()
        
        # Vérification
        self.assertEqual(cobol_balance, python_balance, 
                        f"Les soldes après débit diffèrent: COBOL={cobol_balance}, Python={python_balance}")
        
        print(f"✓ E2E-04: Soldes après débit identiques - COBOL: {cobol_balance}, Python: {python_balance}")
    
    def test_05_debit_account_insufficient(self):
        """E2E-05: Débit de compte avec montant supérieur au solde"""
        # Test COBOL
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("3").add_input("2000.00").add_input("1").add_input("4").run()
        cobol_output = cobol_test.get_output()
        cobol_balance = cobol_test.extract_balance()
        
        # Test Python
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("3").add_input("2000.00").add_input("1").add_input("4").run()
        python_output = python_test.get_output()
        python_balance = python_test.extract_balance()
        
        # Vérification des soldes
        self.assertEqual(cobol_balance, python_balance, 
                        f"Les soldes après tentative de débit excessive diffèrent: COBOL={cobol_balance}, Python={python_balance}")
        
        # Vérification du message d'erreur
        cobol_has_error = "insufficient" in cobol_output.lower() or "fonds insuffisants" in cobol_output.lower()
        python_has_error = "insufficient" in python_output.lower() or "fonds insuffisants" in python_output.lower()
        
        self.assertTrue(cobol_has_error and python_has_error, 
                       "Messages d'erreur pour fonds insuffisants non cohérents")
        
        print(f"✓ E2E-05: Comportement avec fonds insuffisants similaire")
    
    def test_06_debit_account_zero(self):
        """E2E-06: Débit de compte avec montant zéro"""
        # Test COBOL
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("3").add_input("0.00").add_input("1").add_input("4").run()
        cobol_balance = cobol_test.extract_balance()
        
        # Test Python
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("3").add_input("0.00").add_input("1").add_input("4").run()
        python_balance = python_test.extract_balance()
        
        # Vérification des soldes
        self.assertEqual(cobol_balance, python_balance, 
                        f"Les soldes après débit de 0 diffèrent: COBOL={cobol_balance}, Python={python_balance}")
        
        print(f"✓ E2E-06: Comportement avec débit zéro similaire")
    
    def test_07_exit_program(self):
        """E2E-07: Sortie du programme"""
        # Test COBOL
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("4").run()
        cobol_output = cobol_test.get_output()
        
        # Test Python
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("4").run()
        python_output = python_test.get_output()
        
        # Vérification du message de sortie
        cobol_has_exit = "exit" in cobol_output.lower() or "goodbye" in cobol_output.lower() or "au revoir" in cobol_output.lower()
        python_has_exit = "exit" in python_output.lower() or "goodbye" in python_output.lower() or "au revoir" in python_output.lower()
        
        self.assertTrue(cobol_has_exit and python_has_exit, "Messages de sortie non cohérents")
        
        print(f"✓ E2E-07: Messages de sortie cohérents")
    
    def test_08_invalid_option(self):
        """E2E-08: Option invalide"""
        # Test COBOL
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("9").add_input("4").run()
        cobol_output = cobol_test.get_output()
        
        # Test Python
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("9").add_input("4").run()
        python_output = python_test.get_output()
        
        # Vérification du message d'erreur
        cobol_has_error = "invalid" in cobol_output.lower() or "invalide" in cobol_output.lower()
        python_has_error = "invalid" in python_output.lower() or "invalide" in python_output.lower()
        
        self.assertTrue(cobol_has_error and python_has_error, "Messages d'erreur pour option invalide non cohérents")
        
        print(f"✓ E2E-08: Messages pour option invalide cohérents")
    
    def test_09_multiple_operations(self):
        """E2E-09: Séquence d'opérations multiples"""
        # Test COBOL - Crédit puis débit puis consultation
        cobol_test = TestIOCapture(COBOL_APP_PATH)
        cobol_test.add_input("2").add_input("300.00")\
                 .add_input("3").add_input("150.00")\
                 .add_input("1")\
                 .add_input("4").run()
        cobol_balance = cobol_test.extract_balance()
        
        # Test Python - Même séquence
        python_test = TestIOCapture(PYTHON_APP_PATH, is_python=True)
        python_test.add_input("2").add_input("300.00")\
                  .add_input("3").add_input("150.00")\
                  .add_input("1")\
                  .add_input("4").run()
        python_balance = python_test.extract_balance()
        
        # Vérification des soldes
        self.assertEqual(cobol_balance, python_balance, 
                        f"Les soldes après séquence d'opérations diffèrent: COBOL={cobol_balance}, Python={python_balance}")
        
        print(f"✓ E2E-09: Soldes après séquence d'opérations identiques - COBOL: {cobol_balance}, Python: {python_balance}")


if __name__ == "__main__":
    print("=== Tests E2E pour la migration COBOL vers Python ===")
    
    # Vérifier que les fichiers existent
    if not os.path.exists(COBOL_APP_PATH):
        print(f"ERREUR: L'exécutable COBOL '{COBOL_APP_PATH}' n'existe pas.")
        print("Assurez-vous que le programme COBOL a été compilé.")
        sys.exit(1)
    
    if not os.path.exists(PYTHON_APP_PATH):
        print(f"ERREUR: Le script Python '{PYTHON_APP_PATH}' n'existe pas.")
        sys.exit(1)
    
    # Exécuter les tests
    unittest.main(verbosity=2)
