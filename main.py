import flet as ft
import os
import json
from datetime import datetime
from PIL import Image
import shutil
from utils.data_manager import DataManager

class StudentRegistrationSystem:
    def __init__(self):
        # Initialize data manager
        self.data_manager = DataManager()
        
        # Variables pour les champs
        self.registration_no = ""
        self.date = datetime.now().strftime("%d/%m/%Y")
        self.full_name = ""
        self.class_var = ""
        self.date_of_birth = ""
        self.religion = ""
        self.gender = "Masculin"
        self.skills = ""
        self.father_name = ""
        self.mother_name = ""
        self.father_occupation = ""
        self.mother_occupation = ""
        
        self.photo_path = None
        self.current_page = "dashboard"
        
        # Variables UI
        self.page = None
        self.sidebar = None
        self.main_content = None
        self.selected_student_id = None
        self.selected_teacher_id = None
        
    def main(self, page: ft.Page):
        self.page = page
        
        # Configuration de la page
        page.title = "École Sans Base - Gestion d'établissement"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window.width = 1400
        page.window.height = 800
        page.window.maximized = True
        page.padding = 0
        page.bgcolor = "#f8fafc"
        
        # Thème personnalisé moderne
        page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary="#4f46e5",
                primary_container="#eef2ff",
                secondary="#64748b",
                surface="#ffffff",
                background="#f8fafc",
                error="#ef4444",
                on_primary="#ffffff",
                on_surface="#1e293b"
            )
        )
        
        # Initialiser la variable de sélection du menu
        self.selected_menu_index = 0
        
        self.setup_layout()
        page.update()
    
    def setup_layout(self):
        """Configuration du layout principal"""
        self.sidebar = self.create_sidebar()
        self.main_content = ft.Container(
            content=ft.Column([]),
            expand=True,
            bgcolor="#f8fafc",
            padding=0
        )
        
        # Layout principal
        main_layout = ft.Row([
            self.sidebar,
            self.main_content
        ], spacing=0, expand=True)
        
        self.page.add(main_layout)
        self.show_dashboard()
    
    def create_sidebar(self):
        """Créer la sidebar moderne"""
        # Menu items avec icônes modernes
        menu_items = [
            ("dashboard", "Tableau de bord", "📊", self.show_dashboard),
            ("student_registration", "Inscription élève", "👤", self.show_student_registration),
            ("student_management", "Gestion des élèves", "👥", self.show_student_management),
            ("teacher_registration", "Inscription professeur", "👨‍🏫", self.show_teacher_registration),
            ("teacher_management", "Gestion des professeurs", "🏫", self.show_teacher_management),
            ("class_management", "Gestion des classes", "🏛️", self.show_class_management),
            ("grade_management", "Gestion des notes", "📝", self.show_grade_management),
            ("schedule", "Emploi du temps", "📅", self.show_schedule),
            ("attendance", "Gestion des présences", "✅", self.show_attendance)
        ]
        
        # Créer les boutons du menu
        menu_buttons = []
        for i, (page_id, label, icon, callback) in enumerate(menu_items):
            is_selected = i == 0  # Premier élément sélectionné par défaut
            
            button = ft.Container(
                content=ft.Row([
                    ft.Text(
                        icon, 
                        color="#ffffff" if is_selected else "#cbd5e1",
                        size=20
                    ),
                    ft.Text(
                        label,
                        color="#ffffff" if is_selected else "#cbd5e1",
                        size=13,
                        weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.W_400
                    )
                ], spacing=12),
                padding=ft.padding.symmetric(vertical=12, horizontal=16),
                bgcolor="#6366f1" if is_selected else "transparent",
                border_radius=8,
                on_click=lambda e, cb=callback, idx=i: self.handle_menu_click(cb, idx),
                width=248,
                alignment=ft.alignment.center_left
            )
            menu_buttons.append(button)
        
        # Menu de navigation
        navigation_menu = ft.Column(
            controls=menu_buttons,
            spacing=4,
            tight=True
        )
        
        # En-tête de la sidebar
        header = ft.Container(
            content=ft.Column([
                ft.Container(height=24),
                ft.Text(
                    "École Sans Base",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color="#ffffff"
                ),
                ft.Text(
                    "Gestion d'établissement",
                    size=13,
                    color="#cbd5e1",
                    weight=ft.FontWeight.W_400
                ),
                ft.Container(height=32),
            ]),
            padding=ft.padding.all(24),
            bgcolor="#4f46e5"
        )
        
        # Container avec scrollbar qui fonctionne correctement
        scrollable_menu = ft.Container(
            content=navigation_menu,
            padding=ft.padding.all(16),
            bgcolor="#4f46e5",
            expand=True
        )
        
        sidebar_container = ft.Container(
            content=ft.Column([
                header,
                ft.Container(
                    content=ft.Column([
                        scrollable_menu
                    ], scroll=ft.ScrollMode.AUTO, expand=True),
                    expand=True,
                    bgcolor="#4f46e5"
                )
            ], spacing=0, expand=True),
            width=280,
            bgcolor="#4f46e5",
            border=ft.border.only(right=ft.border.BorderSide(1, "#e2e8f0"))
        )
        
        return sidebar_container
    
    def handle_menu_click(self, callback, index):
        """Gérer le clic sur un élément du menu"""
        # Mettre à jour la sélection visuelle
        self.selected_menu_index = index
        self.update_menu_selection()
        
        # Appeler la fonction correspondante
        callback()
    
    def update_menu_selection(self):
        """Mettre à jour la sélection du menu"""
        # Recréer la sidebar avec la nouvelle sélection
        new_menu = self.create_navigation_menu()
        # Mettre à jour le contenu du menu scrollable
        self.sidebar.content.controls[1].content.controls[0].content = new_menu
        self.page.update()
    
    def create_navigation_menu(self):
        """Créer le menu de navigation avec la sélection actuelle"""
        menu_items = [
            ("dashboard", "Tableau de bord", "📊", self.show_dashboard),
            ("student_registration", "Inscription élève", "👤", self.show_student_registration),
            ("student_management", "Gestion des élèves", "👥", self.show_student_management),
            ("teacher_registration", "Inscription professeur", "👨‍🏫", self.show_teacher_registration),
            ("teacher_management", "Gestion des professeurs", "🏫", self.show_teacher_management),
            ("class_management", "Gestion des classes", "🏛️", self.show_class_management),
            ("grade_management", "Gestion des notes", "📝", self.show_grade_management),
            ("schedule", "Emploi du temps", "📅", self.show_schedule),
            ("attendance", "Gestion des présences", "✅", self.show_attendance)
        ]
        
        menu_buttons = []
        for i, (page_id, label, icon, callback) in enumerate(menu_items):
            is_selected = i == getattr(self, 'selected_menu_index', 0)
            
            button = ft.Container(
                content=ft.Row([
                    ft.Text(
                        icon, 
                        color="#ffffff" if is_selected else "#cbd5e1",
                        size=20
                    ),
                    ft.Text(
                        label,
                        color="#ffffff" if is_selected else "#cbd5e1",
                        size=13,
                        weight=ft.FontWeight.W_500 if is_selected else ft.FontWeight.W_400
                    )
                ], spacing=12),
                padding=ft.padding.symmetric(vertical=12, horizontal=16),
                bgcolor="#6366f1" if is_selected else "transparent",
                border_radius=8,
                on_click=lambda e, cb=callback, idx=i: self.handle_menu_click(cb, idx),
                width=248,
                alignment=ft.alignment.center_left
            )
            menu_buttons.append(button)
        
        return ft.Column(
            controls=menu_buttons,
            spacing=4,
            tight=True
        )
    
    def clear_main_content(self):
        """Vider le contenu principal"""
        self.main_content.content = ft.Column([])
    
    def create_stats_cards(self):
        """Créer les cartes de statistiques modernes"""
        students_count = len(self.data_manager.get_all_students())
        teachers_count = len(self.data_manager.get_all_teachers())
        classes_count = len(self.data_manager.get_all_classes())
        
        stats_data = [
            (str(students_count), "Élèves inscrits", "👥", "#4f8fea"),
            (str(teachers_count), "Professeurs actifs", "🏫", "#22c55e"),
            (str(classes_count), "Classes disponibles", "🏛️", "#f59e0b")
        ]
        
        cards = []
        for number, label, icon, color in stats_data:
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(icon, color="white", size=22),
                                bgcolor=color,
                                border_radius=10,
                                width=48,
                                height=48,
                                alignment=ft.alignment.center
                            ),
                        ]),
                        ft.Container(height=16),
                        ft.Text(
                            number,
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        ),
                        ft.Text(
                            label,
                            size=13,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        )
                    ]),
                    padding=24,
                    width=280
                ),
                elevation=0,
                surface_tint_color="#ffffff",
                color="#ffffff"
            )
            cards.append(card)
        
        return ft.Row(cards, spacing=24)
    
    def show_dashboard(self):
        """Afficher le tableau de bord"""
        self.current_page = "dashboard"
        self.clear_main_content()
        
        # En-tête moderne
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Tableau de bord",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1e293b"
                ),
                ft.Text(
                    "Vue d'ensemble de votre établissement scolaire",
                    size=15,
                    color="#64748b",
                    weight=ft.FontWeight.W_400
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Statistiques
        stats = ft.Container(
            content=self.create_stats_cards(),
            padding=ft.padding.symmetric(horizontal=32)
        )
        
        # Carte de bienvenue moderne
        welcome_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "🎓 Bienvenue dans votre système de gestion scolaire",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Utilisez le menu de navigation à gauche pour accéder aux différentes fonctionnalités :\n\n"
                        "• Inscription élève : Enregistrer un nouvel élève\n"
                        "• Gestion des élèves : Voir et modifier les informations des élèves\n"
                        "• Gestion des professeurs : Gérer le personnel enseignant\n"
                        "• Gestion des classes : Organiser les classes et emplois du temps",
                        size=14,
                        color="#64748b",
                        weight=ft.FontWeight.W_400
                    )
                ]),
                padding=28
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        welcome_container = ft.Container(
            content=welcome_card,
            padding=ft.padding.all(32)
        )
        
        # Assembler le contenu avec scrollbar
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    stats,
                    welcome_container
                ], scroll=ft.ScrollMode.AUTO),
                expand=True
            )
        ], spacing=0)
        
        self.page.update()
    
    def show_student_registration(self):
        """Afficher le formulaire d'inscription des élèves"""
        self.current_page = "student_registration"
        self.clear_main_content()
        
        # En-tête
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Inscription d'un élève",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1e293b"
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Formulaire
        form_content = self.create_registration_form()
        
        # Assembler le contenu avec scrollbar
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    form_content
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def create_registration_form(self):
        """Créer le formulaire d'inscription selon le design spécifié"""
        # Champs de saisie selon le design de l'image
        self.prenom_field = ft.TextField(
            label="Prénom *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.nom_field = ft.TextField(
            label="Nom *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        # Date de naissance avec formatage automatique
        self.dob_field = ft.TextField(
            label="Date de naissance *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            hint_text="jj/mm/aaaa",
            expand=True,
            on_change=self.format_date_input,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        # Initialiser le sélecteur de date si ce n'est pas déjà fait
        if not hasattr(self, 'date_picker') or self.date_picker is None:
            self.date_picker = ft.DatePicker(
                first_date=datetime(1900, 1, 1),
                last_date=datetime.now(),
                on_change=self.on_date_change,
            )
            if hasattr(self, 'page') and self.page and hasattr(self.page, 'overlay'):
                self.page.overlay.append(self.date_picker)
        
        self.lieu_naissance_field = ft.TextField(
            label="Lieu de naissance *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        # Champ ID auto-généré (non modifiable)
        students = self.data_manager.get_all_students()
        next_id = len(students)
        
        self.student_id_field = ft.TextField(
            label="ID",
            value=str(next_id),
            bgcolor="#f8fafc",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#e2e8f0",
            width=80,
            read_only=True,
            text_style=ft.TextStyle(color="#64748b", weight=ft.FontWeight.BOLD),
            text_align=ft.TextAlign.CENTER
        )
        
        self.numero_eleve_field = ft.TextField(
            label="Numéro d'élève",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.telephone_parent_field = ft.TextField(
            label="Téléphone parent *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.genre_dropdown = ft.Dropdown(
            label="Genre *",
            options=[
                ft.dropdown.Option("Masculin"),
                ft.dropdown.Option("Féminin"),
            ],
            value="Masculin",
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        # Récupérer les classes créées
        classes = self.data_manager.get_all_classes()
        class_options = []
        
        if classes:
            for classe in classes:
                class_options.append(ft.dropdown.Option(classe.get("nom", "")))
        else:
            # Si aucune classe n'existe, afficher un message d'aide
            class_options.append(ft.dropdown.Option("Aucune classe disponible"))
        
        self.classe_dropdown = ft.Dropdown(
            label="Classe *",
            hint_text="Sélectionner une classe" if classes else "Créez d'abord des classes dans 'Gestion des classes'",
            options=class_options,
            bgcolor="#ffffff",
            border_radius=8,
            expand=True,
            disabled=not classes  # Désactiver si aucune classe n'existe
        )
        
        # Bouton d'inscription
        submit_button = ft.ElevatedButton(
            "👤 Inscrire l'élève",
            bgcolor="#4285f4",
            color="#ffffff",
            height=48,
            width=200,
            on_click=self.save_student,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )
        
        # Créer le formulaire selon le design de l'image
        form_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    # Première ligne - Prénom, Nom et ID (petit à droite)
                    ft.Row([
                        ft.Container(self.prenom_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.nom_field, expand=1),
                        ft.Container(width=16),
                        self.student_id_field  # Petit champ fixe à droite
                    ]),
                    ft.Container(height=20),
                    
                    # Deuxième ligne - Date de naissance avec calendrier et Lieu de naissance
                    ft.Row([
                        ft.Container(
                            content=ft.Row([
                                ft.Container(self.dob_field, expand=1),
                                ft.IconButton(
                                    icon="calendar_today",
                                    icon_color="#4f46e5",
                                    tooltip="Choisir une date",
                                    on_click=self.open_date_picker
                                )
                            ], spacing=8),
                            expand=1
                        ),
                        ft.Container(width=16),
                        ft.Container(self.lieu_naissance_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Troisième ligne - Numéro d'élève et Téléphone parent
                    ft.Row([
                        ft.Container(self.numero_eleve_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.telephone_parent_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Quatrième ligne - Genre et Classe
                    ft.Row([
                        ft.Container(self.genre_dropdown, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.classe_dropdown, expand=1)
                    ]),
                    ft.Container(height=30),
                    
                    # Bouton d'inscription
                    ft.Row([
                        submit_button
                    ], alignment=ft.MainAxisAlignment.START)
                ]),
                padding=40,
                bgcolor="#ffffff",
                border_radius=12
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        return form_card
    
    def on_photo_selected(self, e: ft.FilePickerResultEvent):
        """Gérer la sélection de photo"""
        if e.files:
            file = e.files[0]
            # Copier le fichier vers le dossier photos
            os.makedirs("photos/students", exist_ok=True)
            
            # Générer un nom unique pour la photo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_extension = os.path.splitext(file.name)[1]
            new_filename = f"student_{timestamp}{file_extension}"
            new_path = f"photos/students/{new_filename}"
            
            try:
                shutil.copy2(file.path, new_path)
                self.photo_path = new_path
                
                # Afficher l'aperçu de la photo
                self.photo_display.content = ft.Image(
                    src=new_path,
                    width=120,
                    height=120,
                    fit=ft.ImageFit.COVER,
                    border_radius=8
                )
                self.page.update()
                
            except Exception as ex:
                self.show_snackbar(f"Erreur lors du téléchargement de la photo: {str(ex)}", error=True)
    
    def save_student(self, e):
        """Enregistrer un nouvel élève"""
        # Validation des champs obligatoires
        if not self.prenom_field.value:
            self.show_snackbar("Le prénom est obligatoire", error=True)
            return
        
        if not self.nom_field.value:
            self.show_snackbar("Le nom est obligatoire", error=True)
            return
        
        if not self.classe_dropdown.value or self.classe_dropdown.value == "Aucune classe disponible":
            self.show_snackbar("Veuillez sélectionner une classe valide ou créer des classes dans 'Gestion des classes'", error=True)
            return
        
        if not self.dob_field.value:
            self.show_snackbar("La date de naissance est obligatoire", error=True)
            return
        
        if not self.lieu_naissance_field.value:
            self.show_snackbar("Le lieu de naissance est obligatoire", error=True)
            return
        
        if not self.telephone_parent_field.value:
            self.show_snackbar("Le téléphone parent est obligatoire", error=True)
            return
        
        # Utiliser l'ID séquentiel
        student_id = int(self.student_id_field.value)
        
        # Créer l'objet étudiant
        student_data = {
            "id": student_id,
            "student_id": student_id,  # ID séquentiel pour affichage
            "prenom": self.prenom_field.value.strip(),
            "nom": self.nom_field.value.strip(),
            "nom_complet": f"{self.prenom_field.value.strip()} {self.nom_field.value.strip()}",
            "date_naissance": self.dob_field.value,
            "lieu_naissance": self.lieu_naissance_field.value.strip(),
            "numero_eleve": self.numero_eleve_field.value.strip() if self.numero_eleve_field.value else f"E{student_id:03d}",
            "telephone_parent": self.telephone_parent_field.value.strip(),
            "genre": self.genre_dropdown.value,
            "classe": self.classe_dropdown.value,
            "date_creation": datetime.now().isoformat()
        }
        
        # Sauvegarder l'élève
        if self.data_manager.add_student(student_data):
            self.show_snackbar("Élève inscrit avec succès!")
            self.reset_form(None)
        else:
            self.show_snackbar("Erreur lors de l'inscription", error=True)
    
    def reset_form(self, e):
        """Réinitialiser le formulaire""" 
        self.prenom_field.value = ""
        self.nom_field.value = ""
        self.dob_field.value = ""
        self.lieu_naissance_field.value = ""
        self.numero_eleve_field.value = ""
        self.telephone_parent_field.value = ""
        self.genre_dropdown.value = "Masculin"
        self.classe_dropdown.value = None
        
        # Mettre à jour l'ID pour le prochain élève
        students = self.data_manager.get_all_students()
        next_id = len(students)
        self.student_id_field.value = str(next_id)
        
        self.page.update()
    
    def show_student_management(self):
        """Afficher la gestion des élèves"""
        self.current_page = "student_management"
        self.clear_main_content()
        
        # Récupérer les classes disponibles
        classes = self.data_manager.get_all_classes()
        class_options = [ft.dropdown.Option("Toutes les classes")]
        
        if classes:
            for classe in classes:
                class_options.append(ft.dropdown.Option(classe.get("nom", "")))
        
        # Sélecteur de classe
        self.class_filter_dropdown = ft.Dropdown(
            label="Sélectionner une classe",
            options=class_options,
            value="Toutes les classes",
            bgcolor="#ffffff",
            border_radius=8,
            width=250,
            on_change=self.filter_students_by_class
        )
        
        # En-tête
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text(
                            "Gestion des élèves",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        ),
                        ft.Text(
                            "Consulter et modifier les informations des élèves",
                            size=15,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        )
                    ], expand=True),
                    ft.ElevatedButton(
                        "Nouvel élève",
                        icon="person_add",
                        on_click=lambda _: self.show_student_registration(),
                        bgcolor="#4f46e5",
                        color="#ffffff"
                    )
                ]),
                ft.Container(height=20),
                ft.Row([
                    self.class_filter_dropdown
                ])
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Table des élèves (sera mise à jour par le filtre)
        self.students_table_container = ft.Container()
        self.filter_students_by_class(None)  # Charger tous les élèves initialement
        
        # Assembler le contenu avec scrollbar
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=self.students_table_container,
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def filter_students_by_class(self, e):
        """Filtrer les élèves par classe sélectionnée"""
        selected_class = self.class_filter_dropdown.value if hasattr(self, 'class_filter_dropdown') else "Toutes les classes"
        
        if selected_class == "Toutes les classes":
            students = self.data_manager.get_all_students()
        else:
            students = self.data_manager.get_students_by_class(selected_class)
        
        # Trier les étudiants par ID
        students.sort(key=lambda x: x.get("student_id", x.get("id", 0)))
        
        # Créer la table avec scrollbars
        students_table = self.create_filtered_students_table(students, selected_class)
        self.students_table_container.content = students_table
        
        if hasattr(self, 'page') and self.page:
            self.page.update()
    
    def create_filtered_students_table(self, students, selected_class):
        """Créer la table des élèves filtrée avec scrollbars"""
        
        if not students:
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon("school", size=64, color="#cbd5e1"),
                        ft.Container(height=16),
                        ft.Text(
                            f"Aucun élève trouvé" + (f" dans la classe '{selected_class}'" if selected_class != "Toutes les classes" else ""),
                            size=16,
                            color="#64748b",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=16),
                        ft.ElevatedButton(
                            "Inscrire un élève",
                            icon="person_add",
                            on_click=lambda _: self.show_student_registration(),
                            bgcolor="#4f46e5",
                            color="#ffffff"
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40,
                    alignment=ft.alignment.center
                ),
                elevation=0,
                surface_tint_color="#ffffff",
                color="#ffffff"
            )
        
        # Créer les lignes du tableau (sans colonne classe si classe spécifique sélectionnée)
        rows = []
        for student in students:
            student_id = student.get("student_id", student.get("id", ""))
            
            row_cells = [
                ft.DataCell(ft.Text(str(student_id), size=12, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(student.get("nom_complet", ""), size=12, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(student.get("numero_eleve", ""), size=12)),
                ft.DataCell(ft.Text(student.get("telephone_parent", ""), size=12)),
            ]
            
            # Ajouter la colonne classe seulement si "Toutes les classes" est sélectionné
            if selected_class == "Toutes les classes":
                row_cells.append(ft.DataCell(ft.Text(student.get("classe", ""), size=12)))
            
            row_cells.extend([
                ft.DataCell(ft.Text(student.get("date_naissance", ""), size=12)),
                ft.DataCell(ft.Text(student.get("genre", ""), size=12)),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon="edit",
                            icon_color="#4f46e5",
                            tooltip="Modifier",
                            icon_size=16,
                            on_click=lambda e, student_id=student.get("id"): self.edit_student(student_id)
                        ),
                        ft.IconButton(
                            icon="delete",
                            icon_color="#ef4444",
                            tooltip="Supprimer",
                            icon_size=16,
                            on_click=lambda e, student_id=student.get("id"): self.delete_student(student_id)
                        )
                    ], spacing=0)
                )
            ])
            
            rows.append(ft.DataRow(row_cells))
        
        # Colonnes (sans classe si classe spécifique sélectionnée)
        columns = [
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Nom complet", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("N° Élève", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("N° Parent", weight=ft.FontWeight.BOLD, size=12)),
        ]
        
        if selected_class == "Toutes les classes":
            columns.append(ft.DataColumn(ft.Text("Classe", weight=ft.FontWeight.BOLD, size=12)))
        
        columns.extend([
            ft.DataColumn(ft.Text("Date naissance", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Genre", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD, size=12))
        ])
        
        data_table = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, "#e2e8f0"),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, "#f1f5f9"),
            horizontal_lines=ft.border.BorderSide(1, "#f1f5f9"),
            heading_row_color="#f8fafc"
        )
        
        # Container avec scrollbars horizontal et vertical
        scrollable_table = ft.Container(
            content=data_table,
            border_radius=8,
            bgcolor="#ffffff",
            padding=0
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            f"Total: {len(students)} élève(s)" + (f" - Classe: {selected_class}" if selected_class != "Toutes les classes" else ""),
                            size=14,
                            color="#64748b",
                            weight=ft.FontWeight.W_500
                        )
                    ]),
                    ft.Container(height=16),
                    ft.Container(
                        content=scrollable_table,
                        height=400,  # Hauteur fixe pour permettre le scroll vertical
                        border_radius=8,
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    )
                ], scroll=ft.ScrollMode.AUTO),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
    
    def create_students_table(self):
        """Créer le tableau des élèves"""
        students = self.data_manager.get_all_students()
        
        if not students:
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("👥", size=64, color="#94a3b8"),
                        ft.Container(height=16),
                        ft.Text(
                            "Aucun élève enregistré",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#64748b"
                        ),
                        ft.Text(
                            "Commencez par ajouter votre premier élève",
                            size=14,
                            color="#94a3b8"
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=64,
                    alignment=ft.alignment.center
                ),
                elevation=0,
                surface_tint_color="#ffffff",
                color="#ffffff"
            )
        
        # Créer les lignes du tableau
        rows = []
        for student in students:
            rows.append(
                ft.DataRow([
                    ft.DataCell(ft.Text(student.get("registration_no", ""), size=12)),
                    ft.DataCell(ft.Text(student.get("nom_complet", ""), size=12, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(student.get("classe", ""), size=12)),
                    ft.DataCell(ft.Text(student.get("date_naissance", ""), size=12)),
                    ft.DataCell(ft.Text(student.get("genre", ""), size=12)),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon="📷",
                                icon_color="#4f46e5",
                                tooltip="Modifier",
                                on_click=lambda e, student_id=student.get("id"): self.edit_student(student_id)
                            ),
                            ft.IconButton(
                                icon="📷",
                                icon_color="#ef4444",
                                tooltip="Supprimer",
                                on_click=lambda e, student_id=student.get("id"): self.delete_student(student_id)
                            )
                        ], spacing=0)
                    )
                ])
            )
        
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("N° Inscription", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Nom complet", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Classe", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Date naissance", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Genre", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD, size=12))
            ],
            rows=rows,
            border=ft.border.all(1, "#e2e8f0"),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, "#f1f5f9"),
            horizontal_lines=ft.border.BorderSide(1, "#f1f5f9"),
            heading_row_color="#f8fafc"
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            f"Total: {len(students)} élève(s)",
                            size=14,
                            color="#64748b",
                            weight=ft.FontWeight.W_500
                        )
                    ]),
                    ft.Container(height=16),
                    ft.Container(
                        content=data_table,
                        border_radius=8,
                        bgcolor="#ffffff"
                    )
                ]),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
    
    def edit_student(self, student_id):
        """Modifier un élève"""
        student = self.data_manager.get_student(student_id)
        if student:
            # Pré-remplir le formulaire avec les données existantes
            self.selected_student_id = student_id
            self.show_student_registration()
            
            # Remplir les champs après affichage
            self.reg_no_field.value = student.get("registration_no", "")
            self.date_field.value = student.get("date_inscription", "")
            self.name_field.value = student.get("nom_complet", "")
            self.class_dropdown.value = student.get("classe", "")
            self.dob_field.value = student.get("date_naissance", "")
            self.religion_field.value = student.get("religion", "")
            self.gender_dropdown.value = student.get("genre", "Masculin")
            self.skills_field.value = student.get("competences", "")
            self.father_name_field.value = student.get("nom_pere", "")
            self.mother_name_field.value = student.get("nom_mere", "")
            self.father_occupation_field.value = student.get("profession_pere", "")
            self.mother_occupation_field.value = student.get("profession_mere", "")
            
            # Charger la photo si elle existe
            if student.get("photo_path") and os.path.exists(student.get("photo_path")):
                self.photo_path = student.get("photo_path")
                self.photo_display.content = ft.Image(
                    src=self.photo_path,
                    width=120,
                    height=120,
                    fit=ft.ImageFit.COVER,
                    border_radius=8
                )
            
            self.page.update()
    
    def delete_student(self, student_id):
        """Supprimer un élève"""
        def confirm_delete(e):
            if self.data_manager.delete_student(student_id):
                self.show_snackbar("Élève supprimé avec succès!")
                self.show_student_management()
            else:
                self.show_snackbar("Erreur lors de la suppression", error=True)
            dialog.open = False
            self.page.update()
        
        def cancel_delete(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmer la suppression"),
            content=ft.Text("Êtes-vous sûr de vouloir supprimer cet élève ? Cette action est irréversible."),
            actions=[
                ft.TextButton("Annuler", on_click=cancel_delete),
                ft.TextButton("Supprimer", on_click=confirm_delete, style=ft.ButtonStyle(color="#ef4444"))
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_teacher_registration(self):
        """Afficher le formulaire d'inscription des professeurs"""
        self.current_page = "teacher_registration"
        self.clear_main_content()
        
        # En-tête
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Inscription professeur",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1e293b"
                ),
                ft.Text(
                    "Enregistrer un nouveau professeur dans le système",
                    size=15,
                    color="#64748b",
                    weight=ft.FontWeight.W_400
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Formulaire professeur
        form_content = self.create_teacher_form()
        
        # Assembler le contenu avec scrollbar
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    form_content
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def create_teacher_form(self):
        """Créer le formulaire d'inscription professeur"""
        # Générer automatiquement l'ID professeur
        teachers = self.data_manager.get_all_teachers()
        next_id = len(teachers) + 1
        auto_teacher_id = f"PROF{next_id:04d}"
        
        # Champs de saisie
        self.teacher_id_field = ft.TextField(
            label="ID Professeur",
            value=auto_teacher_id,
            bgcolor="#ffffff",
            border_radius=8,
            read_only=True
        )
        
        self.teacher_name_field = ft.TextField(
            label="Nom complet *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5"
        )
        
        self.teacher_subject_field = ft.TextField(
            label="Matière enseignée *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5"
        )
        
        self.teacher_email_field = ft.TextField(
            label="Email",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5"
        )
        
        self.teacher_phone_field = ft.TextField(
            label="Téléphone",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5"
        )
        
        self.teacher_qualification_field = ft.TextField(
            label="Qualifications",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            multiline=True,
            min_lines=2,
            max_lines=3
        )
        
        # Boutons d'action
        save_teacher_button = ft.ElevatedButton(
            "Enregistrer le professeur",
            icon="📷",
            on_click=self.save_teacher,
            bgcolor="#4f46e5",
            color="#ffffff",
            height=48
        )
        
        reset_teacher_button = ft.OutlinedButton(
            "Réinitialiser",
            icon="📷",
            on_click=self.reset_teacher_form,
            height=48
        )
        
        # Layout du formulaire
        form_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Informations du professeur",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Container(height=16),
                    
                    ft.Row([
                        ft.Container(self.teacher_id_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.teacher_name_field, expand=1)
                    ]),
                    ft.Container(height=16),
                    ft.Row([
                        ft.Container(self.teacher_subject_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.teacher_email_field, expand=1)
                    ]),
                    ft.Container(height=16),
                    ft.Row([
                        ft.Container(self.teacher_phone_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(width=200)  # Spacer
                    ]),
                    ft.Container(height=16),
                    self.teacher_qualification_field,
                    
                    ft.Container(height=32),
                    ft.Row([
                        save_teacher_button,
                        ft.Container(width=16),
                        reset_teacher_button
                    ], alignment=ft.MainAxisAlignment.START)
                ]),
                padding=32
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        return form_card
    
    def save_teacher(self, e):
        """Enregistrer un nouveau professeur"""
        # Validation
        if not self.teacher_name_field.value:
            self.show_snackbar("Le nom du professeur est obligatoire", error=True)
            return
        
        if not self.teacher_subject_field.value:
            self.show_snackbar("La matière enseignée est obligatoire", error=True)
            return
        
        # Créer l'objet professeur
        teacher_data = {
            "id": self.teacher_id_field.value,
            "nom_complet": self.teacher_name_field.value,
            "matiere": self.teacher_subject_field.value,
            "email": self.teacher_email_field.value or "",
            "telephone": self.teacher_phone_field.value or "",
            "qualifications": self.teacher_qualification_field.value or "",
            "date_creation": datetime.now().isoformat()
        }
        
        # Sauvegarder le professeur
        if self.data_manager.add_teacher(teacher_data):
            self.show_snackbar("Professeur enregistré avec succès!")
            self.reset_teacher_form(None)
        else:
            self.show_snackbar("Erreur lors de l'enregistrement", error=True)
    
    def reset_teacher_form(self, e):
        """Réinitialiser le formulaire professeur"""
        self.teacher_name_field.value = ""
        self.teacher_subject_field.value = ""
        self.teacher_email_field.value = ""
        self.teacher_phone_field.value = ""
        self.teacher_qualification_field.value = ""
        
        # Générer un nouvel ID
        teachers = self.data_manager.get_all_teachers()
        next_id = len(teachers) + 1
        self.teacher_id_field.value = f"PROF{next_id:04d}"
        
        self.page.update()
    
    def show_teacher_management(self):
        """Afficher la gestion des professeurs"""
        self.current_page = "teacher_management"
        self.clear_main_content()
        
        # En-tête
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(
                        "Gestion des professeurs",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Text(
                        "Consulter et modifier les informations des professeurs",
                        size=15,
                        color="#64748b",
                        weight=ft.FontWeight.W_400
                    )
                ], expand=True),
                ft.ElevatedButton(
                    "Nouveau professeur",
                    icon="📷",
                    on_click=lambda _: self.show_teacher_registration(),
                    bgcolor="#4f46e5",
                    color="#ffffff"
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Table des professeurs
        teachers_table = self.create_teachers_table()
        
        # Assembler le contenu avec scrollbar
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    teachers_table
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def create_teachers_table(self):
        """Créer le tableau des professeurs"""
        teachers = self.data_manager.get_all_teachers()
        
        if not teachers:
            return ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("🏫", size=64, color="#94a3b8"),
                        ft.Container(height=16),
                        ft.Text(
                            "Aucun professeur enregistré",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#64748b"
                        ),
                        ft.Text(
                            "Commencez par ajouter votre premier professeur",
                            size=14,
                            color="#94a3b8"
                        )
                    ], 
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=64,
                    alignment=ft.alignment.center
                ),
                elevation=0,
                surface_tint_color="#ffffff",
                color="#ffffff"
            )
        
        # Créer les lignes du tableau
        rows = []
        for teacher in teachers:
            rows.append(
                ft.DataRow([
                    ft.DataCell(ft.Text(teacher.get("id", ""), size=12)),
                    ft.DataCell(ft.Text(teacher.get("nom_complet", ""), size=12, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(teacher.get("matiere", ""), size=12)),
                    ft.DataCell(ft.Text(teacher.get("email", ""), size=12)),
                    ft.DataCell(ft.Text(teacher.get("telephone", ""), size=12)),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon="📷",
                                icon_color="#4f46e5",
                                tooltip="Modifier",
                                on_click=lambda e, teacher_id=teacher.get("id"): self.edit_teacher(teacher_id)
                            ),
                            ft.IconButton(
                                icon="📷",
                                icon_color="#ef4444",
                                tooltip="Supprimer",
                                on_click=lambda e, teacher_id=teacher.get("id"): self.delete_teacher(teacher_id)
                            )
                        ], spacing=0)
                    )
                ])
            )
        
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Nom complet", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Matière", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Email", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Téléphone", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD, size=12))
            ],
            rows=rows,
            border=ft.border.all(1, "#e2e8f0"),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, "#f1f5f9"),
            horizontal_lines=ft.border.BorderSide(1, "#f1f5f9"),
            heading_row_color="#f8fafc"
        )
        
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            f"Total: {len(teachers)} professeur(s)",
                            size=14,
                            color="#64748b",
                            weight=ft.FontWeight.W_500
                        )
                    ]),
                    ft.Container(height=16),
                    ft.Container(
                        content=data_table,
                        border_radius=8,
                        bgcolor="#ffffff"
                    )
                ]),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
    
    def edit_teacher(self, teacher_id):
        """Modifier un professeur"""
        teacher = self.data_manager.get_teacher(teacher_id)
        if teacher:
            self.selected_teacher_id = teacher_id
            self.show_teacher_registration()
            
            # Remplir les champs
            self.teacher_id_field.value = teacher.get("id", "")
            self.teacher_name_field.value = teacher.get("nom_complet", "")
            self.teacher_subject_field.value = teacher.get("matiere", "")
            self.teacher_email_field.value = teacher.get("email", "")
            self.teacher_phone_field.value = teacher.get("telephone", "")
            self.teacher_qualification_field.value = teacher.get("qualifications", "")
            
            self.page.update()
    
    def delete_teacher(self, teacher_id):
        """Supprimer un professeur"""
        def confirm_delete(e):
            if self.data_manager.delete_teacher(teacher_id):
                self.show_snackbar("Professeur supprimé avec succès!")
                self.show_teacher_management()
            else:
                self.show_snackbar("Erreur lors de la suppression", error=True)
            dialog.open = False
            self.page.update()
        
        def cancel_delete(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmer la suppression"),
            content=ft.Text("Êtes-vous sûr de vouloir supprimer ce professeur ? Cette action est irréversible."),
            actions=[
                ft.TextButton("Annuler", on_click=cancel_delete),
                ft.TextButton("Supprimer", on_click=confirm_delete, style=ft.ButtonStyle(color="#ef4444"))
            ]
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_class_management(self):
        """Afficher la gestion des classes"""
        self.current_page = "class_management"
        self.clear_main_content()
        
        # En-tête
        header = ft.Container(
            content=ft.Row([
                ft.Column([
                    ft.Text(
                        "Gestion des classes",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Text(
                        "Créer et gérer les classes de l'établissement",
                        size=15,
                        color="#64748b",
                        weight=ft.FontWeight.W_400
                    )
                ], expand=True),
                ft.ElevatedButton(
                    "➕ Créer une classe",
                    bgcolor="#4f46e5",
                    color="#ffffff",
                    height=40,
                    on_click=self.show_create_class_dialog,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8)
                    )
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Liste des classes
        self.classes_list = ft.Column(
            spacing=12,
            scroll=ft.ScrollMode.AUTO
        )
        
        # Charger les classes existantes
        self.load_classes()
        
        # Contenu principal
        content = ft.Container(
            content=self.classes_list,
            padding=ft.padding.all(32),
            expand=True
        )
        
        self.main_content.content = ft.Column([
            header,
            content
        ])
        
        self.page.update()
    
    def load_classes(self):
        """Charger et afficher la liste des classes"""
        classes = self.data_manager.get_all_classes()
        self.classes_list.controls.clear()
        
        if not classes:
            # Message si aucune classe n'existe
            empty_message = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon("school", size=48, color="#94a3b8"),
                        ft.Text(
                            "Aucune classe créée",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#64748b",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Text(
                            "Cliquez sur 'Créer une classe' pour commencer",
                            size=14,
                            color="#94a3b8",
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=16),
                    padding=40,
                    alignment=ft.alignment.center
                ),
                elevation=0,
                surface_tint_color="#ffffff",
                color="#ffffff"
            )
            self.classes_list.controls.append(empty_message)
        else:
            for classe in classes:
                student_count = self.data_manager.get_students_count_in_class(classe.get("nom", ""))
                class_card = self.create_class_card(classe, student_count)
                self.classes_list.controls.append(class_card)
    
    def create_class_card(self, classe, student_count):
        """Créer une carte pour une classe"""
        return ft.Card(
            content=ft.Container(
                content=ft.Row([
                    # Informations de la classe
                    ft.Column([
                        ft.Text(
                            classe.get("nom", ""),
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        ),
                        ft.Text(
                            f"{student_count} élève(s)",
                            size=14,
                            color="#64748b"
                        ),
                        ft.Text(
                            f"Créée le: {classe.get('date_creation', 'Date inconnue')[:10] if classe.get('date_creation') else 'Date inconnue'}",
                            size=12,
                            color="#94a3b8"
                        )
                    ], expand=True),
                    
                    # Actions
                    ft.Row([
                        ft.IconButton(
                            icon="edit",
                            icon_color="#4f46e5",
                            tooltip="Modifier la classe",
                            on_click=lambda e, c=classe: self.show_edit_class_dialog(c)
                        ),
                        ft.IconButton(
                            icon="delete",
                            icon_color="#ef4444",
                            tooltip="Supprimer la classe",
                            on_click=lambda e, c=classe: self.confirm_delete_class(c)
                        )
                    ], spacing=8)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
    
    def show_create_class_dialog(self, e):
        """Afficher le popup de création de classe"""
        print("show_create_class_dialog appelé")
        
        self.class_name_field = ft.TextField(
            label="Nom de la classe *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            width=300,
            autofocus=True
        )
        
        self.create_class_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Créer une nouvelle classe"),
            content=ft.Container(
                content=ft.Column([
                    self.class_name_field,
                    ft.Container(height=8),
                    ft.Text(
                        "Saisissez le nom de la classe (ex: CP, CE1, 6ème, etc.)",
                        size=12,
                        color="#64748b"
                    )
                ], tight=True),
                width=300,
                height=120
            ),
            actions=[
                ft.TextButton("Annuler", on_click=self.close_create_class_dialog),
                ft.ElevatedButton(
                    "Créer",
                    bgcolor="#4f46e5",
                    color="#ffffff",
                    on_click=self.create_class
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        print("Ouverture du popup...")
        self.page.open(self.create_class_dialog)
    
    def close_create_class_dialog(self, e):
        """Fermer le popup de création de classe"""
        print("Fermeture popup création classe")
        self.page.close(self.create_class_dialog)
    
    def create_class(self, e):
        """Créer une nouvelle classe"""
        print("Tentative de création de classe")
        
        if not self.class_name_field.value or not self.class_name_field.value.strip():
            self.show_snackbar("Le nom de la classe est obligatoire", error=True)
            return
        
        # Générer un ID unique basé sur le nom
        class_name = self.class_name_field.value.strip()
        class_id = class_name.upper().replace(" ", "_").replace("È", "E").replace("É", "E")
        
        class_data = {
            "id": class_id,
            "nom": class_name,
            "date_creation": datetime.now().isoformat()
        }
        
        print(f"Données classe: {class_data}")
        
        if self.data_manager.add_class(class_data):
            self.show_snackbar("Classe créée avec succès!")
            print("Classe sauvegardée, fermeture popup")
            self.page.close(self.create_class_dialog)
            self.load_classes()  # Recharger la liste des classes
            self.page.update()
        else:
            self.show_snackbar("Une classe avec ce nom existe déjà", error=True)
    
    def show_edit_class_dialog(self, classe):
        """Afficher le popup de modification de classe"""
        print(f"show_edit_class_dialog appelé pour {classe['nom']}")
        self.editing_class = classe
        
        self.class_name_field = ft.TextField(
            label="Nom de la classe *",
            value=classe.get("nom", ""),
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            width=300,
            autofocus=True
        )
        
        self.edit_class_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Modifier la classe '{classe['nom']}'"),
            content=ft.Container(
                content=ft.Column([
                    self.class_name_field,
                    ft.Container(height=8),
                    ft.Text(
                        "Modifiez le nom de la classe",
                        size=12,
                        color="#64748b"
                    )
                ], tight=True),
                width=300,
                height=120
            ),
            actions=[
                ft.TextButton("Annuler", on_click=self.close_edit_class_dialog),
                ft.ElevatedButton(
                    "Modifier",
                    bgcolor="#4f46e5",
                    color="#ffffff",
                    on_click=self.update_class
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        print("Ouverture du popup de modification...")
        self.page.open(self.edit_class_dialog)
    
    def close_edit_class_dialog(self, e):
        """Fermer le popup de modification de classe"""
        print("Fermeture popup modification classe")
        self.page.close(self.edit_class_dialog)
    
    def update_class(self, e):
        """Mettre à jour une classe existante"""
        print("Tentative de modification de classe")
        
        if not self.class_name_field.value or not self.class_name_field.value.strip():
            self.show_snackbar("Le nom de la classe est obligatoire", error=True)
            return
        
        class_data = {
            "nom": self.class_name_field.value.strip()
        }
        
        if self.data_manager.update_class(self.editing_class["id"], class_data):
            self.show_snackbar("Classe modifiée avec succès!")
            print("Classe modifiée, fermeture popup")
            self.page.close(self.edit_class_dialog)
            self.load_classes()  # Recharger la liste des classes
            self.page.update()
        else:
            self.show_snackbar("Erreur lors de la modification", error=True)
    
    def confirm_delete_class(self, classe):
        """Confirmer la suppression d'une classe"""
        print(f"confirm_delete_class appelé pour {classe['nom']}")
        student_count = self.data_manager.get_students_count_in_class(classe.get("nom", ""))
        
        message = f"Êtes-vous sûr de vouloir supprimer la classe '{classe.get('nom', '')}'?"
        if student_count > 0:
            message += f"\n\nAttention: Cette classe contient {student_count} élève(s). Ils devront être réassignés à d'autres classes."
        
        self.delete_class_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmer la suppression"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Annuler", on_click=self.close_delete_class_dialog),
                ft.ElevatedButton(
                    "Supprimer",
                    bgcolor="#ef4444",
                    color="#ffffff",
                    on_click=lambda e: self.delete_class(classe)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        print("Ouverture du popup de confirmation de suppression...")
        self.page.open(self.delete_class_dialog)
    
    def close_delete_class_dialog(self, e):
        """Fermer le popup de confirmation de suppression"""
        print("Fermeture popup suppression classe")
        self.page.close(self.delete_class_dialog)
    
    def delete_class(self, classe):
        """Supprimer une classe"""
        print(f"Suppression de la classe {classe['nom']}")
        if self.data_manager.delete_class(classe["id"]):
            self.show_snackbar("Classe supprimée avec succès!")
            print("Classe supprimée, fermeture popup")
            self.page.close(self.delete_class_dialog)
            self.load_classes()  # Recharger la liste des classes
            self.page.update()
        else:
            self.show_snackbar("Erreur lors de la suppression", error=True)
    
    def close_class_dialog(self, e):
        """Fermer le dialog de classe"""
        if hasattr(self, 'page') and self.page and hasattr(self.page, 'dialog') and self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    def show_grade_management(self):
        """Afficher la gestion des notes"""
        self.current_page = "grade_management"
        self.clear_main_content()
        
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Gestion des notes",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1e293b"
                ),
                ft.Text(
                    "Saisir et consulter les notes des élèves",
                    size=15,
                    color="#64748b",
                    weight=ft.FontWeight.W_400
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "📊 Gestion des notes",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Cette section permettra de :\n\n"
                        "• Saisir les notes par matière\n"
                        "• Calculer les moyennes\n"
                        "• Générer les bulletins\n"
                        "• Suivre les progressions",
                        size=14,
                        color="#64748b"
                    )
                ]),
                padding=32
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=content,
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def show_schedule(self):
        """Afficher l'emploi du temps"""
        self.current_page = "schedule"
        self.clear_main_content()
        
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Emploi du temps",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1e293b"
                ),
                ft.Text(
                    "Gérer les horaires et plannings",
                    size=15,
                    color="#64748b",
                    weight=ft.FontWeight.W_400
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "📅 Emploi du temps",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Cette section permettra de :\n\n"
                        "• Créer les emplois du temps\n"
                        "• Affecter les créneaux aux professeurs\n"
                        "• Gérer les salles de classe\n"
                        "• Planifier les examens",
                        size=14,
                        color="#64748b"
                    )
                ]),
                padding=32
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=content,
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def show_attendance(self):
        """Afficher la gestion des présences"""
        self.current_page = "attendance"
        self.clear_main_content()
        
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Gestion des présences",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1e293b"
                ),
                ft.Text(
                    "Suivre les présences et absences",
                    size=15,
                    color="#64748b",
                    weight=ft.FontWeight.W_400
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "✅ Gestion des présences",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Cette section permettra de :\n\n"
                        "• Prendre les présences quotidiennes\n"
                        "• Justifier les absences\n"
                        "• Générer des rapports d'assiduité\n"
                        "• Alerter les parents",
                        size=14,
                        color="#64748b"
                    )
                ]),
                padding=32
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=content,
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def format_date_input(self, e):
        """Formater automatiquement la saisie de date"""
        value = e.control.value
        if not value:
            return
        
        # Supprimer tous les caractères non numériques
        digits_only = ''.join(filter(str.isdigit, value))
        
        # Formater automatiquement avec des /
        if len(digits_only) <= 2:
            formatted = digits_only
        elif len(digits_only) <= 4:
            formatted = f"{digits_only[:2]}/{digits_only[2:]}"
        elif len(digits_only) <= 8:
            formatted = f"{digits_only[:2]}/{digits_only[2:4]}/{digits_only[4:]}"
        else:
            # Limiter à 8 chiffres (jj/mm/aaaa)
            digits_only = digits_only[:8]
            formatted = f"{digits_only[:2]}/{digits_only[2:4]}/{digits_only[4:]}"
        
        # Mettre à jour le champ si le formatage a changé
        if formatted != value:
            e.control.value = formatted
            self.page.update()
    
    def open_date_picker(self, e):
        """Ouvrir le sélecteur de date"""
        if hasattr(self, 'date_picker') and self.date_picker:
            self.date_picker.open = True
            self.page.update()
    
    def on_date_change(self, e):
        """Gérer le changement de date depuis le calendrier"""
        if e.control.value:
            # Formater la date sélectionnée
            selected_date = e.control.value
            formatted_date = selected_date.strftime("%d/%m/%Y")
            self.dob_field.value = formatted_date
            self.page.update()

    def show_snackbar(self, message: str, error: bool = False):
        """Afficher un message de notification"""
        color = "#ef4444" if error else "#10b981"
        icon = "❌" if error else "✅"
        
        snackbar = ft.SnackBar(
            content=ft.Row([
                ft.Text(icon, color="white", size=20),
                ft.Text(message, color="white", weight=ft.FontWeight.W_500)
            ]),
            bgcolor=color,
            duration=3000
        )
        
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()

def main(page: ft.Page):
    app = StudentRegistrationSystem()
    app.main(page)

if __name__ == "__main__":
    ft.app(target=main, port=5000, view=ft.AppView.WEB_BROWSER)
