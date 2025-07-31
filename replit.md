# École Sans Base - Gestion d'établissement

## Overview

This is a Python-based school management system built with Flet (Flutter for Python) that provides a desktop application for managing educational institutions. The system handles student and teacher registration, class management, attendance tracking, grades, and scheduling without requiring a traditional database setup.

## Recent Changes

### Système complet de calcul des moyennes (31/07/2025)
- **Nouveau bouton "Calculer les moyennes"** :
  - Accessible après sélection d'un semestre dans Gestion des notes
  - Propose deux méthodes de calcul distinctes avec algorithms précis
  - Interface claire avec options explicites et exemples

- **Option 1 : Utiliser les 2 meilleurs devoirs** :
  - Algorithme : (meilleur_devoir1 + meilleur_devoir2 + composition) / 3
  - Tri automatique des notes de devoirs par ordre décroissant
  - Gestion des cas avec un seul devoir (duplication automatique)
  - Calcul de moyenne pondérée par coefficient de matière

- **Option 2 : Utiliser tous les devoirs** :
  - Algorithme : (somme_tous_devoirs + composition) / (nombre_devoirs + 1)
  - Évite le biais de calcul pour matières avec nombres de devoirs différents
  - Inclusif de tous les devoirs saisis pour chaque matière
  - Calcul robuste et équitable

- **Affichage des résultats** :
  - Tableau trié par moyenne générale décroissante
  - Code couleur selon performance (vert ≥16, bleu ≥14, orange ≥10, rouge <10)
  - Détails par matière avec moyennes individuelles
  - Interface professionnelle avec navigation claire

### Système de devoirs flexibles (31/07/2025)
- **Nombre de devoirs configurable** :
  - Nouveau sélecteur permettant de choisir entre 2, 3 ou 4 devoirs par matière
  - Interface dynamique qui s'adapte au nombre de devoirs sélectionné
  - Colonnes de tableau générées automatiquement selon le choix (Devoir 1, Devoir 2, Devoir 3, Devoir 4)
  - Préservation des notes existantes lors du changement de configuration

- **Fonctionnalités avancées** :
  - Sauvegarde et récupération des notes pour tous les types de devoirs
  - Validation des notes (0-20) pour tous les devoirs
  - Interface cohérente avec le système existant
  - Changement instantané sans rechargement complet de page

- **Interface utilisateur** :
  - Dropdown "Nombre de devoirs" placé en haut à gauche du tableau de notes
  - Colonnes redimensionnées automatiquement pour s'adapter aux devoirs supplémentaires
  - Conservation du style visuel uniforme avec le reste de l'application

### Synchronisation des matières entre semestres (31/07/2025)
- **Bouton Synchroniser pour le Deuxième semestre** :
  - Nouveau bouton "Synchroniser" visible uniquement dans la gestion du Deuxième semestre
  - Copie automatiquement toutes les matières et coefficients du Premier semestre
  - Ne copie pas les notes (restent vides pour le deuxième semestre)
  - Synchronisation instantanée sans rechargement complet de page
  
- **Fonctionnalités avancées** :
  - Détection automatique des matières existantes avec demande de confirmation
  - Suppression et remplacement des matières existantes si nécessaire
  - Messages de confirmation et de succès avec compteur de matières synchronisées
  - Gestion d'erreurs avec messages informatifs
  - Référence de traçabilité (sync_from) pour lier les matières synchronisées

- **Interface utilisateur** :
  - Bouton vert "Synchroniser" avec icône sync placé à côté du bouton "Ajouter une matière"
  - Tooltip explicatif sur la fonction du bouton
  - Dialog de confirmation avec détails sur le nombre de matières

### Système complet de gestion des professeurs (29/07/2025)
- **Gestion des professeurs identique aux élèves** :
  - Barre de recherche instantanée par ID, nom, prénom ou nom complet
  - Système de masquage/affichage des colonnes avec popup "Paramètres"
  - Colonnes spécifiques aux professeurs : Email, Téléphone, Résidence, Expérience, Matière
  - Colonne "Lieu de naissance" désactivée par défaut comme pour les élèves
  - Tri automatique par ID et hauteur dynamique du tableau
  
- **Actions complètes sur les professeurs** :
  - Popup de modification avec formulaire pré-rempli et scrollbars
  - Popup de confirmation de suppression avec détails du professeur
  - Validation des champs obligatoires (prénom, nom, date naissance, genre, email, matière)
  - Design cohérent avec la gestion des élèves

- **Ergonomie unifiée** :
  - Même design que la gestion des élèves pour garantir l'uniformité
  - Boutons d'actions identiques (Modifier/Supprimer)
  - Même système de colonnes configurables
  - Interface responsive avec scrollbars horizontaux et verticaux

### Gestion avancée des colonnes et recherche d'élèves (29/07/2025)
- **Barre de recherche dans la gestion des élèves** :
  - Remplacement du bouton "Nouvel élève" par une barre de recherche
  - Recherche instantanée et insensible à la casse par ID, nom, prénom ou nom complet
  - Filtrage combiné avec le sélecteur de classe existant
  - Conservation de toutes les fonctionnalités existantes

- **Système de gestion d'affichage des colonnes** :
  - Nouveau bouton "Paramètres" au-dessus du tableau des élèves
  - Popup modal permettant d'activer/désactiver l'affichage des colonnes
  - Colonne "Lieu de naissance" ajoutée (désactivée par défaut, apparaît après "Date de naissance")
  - Colonnes ID et Actions non-désactivables pour maintenir l'intégrité du tableau
  - Changements dynamiques sans rechargement de page
  - Préservation des données même quand les colonnes sont masquées

- **Actions améliorées pour la gestion des élèves** :
  - Popup de modification d'élève avec formulaire complet pré-rempli
  - ID verrouillé et non-modifiable lors de l'édition
  - Validation des champs obligatoires avant sauvegarde
  - Popup de confirmation de suppression avec informations détaillées de l'élève
  - Design moderne et responsive pour tous les popups
  - Interface utilisateur cohérente avec le style graphique existant

### Modifications de l'interface utilisateur (29/07/2025)
- **Formulaire d'inscription des élèves** : 
  - Champ ID déplacé vers le haut (verticalement) tout en conservant sa position horizontale à droite
  - Le champ ID n'est plus aligné avec les champs "Prénom" et "Nom"
- **Affichage des données des élèves** :
  - Colonnes "Prénom" et "Nom" séparées en deux colonnes distinctes
  - Nouvel ordre des colonnes : ID | Prénom | Nom | Date de naissance | Lieu de naissance (optionnel) | Genre | Classe (visible uniquement si "Toutes les classes") | N° Élève | N° Parent | Actions
  - Amélioration de la lisibilité et de l'organisation des données
- **Optimisation du tableau de gestion des élèves** :
  - Barre de défilement horizontale toujours visible pour navigation entre colonnes
  - Hauteur dynamique adaptée au nombre d'élèves pour éliminer l'espace vide
  - Structure de scrollbar cohérente avec les autres pages de l'application
  - Fonction de tri robuste gérant différents formats d'ID (entiers et chaînes)

### Dernières améliorations (27/07/2025)
- **Système de popups complet**: Tous les dialogs utilisent maintenant `page.open()` pour un affichage correct
- **ID élève automatique**: Champ ID séquentiel (0, 1, 2...) non-modifiable avec zone encadrée orange
- **Gestion des élèves avancée**: 
  - Sélecteur de classe avec filtrage des élèves par classe
  - Suppression de la colonne classe quand une classe spécifique est sélectionnée
  - Scrollbars horizontal et vertical pour la table des élèves
  - Tri automatique des élèves par ID
- **Correction des erreurs IconButton**: Remplacement des icones invalides par des icones Material Design
- **Interface utilisateur améliorée**: Zone ID encadrée en orange dans le formulaire d'inscription

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Flet (Python bindings for Flutter)
- **UI Pattern**: Single-page application with component-based sidebar navigation
- **Theme**: Modern light theme with custom color scheme using Material Design principles
- **Window Configuration**: Maximized desktop application (1400x800 default)

### Backend Architecture
- **Language**: Python
- **Architecture Pattern**: Object-oriented with centralized data management
- **Data Storage**: File-based JSON storage system
- **Photo Management**: Local file system storage in `photos/students/` directory

### Data Storage Solutions
- **Primary Storage**: JSON files for structured data
- **File Structure**:
  - `data/students.json` - Student records
  - `data/teachers.json` - Teacher records
  - `data/classes.json` - Class information
  - `data/grades.json` - Grade records
  - `data/attendance.json` - Attendance tracking
  - `data/schedule.json` - Class schedules
- **Media Storage**: Local filesystem for student photos
- **Backup Strategy**: File-based with automatic directory creation

## Key Components

### Core Application (`main.py`)
- **StudentRegistrationSystem**: Main application class managing UI state and navigation
- **Form Management**: Handles student registration with comprehensive field validation
- **Photo Integration**: PIL-based image processing for student photos
- **UI State Management**: Centralized page navigation and component rendering

### Data Management Layer (`utils/data_manager.py`)
- **DataManager Class**: Centralized data access layer
- **CRUD Operations**: Create, read, update, delete for all entity types
- **File System Management**: Automatic directory creation and file initialization
- **Error Handling**: Graceful handling of missing files and JSON parsing errors

### Entity Models
- **Students**: Registration number, personal info, academic details, family information
- **Teachers**: Professional records and qualifications
- **Classes**: Class definitions and student assignments
- **Grades**: Academic performance tracking
- **Attendance**: Daily attendance records
- **Schedule**: Class timetables and scheduling

## Data Flow

1. **Application Initialization**:
   - DataManager creates necessary directories and files
   - Main UI components are rendered with sidebar navigation

2. **Data Operations**:
   - User interactions trigger form submissions
   - DataManager handles JSON file read/write operations
   - UI updates reflect data changes immediately

3. **File Management**:
   - Student photos are copied to local storage
   - JSON files are updated atomically to prevent corruption
   - Directory structure is maintained automatically

## External Dependencies

### Core Dependencies
- **Flet**: UI framework for cross-platform desktop applications
- **PIL (Pillow)**: Image processing for student photo management
- **Python Standard Library**: 
  - `json` for data serialization
  - `os` for file system operations
  - `datetime` for timestamp management
  - `shutil` for file operations

### Development Considerations
- No external database required (SQLite, PostgreSQL, etc.)
- No network dependencies for core functionality
- Self-contained application with minimal setup requirements

## Deployment Strategy

### Local Development
- **Setup**: Install Python dependencies via pip
- **Data Persistence**: JSON files and photos stored locally
- **Platform Support**: Cross-platform via Flet framework

### Distribution Options
- **Standalone Executable**: Flet can package as native desktop app
- **Source Distribution**: Python environment with requirements.txt
- **Data Migration**: Simple file copying for backup/restore

### Scalability Considerations
- **Current Approach**: Suitable for small to medium educational institutions
- **Future Migration Path**: DataManager abstraction allows easy transition to SQL databases
- **Performance**: JSON-based storage optimal for <1000 records per entity type

### Security Model
- **Local Storage**: Data remains on local machine
- **No Network Exposure**: Standalone application reduces security surface
- **File Permissions**: Standard OS-level file access controls