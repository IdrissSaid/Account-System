# Plan de Test Complet pour la Migration COBOL vers Python

Ce plan de test détaille tous les cas de test nécessaires pour garantir la parité fonctionnelle entre l'application COBOL d'origine et sa version migrée en Python.

## 1. Tests End-to-End (E2E)

Ces tests vérifient le comportement global de l'application en simulant les interactions utilisateur et en comparant les sorties des deux versions.

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| E2E-01 | Consultation du solde initial | Option 1 | Affichage du solde de 1000.00 | ✅ |
| E2E-02 | Crédit de compte (montant valide) | Option 2, Montant 500.00 | Nouveau solde de 1500.00 | ✅ |
| E2E-03 | Crédit de compte (montant zéro) | Option 2, Montant 0.00 | Message d'erreur, solde inchangé | ✅ |
| E2E-04 | Débit de compte (montant valide) | Option 3, Montant 200.00 | Nouveau solde réduit de 200.00 | ✅ |
| E2E-05 | Débit de compte (montant supérieur au solde) | Option 3, Montant 2000.00 | Message "Fonds insuffisants" | ✅ |
| E2E-06 | Débit de compte (montant zéro) | Option 3, Montant 0.00 | Message d'erreur, solde inchangé | ✅ |
| E2E-07 | Sortie du programme | Option 4 | Message de sortie | ✅ |
| E2E-08 | Option invalide | Option 9 | Message d'erreur | ✅ |
| E2E-09 | Séquence d'opérations multiples | Options 2, 3, 1, 4 | Comportement correct pour chaque opération | ✅ |
| E2E-10 | Entrée non numérique pour le montant | Option 2, "abc" puis 100.00 | Rejet de l'entrée invalide, acceptation de l'entrée valide | ❌ |
| E2E-11 | Persistance entre les sessions | Options: 2, 500.00, 4, puis redémarrage, Option 1 | Le solde mis à jour (1500.00) persiste entre les sessions | ❌ |
| E2E-12 | Nombres à la limite de la précision COBOL | Option 2, 999999.99 | Solde correctement mis à jour sans troncature | ❌ |
| E2E-13 | Saisie avec différents formats de nombre | Option 2, "500", "500.0", "500,00" | Tous les formats valides acceptés | ❌ |

## 2. Tests Unitaires pour les Modules COBOL

Note: Ces tests peuvent être difficiles à implémenter directement sur COBOL sans outils spécialisés. Ils servent principalement de documentation du comportement attendu.

### Module Principal (MainProgram)

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| UT-MAIN-01 | Validation du menu principal | N/A | Affichage correct des options | ❌ |
| UT-MAIN-02 | Sélection option 1 (consultation) | Option 1 | Appel à Operations avec 'TOTAL ' | ❌ |
| UT-MAIN-03 | Sélection option 2 (crédit) | Option 2 | Appel à Operations avec 'CREDIT' | ❌ |
| UT-MAIN-04 | Sélection option 3 (débit) | Option 3 | Appel à Operations avec 'DEBIT ' | ❌ |
| UT-MAIN-05 | Sélection option 4 (sortie) | Option 4 | Modification du drapeau de continuation | ❌ |
| UT-MAIN-06 | Sélection option invalide | Option 9 | Message d'erreur affiché | ❌ |

### Module Opérations (Operations)

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| UT-OPS-01 | Consultation du solde | OPERATION-TYPE='TOTAL ' | Appel à DataProgram avec 'READ', affichage du solde | ❌ |
| UT-OPS-02 | Crédit de compte (montant valide) | OPERATION-TYPE='CREDIT', Montant 500.00 | Ajout au solde, appel à DataProgram avec 'WRITE' | ❌ |
| UT-OPS-03 | Débit de compte (montant valide) | OPERATION-TYPE='DEBIT ', Montant 200.00 | Soustraction du solde, appel à DataProgram avec 'WRITE' | ❌ |
| UT-OPS-04 | Débit de compte (montant supérieur au solde) | OPERATION-TYPE='DEBIT ', Montant 2000.00 | Message "Fonds insuffisants", pas de modification | ❌ |
| UT-OPS-05 | Validation des arrondis | OPERATION-TYPE='CREDIT', Montant 0.123 | Arrondi à 0.12, solde augmenté de 0.12 | ❌ |
| UT-OPS-06 | Limites de précision | OPERATION-TYPE='CREDIT', Montant 999999.99 | Accepté, solde mis à jour correctement | ❌ |
| UT-OPS-07 | Dépassement de capacité | OPERATION-TYPE='CREDIT', Montant 9999999.99 | Comportement à documenter (erreur ou troncature) | ❌ |

### Module Données (DataProgram)

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| UT-DATA-01 | Lecture du solde | PASSED-OPERATION='READ' | Copie de STORAGE-BALANCE vers BALANCE | ❌ |
| UT-DATA-02 | Écriture du solde | PASSED-OPERATION='WRITE', BALANCE=1500.00 | Mise à jour de STORAGE-BALANCE avec 1500.00 | ❌ |
| UT-DATA-03 | Opération non reconnue | PASSED-OPERATION='OTHER' | Aucune action effectuée | ❌ |

## 3. Tests Unitaires pour les Modules Python

### AccountManager

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| UT-PY-AM-01 | Initialisation avec solde par défaut | N/A | Solde initialisé à 1000.00 | ✅ |
| UT-PY-AM-02 | Consultation du solde | N/A | Retourne le solde correct | ✅ |
| UT-PY-AM-03 | Crédit de compte (montant valide) | amount=500.00 | Solde augmenté de 500.00, retourne True | ✅ |
| UT-PY-AM-04 | Crédit de compte (montant zéro ou négatif) | amount=0.00 | Message d'erreur, retourne False | ✅ |
| UT-PY-AM-05 | Débit de compte (montant valide) | amount=200.00 | Solde réduit de 200.00, retourne True | ✅ |
| UT-PY-AM-06 | Débit de compte (montant supérieur au solde) | amount=2000.00 | Message "Fonds insuffisants", retourne False | ✅ |
| UT-PY-AM-07 | Débit de compte (montant zéro ou négatif) | amount=0.00 | Message d'erreur, retourne False | ✅ |
| UT-PY-AM-08 | Persistance des données (sauvegarde) | Modification du solde | Fichier JSON créé/mis à jour | ✅ |
| UT-PY-AM-09 | Persistance des données (chargement) | N/A | Chargement correct du solde depuis le fichier | ✅ |
| UT-PY-AM-10 | Précision des nombres décimaux | Tests avec grands nombres et décimales | Comparable à la précision COBOL | ✅ |
| UT-PY-AM-11 | Fichier de données corrompu | Fichier JSON invalide | Fallback au solde par défaut | ❌ |
| UT-PY-AM-12 | Erreur de sauvegarde | Fichier en lecture seule | Gestion appropriée de l'erreur | ❌ |
| UT-PY-AM-13 | Grandes valeurs numériques | Montants à 6 chiffres avant la virgule | Traitement sans perte de précision | ❌ |
| UT-PY-AM-14 | Arrondis de nombres | Montants avec plus de 2 décimales | Arrondis identiques à COBOL | ❌ |

### Application Principale

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| UT-PY-APP-01 | Affichage du menu | N/A | Menu correctement affiché | ✅ |
| UT-PY-APP-02 | Saisie du montant (valide) | "100.00" | Retourne 100.00 | ✅ |
| UT-PY-APP-03 | Saisie du montant (invalide puis valide) | "abc", puis "100.00" | Demande à nouveau, puis retourne 100.00 | ✅ |
| UT-PY-APP-04 | Saisie du montant (négatif puis valide) | "-50.00", puis "100.00" | Demande à nouveau, puis retourne 100.00 | ✅ |
| UT-PY-APP-05 | Traitement option 1 (consultation) | Option "1" | Appel à get_balance() et affichage | ✅ |
| UT-PY-APP-06 | Traitement option 2 (crédit) | Option "2", montant | Appel à credit_account() et affichage | ✅ |
| UT-PY-APP-07 | Traitement option 3 (débit) | Option "3", montant | Appel à debit_account() et affichage | ✅ |
| UT-PY-APP-08 | Traitement option 4 (sortie) | Option "4" | Sortie du programme | ✅ |
| UT-PY-APP-09 | Traitement option invalide | Option "9" | Message d'erreur | ✅ |
| UT-PY-APP-10 | Formats d'entrée alternatifs | "1.0", "1,0", "1" | Tous acceptés comme 1.0 | ❌ |
| UT-PY-APP-11 | Interruption utilisateur (Ctrl+C) | Signal d'interruption | Sortie propre du programme | ❌ |
| UT-PY-APP-12 | Entrées avec espaces | " 100.00 " | Nettoyage des espaces, accepté comme 100.00 | ❌ |

## 4. Tests d'Intégration

### Tests d'Intégration pour COBOL

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| IT-COB-01 | Main -> Operations (consultation) | Option 1 | Appel correct et affichage du solde | ❌ |
| IT-COB-02 | Main -> Operations -> Data (crédit) | Option 2, Montant | Mise à jour correcte du solde | ❌ |
| IT-COB-03 | Main -> Operations -> Data (débit) | Option 3, Montant | Mise à jour correcte du solde | ❌ |
| IT-COB-04 | Flux complet avec plusieurs opérations | Séquence d'opérations | État final correct | ❌ |

### Tests d'Intégration pour Python

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| IT-PY-01 | app.py -> AccountManager (consultation) | Option "1" | Appel correct et affichage du solde | ❌ |
| IT-PY-02 | app.py -> AccountManager (crédit) | Option "2", Montant | Mise à jour et sauvegarde correcte du solde | ❌ |
| IT-PY-03 | app.py -> AccountManager (débit) | Option "3", Montant | Mise à jour et sauvegarde correcte du solde | ❌ |
| IT-PY-04 | AccountManager -> Fichier JSON | Modification du solde | Persistance des données | ❌ |
| IT-PY-05 | Cycle complet avec redémarrage | Séquence incluant arrêt/reprise | Persistance correcte des données | ❌ |
| IT-PY-06 | Traitement des erreurs inter-modules | Entrées problématiques | Propagation correcte des erreurs | ❌ |

## 5. Tests de Performance

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| PERF-01 | Temps de réponse pour consultation | Option 1 | Temps de réponse comparable à COBOL | ❌ |
| PERF-02 | Temps de réponse pour crédit | Option 2, Montant | Temps de réponse comparable à COBOL | ❌ |
| PERF-03 | Temps de réponse pour débit | Option 3, Montant | Temps de réponse comparable à COBOL | ❌ |
| PERF-04 | Performances avec grand nombre d'opérations | Séquence longue d'opérations | Comportement stable | ❌ |

## 6. Tests de Robustesse

| ID | Description | Entrées | Sortie Attendue | Implémenté |
|----|-------------|---------|-----------------|------------|
| ROB-01 | Entrées très longues | Option 2, chaîne de 1000 caractères | Gestion correcte (rejet propre) | ❌ |
| ROB-02 | Valeurs aux limites | Montants très grands ou très petits | Gestion correcte selon les spécifications | ❌ |
| ROB-03 | Caractères spéciaux dans les entrées | Option 2, "$100.00" | Gestion correcte (rejet ou nettoyage) | ❌ |
| ROB-04 | Fichier de données inaccessible | Fichier verrouillé | Message d'erreur approprié | ❌ |
| ROB-05 | Corruption de fichier pendant l'exécution | Modification externe du fichier | Récupération ou message d'erreur clair | ❌ |

## 7. Recommandations pour l'Exécution des Tests

### Ordre de Priorité

1. Tests E2E (E2E-01 à E2E-09) - Établissent la parité fonctionnelle de base
2. Tests unitaires Python (UT-PY-AM-01 à UT-PY-AM-10, UT-PY-APP-01 à UT-PY-APP-09) - Valident les composants Python
3. Tests d'intégration Python (IT-PY-01 à IT-PY-04) - Valident les interactions entre composants
4. Tests de robustesse (ROB-01 à ROB-05) - Assurent la stabilité face aux entrées problématiques
5. Tests supplémentaires (E2E-10 à E2E-13, etc.) - Couvrent les cas particuliers

### Environnement de Test

- Installer GnuCOBOL pour les tests E2E
- Assurer l'accès en lecture/écriture au répertoire de travail
- Exécuter les tests dans un environnement propre (réinitialisation des données entre les tests)

### Couverture de Code

- Vérifier la couverture des tests avec des outils comme coverage.py
- S'assurer que tous les chemins d'exécution importants sont testés
- Porter une attention particulière aux conditions limites et chemins d'erreur

## 8. Conclusion

Ce plan de test complet couvre tous les aspects fonctionnels et non-fonctionnels nécessaires pour assurer une migration COBOL vers Python réussie. En suivant méthodiquement ce plan, vous garantirez que la version Python offre exactement le même comportement que la version COBOL originale, tout en bénéficiant des avantages de la modernisation du code.
