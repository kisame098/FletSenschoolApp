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

### 01/08/2025 - Amélioration ergonomique des tableaux de notes

**Problème identifié :**
- Difficulté de saisie des notes pour le dernier élève du tableau
- Manque d'espacement visuel en bas du tableau causant une gêne ergonomique
- Interface trop compacte rendant la saisie inconfortable

**Solution implémentée (approche rigoureuse) :**

1. **Espacement via conteneur dédié :**
   - Remplacement des lignes vides factices par un conteneur d'espacement
   - Utilisation de `ft.Container(height=100, bgcolor="#ffffff")` pour créer l'espacement
   - Architecture plus propre et maintenable

2. **Structure en colonnes pour les tableaux :**
   - Migration vers `ft.Column([data_table, espacement_container])`
   - Séparation claire entre le contenu et l'espacement
   - Meilleur contrôle de la mise en page

3. **Ajustement coordonné des hauteurs :**
   - Hauteur des conteneurs ajustée : `len(students) * 45 + 150`
   - Espacement fixe de 100px via conteneur dédié
   - Cohérence visuelle maintenue sur tous les tableaux

4. **Avantages de cette approche :**
   - Plus maintenable (pas de fausses données dans le DataTable)
   - Meilleure séparation des responsabilités
   - Facilite les futures modifications d'espacement
   - Respect des bonnes pratiques de développement UI

**Impact utilisateur :**
- Amélioration significative du confort de saisie
- Meilleure visibilité du dernier élève dans la liste
- Interface plus aérée et professionnelle
- Réduction de la fatigue visuelle lors de la saisie

## Préférences utilisateur
- Langue : Français
- Interface : Simple et intuitive pour utilisateurs non-techniques
- Workflow : Optimisation pour réduire les étapes manuelles

## Notes techniques
- Utilisation de Flet pour l'interface utilisateur
- Système de conteneurs modulaires pour la responsivité
- Gestion d'état centralisée via `data_manager.py`
- Persistance JSON pour la simplicité de déploiement