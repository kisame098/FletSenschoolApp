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
6. **Gestion des emplois du temps** - Système complet avec deux modes (classes et professeurs)

## Changements récents

### 04/08/2025 - Nouvelle approche d'édition/suppression des blocs dans l'emploi du temps

**Objectif :**
Rendre l'interface des blocs de cours plus discrète et épurée en supprimant les icônes visibles directement sur les blocs, tout en conservant les fonctionnalités de modification et suppression.

**Améliorations implémentées :**

1. **Suppression des icônes visibles :**
   - Retrait complet des icônes "Modifier" et "Supprimer" affichées sur les blocs de cours
   - Interface plus épurée et moderne
   - Réduction de l'encombrement visuel

2. **Menu contextuel interactif :**
   - Système de clic sur les blocs pour ouvrir un menu contextuel élégant
   - Interface modal avec style cohérent à la charte graphique
   - Affichage des informations du cours (matière, professeur, horaires)

3. **Bouton de fermeture optimisé :**
   - Croix de fermeture positionnée dans le coin supérieur droit exact
   - Design circulaire avec style moderne
   - Tooltip "Fermer" pour une meilleure UX

4. **Préservation des fonctionnalités :**
   - Options "Modifier ce cours" et "Supprimer ce cours" accessibles via le menu
   - Fonctionnement interne identique (pas de rechargement de page)
   - Conservation de toutes les validations et confirmations existantes

**Spécifications respectées :**
- ✅ Interface épurée sans icônes visibles sur les blocs
- ✅ Menu contextuel fluide et instantané au clic
- ✅ Style cohérent avec la charte graphique de l'application
- ✅ Aucun rechargement complet nécessaire après modification/suppression
- ✅ Bouton de fermeture correctement positionné

**Impact utilisateur :**
- Interface plus professionnelle et moins chargée visuellement
- Interaction intuitive avec feedback immédiat
- Meilleure expérience utilisateur avec menu contextuel moderne
- Conservation de toutes les fonctionnalités existantes

## Changements récents

### 01/08/2025 - Refonte complète du système d'emploi du temps (interface professionnelle)

**Problème identifié :**
- L'ancienne implémentation de l'emploi du temps était jugée "médiocre" par l'utilisateur
- Interface basique sans grille visuelle professionnelle
- Manque de positionnement précis des blocs de cours
- Absence de design moderne et intuitif

**Solution implémentée (approche rigoureuse inspirée du code HTML professionnel) :**

1. **Interface d'accueil moderne :**
   - Menu principal avec cartes navigables (Classes/Professeurs)
   - Design épuré inspiré des meilleures pratiques web
   - Navigation intuitive avec boutons de retour

2. **Grille d'emploi du temps professionnelle :**
   - Structure en colonnes : Horaires + 6 jours (Lundi-Samedi)
   - Utilisation de `ft.Stack` pour positionnement absolu des blocs
   - Créneaux de 65px de hauteur (8h-19h) 
   - Bordures et séparations visuelles précises

3. **Positionnement précis des blocs de cours :**
   - Calcul mathématique exact basé sur les horaires
   - Fonction `calculate_course_position()` pour conversion heure→pixels
   - Support des cours de durées variables (30min, 1h, 2h, etc.)
   - Positionnement au pixel près comme dans l'exemple HTML

4. **Blocs de cours visuels :**
   - Couleurs distinctes par matière (10 couleurs prédéfinies)
   - Affichage : Matière, Professeur, Horaires
   - Blocs cliquables pour suppression
   - Design avec coins arrondis et ombres

5. **Formulaire d'ajout optimisé :**
   - Layout en 2 lignes : Classe/Jour/Début/Fin puis Professeur/Matière/Bouton
   - Validation complète des conflits d'horaires
   - Créneaux de 30 minutes (07:00 à 19:30)
   - Réinitialisation automatique après ajout

6. **Architecture technique robuste :**
   - Séparation claire entre affichage et logique
   - Gestion d'erreurs complète avec messages utilisateur
   - Performance optimisée avec mise à jour ciblée
   - Code maintenable et extensible

**Spécifications respectées (inspiration HTML) :**
- ✅ Grille visuelle professionnelle avec positionnement précis
- ✅ Blocs colorés de taille variable selon durée
- ✅ Interface de navigation moderne
- ✅ Formulaire optimisé avec validation
- ✅ Suppression interactive par clic
- ✅ Design cohérent avec les meilleures pratiques

**Impact utilisateur :**
- Interface d'emploi du temps de qualité professionnelle
- Visualisation claire et précise des plannings
- Gestion intuitive avec feedback immédiat
- Respect des standards de l'industrie

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

### 01/08/2025 - Système complet de gestion des emplois du temps

**Fonctionnalité développée :**
Implémentation complète du système de gestion des emplois du temps selon les spécifications détaillées avec deux modes distincts.

**Architecture technique :**

1. **Extension du DataManager :**
   - Nouvelles méthodes pour gérer les créneaux d'emploi du temps
   - Fonctions de détection de conflits d'horaires
   - Gestion des emplois du temps par classe et par professeur
   - Persistance dans `data/schedule.json`

2. **Interface utilisateur avancée :**
   - Sélection du mode (Classes vs Professeurs)
   - Formulaire d'ajout avec auto-complétion des données professeur
   - Validation des horaires et détection de conflits
   - Tableau visuel avec blocs colorés selon la durée des cours

3. **Fonctionnalités implémentées :**
   - **Mode Classes :** Formulaire complet avec champs auto-remplis pour les professeurs
   - **Auto-complétion :** Saisie de l'ID professeur → remplissage automatique des informations
   - **Validation robuste :** Vérification des conflits d'horaires et cohérence des données
   - **Tableau visuel :** Affichage en grille Lundi-Samedi avec blocs colorés par matière
   - **Gestion des durées :** Blocs de hauteur variable selon la durée des cours (1h, 2h, etc.)
   - **Suppression interactive :** Clic sur un cours pour le supprimer
   - **Codes couleur :** Couleurs distinctes par matière pour une lecture rapide

4. **Spécifications respectées :**
   - ✅ Deux modes : Classes et Professeurs
   - ✅ Formulaire avec champs auto-remplis (ID professeur → infos complètes)
   - ✅ Sélection jour/horaires (Lundi-Samedi, 07h00-20h00)
   - ✅ Tableau en grille avec créneaux horaires
   - ✅ Blocs colorés avec durée variable
   - ✅ Détection et prévention des conflits
   - ✅ Ajout instantané sans rechargement
   - ✅ Interface responsive et intuitive

**Impact utilisateur :**
- Gestion complète des plannings scolaires
- Prévention automatique des conflits d'horaires
- Interface visuelle claire avec codes couleur
- Workflow optimisé avec auto-complétion des données

## Préférences utilisateur
- Langue : Français
- Interface : Simple et intuitive pour utilisateurs non-techniques
- Workflow : Optimisation pour réduire les étapes manuelles

## Notes techniques
- Utilisation de Flet pour l'interface utilisateur
- Système de conteneurs modulaires pour la responsivité
- Gestion d'état centralisée via `data_manager.py`
- Persistance JSON pour la simplicité de déploiement