# School Management App - Documentation du projet

## Vue d'ensemble
Application de gestion scolaire moderne basée sur Flet, conçue pour simplifier les tâches administratives des établissements d'enseignement avec des capacités avancées de gestion des semestres et une interface utilisateur intuitive.

## Technologies principales
- Framework Flet pour application desktop responsive
- Backend Python avec gestion dynamique des données
- Système avancé de gestion des semestres et matières
- Gestion d'erreurs robuste et réactivité UI
- Support multilingue pour flexibilité institutionnelle
- Design UI modulaire basé sur des conteneurs pour améliorer la gestion des layouts

## Architecture du projet

### Structure des fichiers
- `main.py` - Application principale avec toutes les interfaces utilisateur
- `utils/data_manager.py` - Gestionnaire de données et persistance
- `data/` - Répertoire des fichiers de données JSON

### Composants principaux
1. **Gestion des élèves** - Inscription, modification, suppression avec filtrage par classe
2. **Gestion des professeurs** - Administration du personnel enseignant
3. **Gestion des classes** - Organisation des groupes d'élèves
4. **Gestion des notes** - Saisie et suivi des évaluations par semestre et matière
5. **Calcul des moyennes** - Système automatisé avec plusieurs méthodes de calcul

## Changements récents

### 01/08/2025 - Correction du système de lignes vides dans les tableaux de notes

**Problème identifié :**
- Les lignes vides (concept n+2) dans les tableaux de gestion des notes n'étaient pas fonctionnelles
- Les lignes contenaient uniquement du texte vide au lieu de champs de saisie interactifs
- Impossibilité d'ajouter de nouveaux élèves directement depuis le tableau des notes

**Corrections apportées :**

1. **Tableau des notes principales (fonction `create_grades_table`) :**
   - Remplacement des cellules texte vides par des champs TextField interactifs
   - Ajout de champs pour toutes les informations élève : ID (auto-généré), nom, prénom, date de naissance, lieu de naissance
   - Création automatique des champs pour tous les devoirs et la composition
   - Gestion des hints appropriés pour chaque champ
   - Stockage des références dans `self.grade_fields` avec clés `new_student_1` et `new_student_2`

2. **Tableau des paramètres de matière (fonction `create_subject_settings_table`) :**
   - Même approche pour les lignes vides dans les paramètres des matières
   - Ajout de champs informationnels + switch actif/inactif + coefficient personnalisé
   - Stockage des références dans `self.subject_settings_fields`

3. **Fonction de sauvegarde améliorée (`save_all_grades`) :**
   - Détection automatique des nouvelles entrées (lignes commençant par `new_student_`)
   - Validation : nom et prénom obligatoires pour créer un nouvel élève
   - Création automatique de l'élève avec ID auto-incrémenté
   - Assignation automatique à la classe courante
   - Sauvegarde simultanée des notes saisies pour le nouvel élève
   - Messages de confirmation détaillés (élèves ajoutés + notes sauvegardées)
   - Rechargement automatique du tableau après ajout

**Fonctionnalités ajoutées :**
- Possibilité d'ajouter jusqu'à 2 nouveaux élèves par session depuis le tableau des notes
- Saisie simultanée des informations élève et de leurs notes
- Validation automatique des notes (0-20)
- Gestion des erreurs pour valeurs non numériques
- Interface intuitive avec hints explicites dans chaque champ

**Impact utilisateur :**
- Accélération significative du workflow de saisie des notes
- Réduction des allers-retours entre les différentes sections
- Possibilité d'inscription rapide d'élèves tard dans l'année scolaire
- Maintien de la cohérence des données avec validation automatique

## Préférences utilisateur
- Langue : Français
- Interface : Simple et intuitive pour utilisateurs non-techniques
- Workflow : Optimisation pour réduire les étapes manuelles

## Notes techniques
- Utilisation de Flet pour l'interface utilisateur
- Système de conteneurs modulaires pour la responsivité
- Gestion d'état centralisée via `data_manager.py`
- Persistance JSON pour la simplicité de déploiement