# Stratégie de Tests pour la Migration COBOL vers Python

## Vue d'ensemble

Cette stratégie de tests vise à garantir que la migration du code COBOL vers Python maintient une parité fonctionnelle complète. La structure des tests suit une approche pyramidale :

1. **Tests Unitaires** : Validation de chaque fonction/module individuel
2. **Tests d'Intégration** : Validation des interactions entre modules 
3. **Tests End-to-End (E2E)** : Validation du comportement du système dans son ensemble

## Priorités et Ordre d'Implémentation

1. **Tests E2E sur le code COBOL existant** - Pour établir une référence de comportement
2. **Tests Unitaires sur les modules COBOL** - Pour documenter le comportement de chaque fonction
3. **Mise en œuvre des modules Python** - Avec tests unitaires en parallèle 
4. **Tests d'Intégration Python** - Pour valider les interactions
5. **Tests E2E sur le code Python** - Pour confirmer la parité fonctionnelle

## Détail des Tests

### 1. Tests End-to-End (E2E)

#### Objectif
Capturer le comportement global de l'application COBOL pour s'assurer que l'application Python se comporte de manière identique.

#### Méthodologie
- Créer des scripts qui automatisent les entrées utilisateur
- Capturer et comparer les sorties entre versions COBOL et Python
- Tester toutes les fonctionnalités principales (consultation, crédit, débit, sortie)

#### Cas de Test E2E

| ID | Description | Entrées | Sortie Attendue | Validation |
|----|-------------|---------|-----------------|------------|
| E2E-01 | Consultation du solde initial | Option 1 | Affichage du solde de 1000.00 | ⬜ |
| E2E-02 | Crédit de compte (montant valide) | Option 2, Montant 500.00 | Nouveau solde de 1500.00 | ⬜ |
| E2E-03 | Crédit de compte (montant zéro) | Option 2, Montant 0.00 | Message d'erreur, solde inchangé | ⬜ |
| E2E-04 | Débit de compte (montant valide) | Option 3, Montant 200.00 | Nouveau solde réduit de 200.00 | ⬜ |
| E2E-05 | Débit de compte (montant supérieur au solde) | Option 3, Montant 2000.00 | Message "Fonds insuffisants" | ⬜ |
| E2E-06 | Débit de compte (montant zéro) | Option 3, Montant 0.00 | Message d'erreur, solde inchangé | ⬜ |
| E2E-07 | Sortie du programme | Option 4 | Message de sortie | ⬜ |
| E2E-08 | Option invalide | Option 9 | Message d'erreur | ⬜ |
| E2E-09 | Séquence d'opérations multiples | Options 2, 3, 1, 4 | Comportement correct pour chaque opération | ⬜ |

### 2. Tests Unitaires

#### Tests pour les modules COBOL

##### Module Principal (MainProgram)

| ID | Description | Entrées | Sortie Attendue | Validation |
|----|-------------|---------|-----------------|------------|
| UT-MAIN-01 | Validation du menu principal | N/A | Affichage correct des options | ⬜ |
| UT-MAIN-02 | Sélection option 1 (consultation) | Option 1 | Appel à Operations avec 'TOTAL ' | ⬜ |
| UT-MAIN-03 | Sélection option 2 (crédit) | Option 2 | Appel à Operations avec 'CREDIT' | ⬜ |
| UT-MAIN-04 | Sélection option 3 (débit) | Option 3 | Appel à Operations avec 'DEBIT ' | ⬜ |
| UT-MAIN-05 | Sélection option 4 (sortie) | Option 4 | Modification du drapeau de continuation | ⬜ |
| UT-MAIN-06 | Sélection option invalide | Option 9 | Message d'erreur affiché | ⬜ |

##### Module Opérations (Operations)

| ID | Description | Entrées | Sortie Attendue | Validation |
|----|-------------|---------|-----------------|------------|
| UT-OPS-01 | Consultation du solde | OPERATION-TYPE='TOTAL ' | Appel à DataProgram avec 'READ', affichage du solde | ⬜ |
| UT-OPS-02 | Crédit de compte (montant valide) | OPERATION-TYPE='CREDIT', Montant 500.00 | Ajout au solde, appel à DataProgram avec 'WRITE' | ⬜ |
| UT-OPS-03 | Débit de compte (montant valide) | OPERATION-TYPE='DEBIT ', Montant 200.00 | Soustraction du solde, appel à DataProgram avec 'WRITE' | ⬜ |
| UT-OPS-04 | Débit de compte (montant supérieur au solde) | OPERATION-TYPE='DEBIT ', Montant 2000.00 | Message "Fonds insuffisants", pas de modification | ⬜ |

##### Module Données (DataProgram)

| ID | Description | Entrées | Sortie Attendue | Validation |
|----|-------------|---------|-----------------|------------|
| UT-DATA-01 | Lecture du solde | PASSED-OPERATION='READ' | Copie de STORAGE-BALANCE vers BALANCE | ⬜ |
| UT-DATA-02 | Écriture du solde | PASSED-OPERATION='WRITE', BALANCE=1500.00 | Mise à jour de STORAGE-BALANCE avec 1500.00 | ⬜ |

#### Tests pour les modules Python

##### AccountManager

| ID | Description | Entrées | Sortie Attendue | Validation |
|----|-------------|---------|-----------------|------------|
| UT-PY-AM-01 | Initialisation avec solde par défaut | N/A | Solde initialisé à 1000.00 | ⬜ |
| UT-PY-AM-02 | Consultation du solde | N/A | Retourne le solde correct | ⬜ |
| UT-PY-AM-03 | Crédit de compte (montant valide) | amount=500.00 | Solde augmenté de 500.00, retourne True | ⬜ |
| UT-PY-AM-04 | Crédit de compte (montant zéro ou négatif) | amount=0.00 | Message d'erreur, retourne False | ⬜ |
| UT-PY-AM-05 | Débit de compte (montant valide) | amount=200.00 | Solde réduit de 200.00, retourne True | ⬜ |
| UT-PY-AM-06 | Débit de compte (montant supérieur au solde) | amount=2000.00 | Message "Fonds insuffisants", retourne False | ⬜ |
| UT-PY-AM-07 | Débit de compte (montant zéro ou négatif) | amount=0.00 | Message d'erreur, retourne False | ⬜ |
| UT-PY-AM-08 | Persistance des données (sauvegarde) | Modification du solde | Fichier JSON créé/mis à jour | ⬜ |
| UT-PY-AM-09 | Persistance des données (chargement) | N/A | Chargement correct du solde depuis le fichier | ⬜ |

##### Application Principale

| ID | Description | Entrées | Sortie Attendue | Validation |
|----|-------------|---------|-----------------|------------|
| UT-PY-APP-01 | Affichage du menu | N/A | Menu correctement affiché | ⬜ |
| UT-PY-APP-02 | Saisie du montant (valide) | "100.00" | Retourne 100.00 | ⬜ |
| UT-PY-APP-03 | Saisie du montant (invalide puis valide) | "abc", puis "100.00" | Demande à nouveau, puis retourne 100.00 | ⬜ |
| UT-PY-APP-04 | Saisie du montant (négatif puis valide) | "-50.00", puis "100.00" | Demande à nouveau, puis retourne 100.00 | ⬜ |
| UT-PY-APP-05 | Traitement option 1 (consultation) | Option "1" | Appel à get_balance() et affichage | ⬜ |
| UT-PY-APP-06 | Traitement option 2 (crédit) | Option "2", montant | Appel à credit_account() et affichage | ⬜ |
| UT-PY-APP-07 | Traitement option 3 (débit) | Option "3", montant | Appel à debit_account() et affichage | ⬜ |
| UT-PY-APP-08 | Traitement option 4 (sortie) | Option "4" | Sortie du programme | ⬜ |
| UT-PY-APP-09 | Traitement option invalide | Option "9" | Message d'erreur | ⬜ |

### 3. Tests d'Intégration

#### Tests d'Intégration pour COBOL

| ID | Description | Entrées | Sortie Attendue | Validation |
|----|-------------|---------|-----------------|------------|
| IT-COB-01 | Main -> Operations (consultation) | Option 1 | Appel correct et affichage du solde | ⬜ |
| IT-COB-02 | Main -> Operations -> Data (crédit) | Option 2, Montant | Mise à jour correcte du solde | ⬜ |
| IT-COB-03 | Main -> Operations -> Data (débit) | Option 3, Montant | Mise à jour correcte du solde | ⬜ |

#### Tests d'Intégration pour Python

| ID | Description | Entrées | Sortie Attendue | Validation |
|----|-------------|---------|-----------------|------------|
| IT-PY-01 | app.py -> AccountManager (consultation) | Option "1" | Appel correct et affichage du solde | ⬜ |
| IT-PY-02 | app.py -> AccountManager (crédit) | Option "2", Montant | Mise à jour et sauvegarde correcte du solde | ⬜ |
| IT-PY-03 | app.py -> AccountManager (débit) | Option "3", Montant | Mise à jour et sauvegarde correcte du solde | ⬜ |
| IT-PY-04 | AccountManager -> Fichier JSON | Modification du solde | Persistance des données | ⬜ |

## Risques et Points d'Attention

### Différences de Comportement à Surveiller

1. **Précision Numérique**
   - COBOL : Précision fixe avec PIC 9(6)V99 (6 chiffres avant la virgule, 2 après)
   - Python : Nombres à virgule flottante (potentielles erreurs d'arrondi)
   - **Action** : Vérifier la précision des calculs, particulièrement pour les grands nombres

2. **Gestion des Erreurs**
   - COBOL : Gestion minimale des erreurs
   - Python : Possibilité d'exceptions plus complexes
   - **Action** : S'assurer que les messages d'erreur sont équivalents

3. **Persistance des Données**
   - COBOL : Utilise une variable en mémoire (STORAGE-BALANCE)
   - Python : Utilise un fichier JSON pour la persistance
   - **Action** : Vérifier que le comportement reste cohérent entre redémarrages

4. **Saisie Utilisateur**
   - COBOL : Validation limitée des entrées
   - Python : Validation plus robuste possible
   - **Action** : Aligner les comportements de validation

## Outils et Frameworks Recommandés

1. **Tests Unitaires Python**
   - pytest : Framework de test flexible et puissant
   - unittest.mock : Pour simuler les interactions avec le système de fichiers

2. **Tests E2E**
   - pexpect (Python) : Pour automatiser les interactions avec les programmes en ligne de commande
   - Bash/Shell scripts : Pour orchestrer l'exécution et la comparaison

3. **Outils de Comparaison**
   - difflib (Python) : Pour comparer les sorties textuelles
   - Coverage.py : Pour mesurer la couverture de code des tests

## Mise en Œuvre des Tests

### Étapes Pratiques

1. **Préparation**
   - Mettre en place l'environnement d'exécution COBOL (GnuCOBOL recommandé)
   - Configurer l'environnement Python avec les dépendances nécessaires
   - Créer la structure de répertoires pour les tests

2. **Implémentation**
   - Créer d'abord les tests E2E pour le code COBOL
   - Développer les tests unitaires COBOL (si possible) ou documenter le comportement
   - Développer les tests unitaires Python en parallèle de l'implémentation
   - Mettre en place les tests d'intégration Python
   - Exécuter les tests E2E sur la version Python

3. **Validation**
   - Comparer les résultats des tests E2E entre COBOL et Python
   - Vérifier la couverture de code pour s'assurer que tous les chemins sont testés
   - Documenter les différences acceptables (le cas échéant)

## Conclusion

Cette stratégie de tests fournit un cadre complet pour assurer la parité fonctionnelle entre la version COBOL et la version Python de l'application de gestion de compte. En suivant cette approche, vous minimiserez les risques de régression et garantirez que la migration préserve le comportement métier attendu.
