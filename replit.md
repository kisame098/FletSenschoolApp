# École Sans Base - Gestion d'établissement

## Overview

This is a Python-based school management system built with Flet (Flutter for Python) that provides a desktop application for managing educational institutions. The system handles student and teacher registration, class management, attendance tracking, grades, and scheduling without requiring a traditional database setup.

## Recent Changes

### Dernières améliorations (27/07/2025)
- **Gestion complète des classes**: Système complet de création, modification et suppression des classes
- **Interface de date améliorée**: Formatage automatique et calendrier pour les dates de naissance  
- **Correction scrollbar sidebar**: Résolution du problème de défilement dans le menu de navigation
- **Validation des classes**: Seules les classes créées dans "Gestion des classes" sont disponibles pour l'inscription
- **Compteur d'élèves**: Affichage du nombre d'élèves par classe

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