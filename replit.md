# École Sans Base - Gestion d'établissement

## Overview

This project is a Python-based school management system utilizing Flet (Flutter for Python) to provide a desktop application. It aims to manage educational institutions without requiring a traditional database, handling student and teacher registration, class management, attendance, grades, and scheduling. The system focuses on providing a comprehensive, self-contained solution for small to medium-sized schools.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Flet (Python bindings for Flutter)
- **UI Pattern**: Single-page application with component-based sidebar navigation.
- **Theme**: Modern light theme using Material Design principles with a custom color scheme.
- **Window Configuration**: Maximized desktop application (1400x800 default).
- **UI/UX Decisions**:
    - **ID Management**: Auto-incrementing IDs for students, with intelligent handling of gaps. ID field is non-modifiable in forms and visually highlighted.
    - **Dynamic Tables**: Configurable columns for student and teacher tables, with instant search and filtering. Tables are responsive with horizontal and vertical scrollbars, and dynamic height.
    - **Navigation**: Consistent sidebar navigation and clear page transitions.
    - **Forms & Popups**: Modern, responsive design for all forms and confirmation popups, with pre-filled data for editing and clear validation messages.
    - **Grade Management**: Flexible homework system allowing configuration of 2, 3, or 4 homework assignments per subject. Synchronized subject parameters and coefficients between semesters.
    - **Average Calculation**: Two distinct methods for calculating averages (best 2 homeworks + composition, or all homeworks + composition) with detailed display and color-coded results.
    - **Subject Parameters**: Dedicated page to manage which students take which subjects, including custom coefficients and dispensation options.

### Backend Architecture
- **Language**: Python
- **Architecture Pattern**: Object-oriented with centralized data management.
- **Technical Implementations**:
    - **Data Management Layer**: Centralized `DataManager` class for all CRUD operations on entities.
    - **Auto-increment ID System**: Robust mechanism to generate sequential IDs, managing gaps effectively upon deletion.
    - **Logging**: Detailed console logs for critical operations like student registration, including validation steps and error tracing.

### Data Storage Solutions
- **Primary Storage**: JSON files for structured data.
- **File Structure**: Dedicated JSON files for students, teachers, classes, grades, attendance, and schedules within a `data/` directory.
- **Media Storage**: Local filesystem for student photos in `photos/students/`.
- **Backup Strategy**: File-based with automatic directory creation.

## External Dependencies

### Core Dependencies
- **Flet**: For UI development and cross-platform desktop application capabilities.
- **PIL (Pillow)**: Used for image processing, specifically for student photo management.
- **Python Standard Library**: Essential modules like `json` for data serialization, `os` for file system operations, `datetime` for timestamp management, and `shutil` for file operations.

### Development Considerations
- The system is designed to be self-contained, requiring no external databases (e.g., SQLite, PostgreSQL) or network dependencies for its core functionality.