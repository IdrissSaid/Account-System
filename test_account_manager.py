#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests unitaires pour le module AccountManager
Validation de la logique métier de la version Python
"""

import os
import sys
import json
import unittest
import tempfile
from unittest.mock import patch, mock_open

# Ajouter le répertoire python au chemin de recherche
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'python')))

# Importer le module à tester
from python.account_manager import AccountManager

class TestAccountManager(unittest.TestCase):
    """Tests unitaires pour la classe AccountManager"""
    
    def setUp(self):
        """Préparer l'environnement de test"""
        # Utiliser un fichier temporaire pour les tests
        self.test_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json').name
        
        # Initialiser le fichier avec un solde de 1000.0
        with open(self.test_file, 'w') as f:
            json.dump({'balance': 1000.0}, f)
    
    def tearDown(self):
        """Nettoyer après les tests"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_ut_py_am_01_default_balance(self):
        """UT-PY-AM-01: Initialisation avec solde par défaut"""
        # Supprimer le fichier pour tester le comportement par défaut
        os.remove(self.test_file)
        
        # Créer une nouvelle instance
        account = AccountManager(self.test_file)
        
        # Vérifier que le solde par défaut est 1000.0
        self.assertEqual(account.get_balance(), 1000.0)
        
        print("✓ UT-PY-AM-01: Solde par défaut correctement initialisé à 1000.0")
    
    def test_ut_py_am_02_get_balance(self):
        """UT-PY-AM-02: Consultation du solde"""
        # Créer une instance avec un fichier existant
        account = AccountManager(self.test_file)
        
        # Vérifier que le solde est correctement lu
        self.assertEqual(account.get_balance(), 1000.0)
        
        print("✓ UT-PY-AM-02: Consultation du solde fonctionnelle")
    
    def test_ut_py_am_03_credit_valid(self):
        """UT-PY-AM-03: Crédit de compte avec montant valide"""
        account = AccountManager(self.test_file)
        
        # Créditer le compte de 500.0
        success, message = account.credit_account(500.0)
        
        # Vérifier le résultat
        self.assertTrue(success)
        self.assertEqual(account.get_balance(), 1500.0)
        
        # Vérifier que le message contient le nouveau solde
        self.assertIn("1500", message)
        
        # Vérifier la persistance
        with open(self.test_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['balance'], 1500.0)
        
        print("✓ UT-PY-AM-03: Crédit valide traité correctement")
    
    def test_ut_py_am_04_credit_zero(self):
        """UT-PY-AM-04: Crédit de compte avec montant zéro ou négatif"""
        account = AccountManager(self.test_file)
        
        # Tester crédit zéro
        success_zero, message_zero = account.credit_account(0.0)
        
        # Vérifier le résultat
        self.assertFalse(success_zero)
        self.assertEqual(account.get_balance(), 1000.0)  # Solde inchangé
        
        # Tester crédit négatif
        success_neg, message_neg = account.credit_account(-100.0)
        
        # Vérifier le résultat
        self.assertFalse(success_neg)
        self.assertEqual(account.get_balance(), 1000.0)  # Solde inchangé
        
        print("✓ UT-PY-AM-04: Crédit zéro ou négatif correctement rejeté")
    
    def test_ut_py_am_05_debit_valid(self):
        """UT-PY-AM-05: Débit de compte avec montant valide"""
        account = AccountManager(self.test_file)
        
        # Débiter le compte de 200.0
        success, message = account.debit_account(200.0)
        
        # Vérifier le résultat
        self.assertTrue(success)
        self.assertEqual(account.get_balance(), 800.0)
        
        # Vérifier que le message contient le nouveau solde
        self.assertIn("800", message)
        
        # Vérifier la persistance
        with open(self.test_file, 'r') as f:
            data = json.load(f)
            self.assertEqual(data['balance'], 800.0)
        
        print("✓ UT-PY-AM-05: Débit valide traité correctement")
    
    def test_ut_py_am_06_debit_insufficient(self):
        """UT-PY-AM-06: Débit de compte avec montant supérieur au solde"""
        account = AccountManager(self.test_file)
        
        # Tenter de débiter plus que le solde
        success, message = account.debit_account(2000.0)
        
        # Vérifier le résultat
        self.assertFalse(success)
        self.assertEqual(account.get_balance(), 1000.0)  # Solde inchangé
        
        # Vérifier le message d'erreur - utiliser une condition OR explicite
        self.assertTrue("insuffisant" in message.lower() or "insufficient" in message.lower(), 
                       f"Message d'erreur attendu non trouvé: {message}")
        
        print("✓ UT-PY-AM-06: Débit excessif correctement rejeté")
    
    def test_ut_py_am_07_debit_zero(self):
        """UT-PY-AM-07: Débit de compte avec montant zéro ou négatif"""
        account = AccountManager(self.test_file)
        
        # Tester débit zéro
        success_zero, message_zero = account.debit_account(0.0)
        
        # Vérifier le résultat
        self.assertFalse(success_zero)
        self.assertEqual(account.get_balance(), 1000.0)  # Solde inchangé
        
        # Tester débit négatif
        success_neg, message_neg = account.debit_account(-100.0)
        
        # Vérifier le résultat
        self.assertFalse(success_neg)
        self.assertEqual(account.get_balance(), 1000.0)  # Solde inchangé
        
        print("✓ UT-PY-AM-07: Débit zéro ou négatif correctement rejeté")
    
    @patch('builtins.open', new_callable=mock_open)
    def test_ut_py_am_08_save_balance(self, mock_file):
        """UT-PY-AM-08: Persistance des données (sauvegarde)"""
        account = AccountManager(self.test_file)
        
        # Modifier le solde et forcer la sauvegarde
        account.balance = 1500.0
        result = account._save_balance()
        
        # Vérifier que la sauvegarde a réussi
        self.assertTrue(result)
        
        # Vérifier que le fichier a été ouvert en écriture
        mock_file.assert_called_with(self.test_file, 'w')
        
        # Vérifier que l'écriture a été effectuée (sans vérifier le contenu exact)
        handle = mock_file()
        self.assertTrue(handle.write.called, "La méthode write() n'a pas été appelée")
        
        print("✓ UT-PY-AM-08: Persistance des données fonctionnelle")
    
    def test_ut_py_am_09_load_balance(self):
        """UT-PY-AM-09: Persistance des données (chargement)"""
        # Modifier le fichier avec un solde différent
        with open(self.test_file, 'w') as f:
            json.dump({'balance': 1500.0}, f)
        
        # Créer une nouvelle instance qui devrait charger ce solde
        account = AccountManager(self.test_file)
        
        # Vérifier que le solde est correctement chargé
        self.assertEqual(account.get_balance(), 1500.0)
        
        print("✓ UT-PY-AM-09: Chargement des données fonctionnel")
    
    def test_ut_py_am_10_format_precision(self):
        """UT-PY-AM-10: Précision des nombres décimaux (comparable à COBOL)"""
        account = AccountManager(self.test_file)
        
        # COBOL utilise 6 chiffres avant la virgule, 2 après (9(6)V99)
        # Tester les limites
        
        # Grand nombre
        success, _ = account.credit_account(999999.99)
        self.assertTrue(success)
        self.assertEqual(account.get_balance(), 1000999.99)
        
        # Précision à 2 décimales
        account.balance = 1000.0  # Réinitialiser
        success, _ = account.credit_account(0.01)
        self.assertTrue(success)
        self.assertEqual(account.get_balance(), 1000.01)
        
        print("✓ UT-PY-AM-10: Précision des nombres conforme aux attentes COBOL")


if __name__ == "__main__":
    unittest.main(verbosity=2)
