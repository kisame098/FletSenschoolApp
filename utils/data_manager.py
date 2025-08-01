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
        self.subjects_file = os.path.join(self.data_dir, "subjects.json")
        self.attendance_file = os.path.join(self.data_dir, "attendance.json")
        self.schedule_file = os.path.join(self.data_dir, "schedule.json")
        self.homework_config_file = os.path.join(self.data_dir, "homework_config.json")
        self.subject_settings_file = os.path.join(self.data_dir, "subject_settings.json")
        
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
            self.subjects_file,
            self.attendance_file,
            self.schedule_file,
            self.homework_config_file,
            self.subject_settings_file
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
    
    def get_next_student_id(self) -> int:
        """Générer le prochain ID d'élève disponible"""
        students = self.get_all_students()
        
        if not students:
            return 0
        
        # Récupérer tous les IDs existants
        existing_ids = []
        for student in students:
            student_id = student.get("id", student.get("student_id", 0))
            try:
                existing_ids.append(int(student_id))
            except (ValueError, TypeError):
                continue
        
        if not existing_ids:
            return 0
        
        # Trouver le prochain ID disponible (gérer les trous)
        existing_ids.sort()
        
        # Vérifier s'il y a des trous dans la séquence
        for i in range(len(existing_ids)):
            if i not in existing_ids:
                return i
        
        # Si pas de trous, retourner le suivant
        return max(existing_ids) + 1

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
    
    def get_students_by_class(self, class_name: str) -> List[Dict]:
        """Récupérer tous les étudiants d'une classe spécifique"""
        students = self.get_all_students()
        return [s for s in students if s.get("classe") == class_name]
    
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
    
    def get_next_teacher_id(self) -> int:
        """Obtenir le prochain ID de professeur disponible"""
        teachers = self.get_all_teachers()
        if not teachers:
            return 1
        
        # Trouver l'ID le plus élevé et ajouter 1
        max_id = 0
        for teacher in teachers:
            teacher_id = teacher.get("teacher_id", teacher.get("id", 0))
            try:
                current_id = int(teacher_id)
                if current_id > max_id:
                    max_id = current_id
            except (ValueError, TypeError):
                continue
        
        return max_id + 1
    
    # Gestion des classes
    def get_all_classes(self) -> List[Dict]:
        """Récupérer toutes les classes"""
        return self._load_data(self.classes_file)
    
    def get_class(self, class_id: str) -> Optional[Dict]:
        """Récupérer une classe par son ID"""
        classes = self.get_all_classes()
        for classe in classes:
            if classe.get("id") == class_id:
                return classe
        return None
    
    def add_class(self, class_data: Dict) -> bool:
        """Ajouter une nouvelle classe"""
        classes = self.get_all_classes()
        
        # Vérifier si l'ID existe déjà
        for classe in classes:
            if classe.get("id") == class_data.get("id"):
                return False
        
        class_data["date_creation"] = datetime.now().isoformat()
        classes.append(class_data)
        return self._save_data(self.classes_file, classes)
    
    def update_class(self, class_id: str, class_data: Dict) -> bool:
        """Mettre à jour une classe"""
        classes = self.get_all_classes()
        for i, classe in enumerate(classes):
            if classe.get("id") == class_id:
                class_data["date_modification"] = datetime.now().isoformat()
                classes[i].update(class_data)
                return self._save_data(self.classes_file, classes)
        return False
    
    def delete_class(self, class_id: str) -> bool:
        """Supprimer une classe"""
        classes = self.get_all_classes()
        classes = [c for c in classes if c.get("id") != class_id]
        return self._save_data(self.classes_file, classes)
    
    def get_students_count_in_class(self, class_name: str) -> int:
        """Récupérer le nombre d'élèves dans une classe"""
        students = self.get_all_students()
        return len([s for s in students if s.get("classe") == class_name])
    
    # Gestion des matières
    def get_all_subjects(self) -> List[Dict]:
        """Récupérer toutes les matières"""
        return self._load_data(self.subjects_file)
    
    def get_subjects_by_semester(self, semester: str) -> List[Dict]:
        """Récupérer les matières d'un semestre"""
        subjects = self.get_all_subjects()
        return [s for s in subjects if s.get("semestre") == semester]
    
    def add_subject(self, subject_data: Dict) -> bool:
        """Ajouter une nouvelle matière"""
        subjects = self.get_all_subjects()
        
        # Vérifier si l'ID existe déjà
        for subject in subjects:
            if subject.get("id") == subject_data.get("id"):
                return False
        
        subject_data["date_creation"] = datetime.now().isoformat()
        subjects.append(subject_data)
        return self._save_data(self.subjects_file, subjects)
    
    def get_subject(self, subject_id: str) -> Optional[Dict]:
        """Récupérer une matière par son ID"""
        subjects = self.get_all_subjects()
        for subject in subjects:
            if subject.get("id") == subject_id:
                return subject
        return None
    
    def delete_subject(self, subject_id: str) -> bool:
        """Supprimer une matière"""
        subjects = self.get_all_subjects()
        subjects = [s for s in subjects if s.get("id") != subject_id]
        return self._save_data(self.subjects_file, subjects)
    
    # Gestion des notes
    def get_all_grades(self) -> List[Dict]:
        """Récupérer toutes les notes"""
        return self._load_data(self.grades_file)
    
    def add_grade(self, grade_data: Dict) -> bool:
        """Ajouter ou mettre à jour une note"""
        grades = self.get_all_grades()
        
        # Vérifier si la note existe déjà
        for i, grade in enumerate(grades):
            if grade.get("id") == grade_data.get("id"):
                # Mettre à jour la note existante
                grade_data["date_modification"] = datetime.now().isoformat()
                grades[i] = grade_data
                return self._save_data(self.grades_file, grades)
        
        # Ajouter une nouvelle note
        grade_data["date_creation"] = datetime.now().isoformat()
        grades.append(grade_data)
        return self._save_data(self.grades_file, grades)
    
    def get_student_grades(self, student_id: str) -> List[Dict]:
        """Récupérer les notes d'un étudiant"""
        grades = self.get_all_grades()
        return [g for g in grades if g.get("student_id") == student_id]
    
    def get_student_subject_grades(self, student_id: str, subject_id: str) -> List[Dict]:
        """Récupérer les notes d'un étudiant pour une matière spécifique"""
        grades = self.get_all_grades()
        return [g for g in grades if g.get("student_id") == student_id and g.get("subject_id") == subject_id]
    
    def get_subject_grades(self, subject_id: str) -> List[Dict]:
        """Récupérer toutes les notes d'une matière"""
        grades = self.get_all_grades()
        return [g for g in grades if g.get("subject_id") == subject_id]
    
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
    
    # Ancienne gestion de l'emploi du temps (remplacée par les nouvelles méthodes en fin de fichier)
    
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
    
    # Gestion de la configuration des devoirs
    def get_homework_config(self, class_name: str, subject_id: str, semester: str) -> int:
        """Récupérer le nombre de devoirs configuré pour une classe+matière+semestre"""
        configs = self._load_data(self.homework_config_file)
        
        for config in configs:
            if (config.get("class_name") == class_name and 
                config.get("subject_id") == subject_id and 
                config.get("semester") == semester):
                return config.get("num_homework", 2)  # Par défaut 2 devoirs
        
        return 2  # Par défaut 2 devoirs si pas de configuration
    
    def set_homework_config(self, class_name: str, subject_id: str, semester: str, num_homework: int) -> bool:
        """Définir le nombre de devoirs pour une classe+matière+semestre"""
        configs = self._load_data(self.homework_config_file)
        
        # Vérifier si une configuration existe déjà
        for i, config in enumerate(configs):
            if (config.get("class_name") == class_name and 
                config.get("subject_id") == subject_id and 
                config.get("semester") == semester):
                configs[i]["num_homework"] = num_homework
                configs[i]["updated_at"] = datetime.now().isoformat()
                return self._save_data(self.homework_config_file, configs)
        
        # Créer une nouvelle configuration
        new_config = {
            "class_name": class_name,
            "subject_id": subject_id,
            "semester": semester,
            "num_homework": num_homework,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        configs.append(new_config)
        return self._save_data(self.homework_config_file, configs)
    
    # Gestion des paramètres de matière par élève
    def get_student_subject_settings(self, class_name: str, subject_id: str, semester: str) -> Dict:
        """Récupérer les paramètres d'une matière pour tous les élèves d'une classe"""
        settings_data = self._load_data(self.subject_settings_file)
        
        # Trouver les paramètres pour cette classe+matière+semestre
        for settings in settings_data:
            if (settings.get("class_name") == class_name and 
                settings.get("subject_id") == subject_id and 
                settings.get("semester") == semester):
                return settings.get("student_settings", {})
        
        return {}  # Retourner vide si aucun paramètre trouvé
    
    def save_student_subject_settings(self, class_name: str, subject_id: str, semester: str, student_settings: Dict) -> bool:
        """Sauvegarder les paramètres d'une matière pour tous les élèves d'une classe"""
        settings_data = self._load_data(self.subject_settings_file)
        
        # Chercher s'il existe déjà des paramètres pour cette classe+matière+semestre
        for i, settings in enumerate(settings_data):
            if (settings.get("class_name") == class_name and 
                settings.get("subject_id") == subject_id and 
                settings.get("semester") == semester):
                settings_data[i]["student_settings"] = student_settings
                settings_data[i]["updated_at"] = datetime.now().isoformat()
                return self._save_data(self.subject_settings_file, settings_data)
        
        # Créer de nouveaux paramètres
        new_settings = {
            "class_name": class_name,
            "subject_id": subject_id,
            "semester": semester,
            "student_settings": student_settings,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        settings_data.append(new_settings)
        return self._save_data(self.subject_settings_file, settings_data)
    
    # Gestion des emplois du temps
    def get_all_schedules(self) -> List[Dict]:
        """Récupérer tous les emplois du temps"""
        return self._load_data(self.schedule_file)
    
    def add_schedule_slot(self, schedule_data: Dict) -> bool:
        """Ajouter un créneau à l'emploi du temps"""
        schedules = self.get_all_schedules()
        
        # Générer un ID unique
        schedule_data["id"] = max([s.get("id", 0) for s in schedules], default=0) + 1
        schedule_data["created_at"] = datetime.now().isoformat()
        
        schedules.append(schedule_data)
        return self._save_data(self.schedule_file, schedules)
    
    def get_schedule_by_class(self, class_name: str) -> List[Dict]:
        """Récupérer l'emploi du temps d'une classe"""
        schedules = self.get_all_schedules()
        return [s for s in schedules if s.get("class_name") == class_name]
    
    def get_schedule_by_teacher(self, teacher_id: str) -> List[Dict]:
        """Récupérer l'emploi du temps d'un professeur"""
        schedules = self.get_all_schedules()
        return [s for s in schedules if s.get("teacher_id") == teacher_id]
    
    def check_schedule_conflict(self, class_name: str, day: str, start_time: str, end_time: str, exclude_id: Optional[int] = None) -> bool:
        """Vérifier s'il y a un conflit d'horaire pour une classe"""
        schedules = self.get_schedule_by_class(class_name)
        
        for schedule in schedules:
            if exclude_id and schedule.get("id") == exclude_id:
                continue
                
            if schedule.get("day") == day:
                # Convertir les heures en minutes pour comparaison
                def time_to_minutes(time_str):
                    hour, minute = map(int, time_str.split(':'))
                    return hour * 60 + minute
                
                existing_start = time_to_minutes(schedule.get("start_time", "00:00"))
                existing_end = time_to_minutes(schedule.get("end_time", "00:00"))
                new_start = time_to_minutes(start_time)
                new_end = time_to_minutes(end_time)
                
                # Vérifier chevauchement
                if (new_start < existing_end and new_end > existing_start):
                    return True
        
        return False
    
    def delete_schedule_slot(self, schedule_id: int) -> bool:
        """Supprimer un créneau de l'emploi du temps"""
        schedules = self.get_all_schedules()
        schedules = [s for s in schedules if s.get("id") != schedule_id]
        return self._save_data(self.schedule_file, schedules)
