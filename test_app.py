#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Tests unitaires pour l'application principale (app.py)
Validation des fonctions d'interface utilisateur
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

# Ajouter le répertoire python au chemin de recherche
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'python')))

# Importer les modules à tester
from python.app import display_menu, get_amount, main

class TestApp(unittest.TestCase):
    """Tests unitaires pour l'application principale"""
    
    def test_ut_py_app_01_display_menu(self):
        """UT-PY-APP-01: Affichage du menu"""
        with patch('builtins.input', return_value="1") as mock_input:
            with patch('builtins.print') as mock_print:
                result = display_menu()
        
        # Vérifier que la fonction retourne bien l'entrée utilisateur
        self.assertEqual(result, "1")
        
        # Vérifier que le menu est affiché avec toutes les options
        # On ne peut pas facilement vérifier les appels exacts à print,
        # mais on peut vérifier qu'il a été appelé au moins 5 fois (4 options + en-tête)
        self.assertGreaterEqual(mock_print.call_count, 5)
        
        print("✓ UT-PY-APP-01: Affichage du menu fonctionnel")
    
    def test_ut_py_app_02_get_amount_valid(self):
        """UT-PY-APP-02: Saisie du montant (valide)"""
        with patch('builtins.input', return_value="100.00"):
            result = get_amount()
        
        # Vérifier que la fonction retourne bien le montant converti
        self.assertEqual(result, 100.00)
        
        print("✓ UT-PY-APP-02: Saisie de montant valide fonctionnelle")
    
    def test_ut_py_app_03_get_amount_invalid_then_valid(self):
        """UT-PY-APP-03: Saisie du montant (invalide puis valide)"""
        # Simuler une entrée invalide suivie d'une entrée valide
        with patch('builtins.input', side_effect=["abc", "100.00"]):
            with patch('builtins.print') as mock_print:
                result = get_amount()
        
        # Vérifier que la fonction retourne bien le montant valide final
        self.assertEqual(result, 100.00)
        
        # Vérifier qu'un message d'erreur a été affiché
        mock_print.assert_called_with("Veuillez entrer un montant valide.")
        
        print("✓ UT-PY-APP-03: Rejet de saisie invalide fonctionnel")
    
    def test_ut_py_app_04_get_amount_negative_then_valid(self):
        """UT-PY-APP-04: Saisie du montant (négatif puis valide)"""
        # Simuler une entrée négative suivie d'une entrée valide
        with patch('builtins.input', side_effect=["-50.00", "100.00"]):
            with patch('builtins.print') as mock_print:
                result = get_amount()
        
        # Vérifier que la fonction retourne bien le montant valide final
        self.assertEqual(result, 100.00)
        
        # Vérifier qu'un message d'erreur a été affiché
        mock_print.assert_called_with("Le montant ne peut pas être négatif.")
        
        print("✓ UT-PY-APP-04: Rejet de montant négatif fonctionnel")
    
    @patch('python.app.AccountManager')
    def test_ut_py_app_05_option_view_balance(self, mock_account_manager):
        """UT-PY-APP-05: Traitement option 1 (consultation)"""
        # Configurer le mock pour simuler un solde
        mock_instance = mock_account_manager.return_value
        mock_instance.get_balance.return_value = 1000.0
        
        # Simuler l'exécution avec l'option 1 puis 4 (quitter)
        with patch('builtins.input', side_effect=["1", "4"]):
            with patch('builtins.print') as mock_print:
                main()
        
        # Vérifier que get_balance a été appelé
        mock_instance.get_balance.assert_called_once()
        
        print("✓ UT-PY-APP-05: Option consultation du solde fonctionnelle")
    
    @patch('python.app.AccountManager')
    @patch('python.app.get_amount', return_value=500.0)
    def test_ut_py_app_06_option_credit(self, mock_get_amount, mock_account_manager):
        """UT-PY-APP-06: Traitement option 2 (crédit)"""
        # Configurer le mock pour simuler un crédit
        mock_instance = mock_account_manager.return_value
        mock_instance.credit_account.return_value = (True, "Compte crédité de 500.00. Nouveau solde: 1500.00")
        
        # Simuler l'exécution avec l'option 2 puis 4 (quitter)
        with patch('builtins.input', side_effect=["2", "4"]):
            with patch('builtins.print') as mock_print:
                main()
        
        # Vérifier que credit_account a été appelé
        mock_instance.credit_account.assert_called_once_with(500.0)
        
        print("✓ UT-PY-APP-06: Option crédit du compte fonctionnelle")
    
    @patch('python.app.AccountManager')
    @patch('python.app.get_amount', return_value=200.0)
    def test_ut_py_app_07_option_debit(self, mock_get_amount, mock_account_manager):
        """UT-PY-APP-07: Traitement option 3 (débit)"""
        # Configurer le mock pour simuler un débit
        mock_instance = mock_account_manager.return_value
        mock_instance.debit_account.return_value = (True, "Compte débité de 200.00. Nouveau solde: 800.00")
        
        # Simuler l'exécution avec l'option 3 puis 4 (quitter)
        with patch('builtins.input', side_effect=["3", "4"]):
            with patch('builtins.print') as mock_print:
                main()
        
        # Vérifier que debit_account a été appelé
        mock_instance.debit_account.assert_called_once_with(200.0)
        
        print("✓ UT-PY-APP-07: Option débit du compte fonctionnelle")
    
    @patch('python.app.AccountManager')
    def test_ut_py_app_08_option_exit(self, mock_account_manager):
        """UT-PY-APP-08: Traitement option 4 (sortie)"""
        # Simuler l'exécution avec l'option 4 (quitter)
        with patch('builtins.input', return_value="4"):
            with patch('builtins.print') as mock_print:
                main()
        
        # Vérifier que le message de sortie est affiché
        mock_print.assert_called_with("Merci d'avoir utilisé l'application. Au revoir!")
        
        print("✓ UT-PY-APP-08: Option sortie fonctionnelle")
    
    @patch('python.app.AccountManager')
    def test_ut_py_app_09_invalid_option(self, mock_account_manager):
        """UT-PY-APP-09: Traitement option invalide"""
        # Simuler l'exécution avec une option invalide puis 4 (quitter)
        with patch('builtins.input', side_effect=["9", "4"]):
            with patch('builtins.print') as mock_print:
                main()
        
        # Vérifier que le message d'erreur est affiché
        mock_print.assert_any_call("Option invalide. Veuillez réessayer.")
        
        print("✓ UT-PY-APP-09: Rejet d'option invalide fonctionnel")


if __name__ == "__main__":
    unittest.main(verbosity=2)
