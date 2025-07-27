import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class DataManager:
    """Gestionnaire de données pour l'application scolaire"""
    
    def __init__(self):
        self.data_dir = "data"
        self.students_file = os.path.join(self.data_dir, "students.json")
        self.teachers_file = os.path.join(self.data_dir, "teachers.json")
        self.classes_file = os.path.join(self.data_dir, "classes.json")
        self.grades_file = os.path.join(self.data_dir, "grades.json")
        self.attendance_file = os.path.join(self.data_dir, "attendance.json")
        self.schedule_file = os.path.join(self.data_dir, "schedule.json")
        
        self._ensure_data_directory()
        self._initialize_files()
    
    def _ensure_data_directory(self):
        """Créer le répertoire de données s'il n'existe pas"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs("photos/students", exist_ok=True)
    
    def _initialize_files(self):
        """Initialiser les fichiers de données avec des structures vides"""
        files_to_init = [
            self.students_file,
            self.teachers_file,
            self.classes_file,
            self.grades_file,
            self.attendance_file,
            self.schedule_file
        ]
        
        for file_path in files_to_init:
            if not os.path.exists(file_path):
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
    
    def _load_data(self, file_path: str) -> List[Dict]:
        """Charger les données depuis un fichier JSON"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_data(self, file_path: str, data: List[Dict]) -> bool:
        """Sauvegarder les données dans un fichier JSON"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    # Gestion des étudiants
    def get_all_students(self) -> List[Dict]:
        """Récupérer tous les étudiants"""
        return self._load_data(self.students_file)
    
    def get_student(self, student_id: str) -> Optional[Dict]:
        """Récupérer un étudiant par son ID"""
        students = self.get_all_students()
        for student in students:
            if student.get("id") == student_id:
                return student
        return None
    
    def add_student(self, student_data: Dict) -> bool:
        """Ajouter un nouvel étudiant"""
        students = self.get_all_students()
        
        # Vérifier si l'ID existe déjà
        for student in students:
            if student.get("id") == student_data.get("id"):
                # Mettre à jour l'étudiant existant
                student.update(student_data)
                student["date_modification"] = datetime.now().isoformat()
                return self._save_data(self.students_file, students)
        
        # Ajouter un nouveau étudiant
        students.append(student_data)
        return self._save_data(self.students_file, students)
    
    def update_student(self, student_id: str, student_data: Dict) -> bool:
        """Mettre à jour un étudiant"""
        students = self.get_all_students()
        for i, student in enumerate(students):
            if student.get("id") == student_id:
                student_data["date_modification"] = datetime.now().isoformat()
                students[i].update(student_data)
                return self._save_data(self.students_file, students)
        return False
    
    def delete_student(self, student_id: str) -> bool:
        """Supprimer un étudiant"""
        students = self.get_all_students()
        students = [s for s in students if s.get("id") != student_id]
        return self._save_data(self.students_file, students)
    
    # Gestion des professeurs
    def get_all_teachers(self) -> List[Dict]:
        """Récupérer tous les professeurs"""
        return self._load_data(self.teachers_file)
    
    def get_teacher(self, teacher_id: str) -> Optional[Dict]:
        """Récupérer un professeur par son ID"""
        teachers = self.get_all_teachers()
        for teacher in teachers:
            if teacher.get("id") == teacher_id:
                return teacher
        return None
    
    def add_teacher(self, teacher_data: Dict) -> bool:
        """Ajouter un nouveau professeur"""
        teachers = self.get_all_teachers()
        
        # Vérifier si l'ID existe déjà
        for teacher in teachers:
            if teacher.get("id") == teacher_data.get("id"):
                # Mettre à jour le professeur existant
                teacher.update(teacher_data)
                teacher["date_modification"] = datetime.now().isoformat()
                return self._save_data(self.teachers_file, teachers)
        
        # Ajouter un nouveau professeur
        teachers.append(teacher_data)
        return self._save_data(self.teachers_file, teachers)
    
    def update_teacher(self, teacher_id: str, teacher_data: Dict) -> bool:
        """Mettre à jour un professeur"""
        teachers = self.get_all_teachers()
        for i, teacher in enumerate(teachers):
            if teacher.get("id") == teacher_id:
                teacher_data["date_modification"] = datetime.now().isoformat()
                teachers[i].update(teacher_data)
                return self._save_data(self.teachers_file, teachers)
        return False
    
    def delete_teacher(self, teacher_id: str) -> bool:
        """Supprimer un professeur"""
        teachers = self.get_all_teachers()
        teachers = [t for t in teachers if t.get("id") != teacher_id]
        return self._save_data(self.teachers_file, teachers)
    
    # Gestion des classes
    def get_all_classes(self) -> List[Dict]:
        """Récupérer toutes les classes"""
        classes = self._load_data(self.classes_file)
        if not classes:
            # Initialiser avec des classes par défaut
            default_classes = [
                {"id": "CP", "nom": "CP", "niveau": "Primaire", "capacite": 25},
                {"id": "CE1", "nom": "CE1", "niveau": "Primaire", "capacite": 25},
                {"id": "CE2", "nom": "CE2", "niveau": "Primaire", "capacite": 25},
                {"id": "CM1", "nom": "CM1", "niveau": "Primaire", "capacite": 25},
                {"id": "CM2", "nom": "CM2", "niveau": "Primaire", "capacite": 25},
                {"id": "6EME", "nom": "6ème", "niveau": "Collège", "capacite": 30},
                {"id": "5EME", "nom": "5ème", "niveau": "Collège", "capacite": 30},
                {"id": "4EME", "nom": "4ème", "niveau": "Collège", "capacite": 30},
                {"id": "3EME", "nom": "3ème", "niveau": "Collège", "capacite": 30},
                {"id": "2NDE", "nom": "2nde", "niveau": "Lycée", "capacite": 35},
                {"id": "1ERE", "nom": "1ère", "niveau": "Lycée", "capacite": 35},
                {"id": "TERM", "nom": "Terminale", "niveau": "Lycée", "capacite": 35}
            ]
            self._save_data(self.classes_file, default_classes)
            return default_classes
        return classes
    
    def add_class(self, class_data: Dict) -> bool:
        """Ajouter une nouvelle classe"""
        classes = self.get_all_classes()
        classes.append(class_data)
        return self._save_data(self.classes_file, classes)
    
    # Gestion des notes
    def get_all_grades(self) -> List[Dict]:
        """Récupérer toutes les notes"""
        return self._load_data(self.grades_file)
    
    def add_grade(self, grade_data: Dict) -> bool:
        """Ajouter une note"""
        grades = self.get_all_grades()
        grades.append(grade_data)
        return self._save_data(self.grades_file, grades)
    
    def get_student_grades(self, student_id: str) -> List[Dict]:
        """Récupérer les notes d'un étudiant"""
        grades = self.get_all_grades()
        return [g for g in grades if g.get("student_id") == student_id]
    
    # Gestion des présences
    def get_all_attendance(self) -> List[Dict]:
        """Récupérer toutes les présences"""
        return self._load_data(self.attendance_file)
    
    def add_attendance(self, attendance_data: Dict) -> bool:
        """Ajouter une présence"""
        attendance_records = self.get_all_attendance()
        attendance_records.append(attendance_data)
        return self._save_data(self.attendance_file, attendance_records)
    
    def get_student_attendance(self, student_id: str) -> List[Dict]:
        """Récupérer les présences d'un étudiant"""
        attendance_records = self.get_all_attendance()
        return [a for a in attendance_records if a.get("student_id") == student_id]
    
    # Gestion de l'emploi du temps
    def get_all_schedules(self) -> List[Dict]:
        """Récupérer tous les emplois du temps"""
        return self._load_data(self.schedule_file)
    
    def add_schedule(self, schedule_data: Dict) -> bool:
        """Ajouter un emploi du temps"""
        schedules = self.get_all_schedules()
        schedules.append(schedule_data)
        return self._save_data(self.schedule_file, schedules)
    
    def get_class_schedule(self, class_id: str) -> List[Dict]:
        """Récupérer l'emploi du temps d'une classe"""
        schedules = self.get_all_schedules()
        return [s for s in schedules if s.get("class_id") == class_id]
    
    def get_teacher_schedule(self, teacher_id: str) -> List[Dict]:
        """Récupérer l'emploi du temps d'un professeur"""
        schedules = self.get_all_schedules()
        return [s for s in schedules if s.get("teacher_id") == teacher_id]
    
    # Statistiques
    def get_statistics(self) -> Dict:
        """Récupérer les statistiques générales"""
        students = self.get_all_students()
        teachers = self.get_all_teachers()
        classes = self.get_all_classes()
        
        # Compter les étudiants par classe
        students_by_class = {}
        for student in students:
            class_name = student.get("classe", "Non assigné")
            students_by_class[class_name] = students_by_class.get(class_name, 0) + 1
        
        # Compter les professeurs par matière
        teachers_by_subject = {}
        for teacher in teachers:
            subject = teacher.get("matiere", "Non assigné")
            teachers_by_subject[subject] = teachers_by_subject.get(subject, 0) + 1
        
        return {
            "total_students": len(students),
            "total_teachers": len(teachers),
            "total_classes": len(classes),
            "students_by_class": students_by_class,
            "teachers_by_subject": teachers_by_subject,
            "last_updated": datetime.now().isoformat()
        }
