#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script d'exécution de tous les tests pour la migration COBOL vers Python
Ce script exécute les tests unitaires et les tests E2E
"""

import os
import sys
import unittest
import argparse

def run_tests(e2e=True, unit=True):
    """Exécute les tests spécifiés"""
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()

    # Ajouter les tests unitaires si demandé
    if unit:
        print("\n=== Exécution des tests unitaires ===\n")
        # Tester AccountManager
        if os.path.exists('test_account_manager.py'):
            account_tests = test_loader.discover('.', pattern='test_account_manager.py')
            test_suite.addTest(account_tests)

        # Tester app.py
        if os.path.exists('test_app.py'):
            app_tests = test_loader.discover('.', pattern='test_app.py')
            test_suite.addTest(app_tests)

    # Ajouter les tests E2E si demandé
    if e2e:
        print("\n=== Exécution des tests End-to-End ===\n")
        if os.path.exists('test_e2e.py'):
            e2e_tests = test_loader.discover('.', pattern='test_e2e.py')
            test_suite.addTest(e2e_tests)

    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(test_suite)

def compile_cobol_if_needed():
    """Compile les programmes COBOL si nécessaire"""
    # Vérifier si l'exécutable existe déjà
    if os.path.exists('cobol/accountsystem'):
        return True

    print("\n=== Compilation des programmes COBOL ===\n")

    # Vérifier que GnuCOBOL est installé
    import subprocess
    try:
        subprocess.run(['cobc', '--version'],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.PIPE,
                       check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("ERREUR: GnuCOBOL n'est pas installé ou n'est pas accessible.")
        print("Veuillez installer GnuCOBOL pour exécuter les tests E2E.")
        return False

    # Compiler les programmes COBOL
    try:
        subprocess.run(['cobc', '-x', '-o', 'cobol/accountsystem',
                        'cobol/main.cob', 'cobol/operations.cob', 'cobol/data.cob'],
                       check=True)
        print("Compilation COBOL réussie.")
        return True
    except subprocess.SubprocessError as e:
        print(f"ERREUR: Échec de la compilation COBOL: {e}")
        return False

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Exécution des tests pour la migration COBOL vers Python")
    parser.add_argument('--unit-only', action='store_true', help="Exécuter uniquement les tests unitaires")
    parser.add_argument('--e2e-only', action='store_true', help="Exécuter uniquement les tests E2E")
    args = parser.parse_args()

    # Déterminer quels tests exécuter
    run_unit = not args.e2e_only
    run_e2e = not args.unit_only

    # Compiler le COBOL si nécessaire pour les tests E2E
    if run_e2e and not compile_cobol_if_needed():
        print("Les tests E2E seront ignorés en raison de l'échec de la compilation COBOL.")
        run_e2e = False

    # Exécuter les tests
    result = run_tests(e2e=run_e2e, unit=run_unit)

    # Afficher un résumé
    print("\n=== Résumé des Tests ===")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Succès: {result.testsRun - len(result.errors) - len(result.failures)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")

    # Retourner un code d'erreur si des tests ont échoué
    if result.failures or result.errors:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
