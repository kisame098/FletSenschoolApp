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
        
        # Configuration des colonnes du tableau des élèves
        self.column_visibility = {
            "id": True,
            "prenom": True,
            "nom": True,
            "date_naissance": True,
            "lieu_naissance": False,  # Désactivé par défaut
            "genre": True,
            "classe": True,  # Géré dynamiquement selon le filtre
            "numero_eleve": True,
            "telephone_parent": True,
            "actions": True
        }
        
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
        
        # Champ ID auto-généré (non modifiable) - utilise la nouvelle méthode
        next_id = self.data_manager.get_next_student_id()
        
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
                    # Ligne ID - Champ ID déplacé vers le haut, aligné à droite
                    ft.Row([
                        ft.Container(expand=1),  # Espace vide à gauche
                        self.student_id_field  # Petit champ fixe à droite
                    ]),
                    ft.Container(height=20),
                    
                    # Première ligne - Prénom et Nom
                    ft.Row([
                        ft.Container(self.prenom_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.nom_field, expand=1)
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
        """Enregistrer un nouvel élève avec logs détaillés"""
        print("=== DÉBUT INSCRIPTION ÉLÈVE ===")
        print(f"[LOG] Tentative d'inscription d'un nouvel élève à {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Validation des champs obligatoires avec logs
        print("[LOG] Validation des champs obligatoires...")
        
        if not self.prenom_field.value:
            print("[LOG] ERREUR: Prénom manquant")
            self.show_snackbar("Le prénom est obligatoire", error=True)
            return
        print(f"[LOG] Prénom validé: '{self.prenom_field.value.strip()}'")
        
        if not self.nom_field.value:
            print("[LOG] ERREUR: Nom manquant")
            self.show_snackbar("Le nom est obligatoire", error=True)
            return
        print(f"[LOG] Nom validé: '{self.nom_field.value.strip()}'")
        
        if not self.classe_dropdown.value or self.classe_dropdown.value == "Aucune classe disponible":
            print("[LOG] ERREUR: Classe manquante ou invalide")
            self.show_snackbar("Veuillez sélectionner une classe valide ou créer des classes dans 'Gestion des classes'", error=True)
            return
        print(f"[LOG] Classe validée: '{self.classe_dropdown.value}'")
        
        if not self.dob_field.value:
            print("[LOG] ERREUR: Date de naissance manquante")
            self.show_snackbar("La date de naissance est obligatoire", error=True)
            return
        print(f"[LOG] Date de naissance validée: '{self.dob_field.value}'")
        
        if not self.lieu_naissance_field.value:
            print("[LOG] ERREUR: Lieu de naissance manquant")
            self.show_snackbar("Le lieu de naissance est obligatoire", error=True)
            return
        print(f"[LOG] Lieu de naissance validé: '{self.lieu_naissance_field.value.strip()}'")
        
        if not self.telephone_parent_field.value:
            print("[LOG] ERREUR: Téléphone parent manquant")
            self.show_snackbar("Le téléphone parent est obligatoire", error=True)
            return
        print(f"[LOG] Téléphone parent validé: '{self.telephone_parent_field.value.strip()}'")
        
        print("[LOG] Tous les champs obligatoires sont valides ✓")
        
        # Générer l'ID avec la nouvelle méthode
        print("[LOG] Génération de l'ID élève...")
        student_id = self.data_manager.get_next_student_id()
        print(f"[LOG] ID généré automatiquement: {student_id}")
        
        # Créer l'objet étudiant
        print("[LOG] Construction des données de l'élève...")
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
        
        print(f"[LOG] Données complètes de l'élève:")
        for key, value in student_data.items():
            print(f"[LOG]   {key}: {value}")
        
        # Sauvegarder l'élève
        print("[LOG] Tentative de sauvegarde dans la base de données...")
        try:
            if self.data_manager.add_student(student_data):
                print(f"[LOG] SUCCESS: Élève inscrit avec succès - ID: {student_id}, Nom: {student_data['nom_complet']}")
                self.show_snackbar("Élève inscrit avec succès!")
                print("[LOG] Réinitialisation complète du formulaire...")
                
                # Forcer la reconstruction complète du formulaire d'inscription
                self.show_student_registration()
                print("[LOG] Formulaire complètement reconstruit avec succès")
            else:
                print("[LOG] ERREUR: Échec de la sauvegarde dans la base de données")
                self.show_snackbar("Erreur lors de l'inscription", error=True)
        except Exception as ex:
            print(f"[LOG] EXCEPTION lors de la sauvegarde: {str(ex)}")
            self.show_snackbar(f"Erreur technique: {str(ex)}", error=True)
        
        print("=== FIN INSCRIPTION ÉLÈVE ===\n")
    
    def reset_form(self, e):
        """Réinitialiser le formulaire avec logs""" 
        print("[LOG] Réinitialisation des champs du formulaire...")
        self.prenom_field.value = ""
        self.nom_field.value = ""
        self.dob_field.value = ""
        self.lieu_naissance_field.value = ""
        self.numero_eleve_field.value = ""
        self.telephone_parent_field.value = ""
        self.genre_dropdown.value = "Masculin"
        
        # Correction spéciale pour le dropdown classe : réinitialiser complètement
        print("[LOG] Réinitialisation spéciale du dropdown classe...")
        self.classe_dropdown.value = None
        
        # Mettre à jour l'ID pour le prochain élève avec la nouvelle méthode
        print("[LOG] Calcul du prochain ID disponible...")
        next_id = self.data_manager.get_next_student_id()
        self.student_id_field.value = str(next_id)
        print(f"[LOG] Prochain ID disponible: {next_id}")
        
        # Mise à jour complète de la page pour forcer le rafraîchissement visuel
        self.page.update()
        print("[LOG] Interface mise à jour avec réinitialisation complète")
    
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
        
        # Barre de recherche remplaçant le bouton "Nouvel élève"
        self.student_search_field = ft.TextField(
            label="Rechercher un élève...",
            hint_text="Saisir ID, nom, prénom ou nom complet",
            prefix_icon="search",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            width=350,
            on_change=self.search_students,
            autofocus=False
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
                    self.student_search_field
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
        
        # Assembler le contenu avec scrollbar comme les autres pages
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    self.students_table_container
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def search_students(self, e):
        """Rechercher des élèves par ID, nom, prénom ou nom complet"""
        search_term = self.student_search_field.value.strip().lower() if self.student_search_field.value else ""
        
        # Si le terme de recherche est vide, afficher tous les élèves selon le filtre de classe actuel
        if not search_term:
            self.filter_students_by_class(None)
            return
        
        # Récupérer tous les élèves selon le filtre de classe actuel
        selected_class = self.class_filter_dropdown.value if hasattr(self, 'class_filter_dropdown') else "Toutes les classes"
        
        if selected_class == "Toutes les classes":
            all_students = self.data_manager.get_all_students()
        else:
            all_students = self.data_manager.get_students_by_class(selected_class)
        
        # Filtrer les élèves selon le terme de recherche
        filtered_students = []
        for student in all_students:
            # Récupérer les champs de recherche
            student_id = str(student.get("student_id", student.get("id", ""))).lower()
            prenom = str(student.get("prenom", "")).lower()
            nom = str(student.get("nom", "")).lower()
            nom_complet = f"{prenom} {nom}".strip()
            numero_eleve = str(student.get("numero_eleve", "")).lower()
            
            # Vérifier si le terme de recherche correspond à l'un des champs
            if (search_term in student_id or 
                search_term in prenom or 
                search_term in nom or 
                search_term in nom_complet or
                search_term in numero_eleve):
                filtered_students.append(student)
        
        # Trier les résultats par ID
        def get_sort_key(student):
            student_id = student.get("student_id", student.get("id", 0))
            id_str = str(student_id)
            import re
            numbers = re.findall(r'\d+', id_str)
            if numbers:
                return int(numbers[0])
            else:
                return 0
        
        filtered_students.sort(key=get_sort_key)
        
        # Créer la table avec les résultats filtrés
        students_table = self.create_filtered_students_table(filtered_students, selected_class)
        self.students_table_container.content = students_table
        
        if hasattr(self, 'page') and self.page:
            self.page.update()
    
    def filter_students_by_class(self, e):
        """Filtrer les élèves par classe sélectionnée"""
        selected_class = self.class_filter_dropdown.value if hasattr(self, 'class_filter_dropdown') else "Toutes les classes"
        
        # Vérifier s'il y a un terme de recherche actif
        search_term = ""
        if hasattr(self, 'student_search_field') and self.student_search_field.value:
            search_term = self.student_search_field.value.strip().lower()
        
        # Récupérer les élèves selon la classe sélectionnée
        if selected_class == "Toutes les classes":
            students = self.data_manager.get_all_students()
        else:
            students = self.data_manager.get_students_by_class(selected_class)
        
        # Appliquer le filtre de recherche si un terme de recherche est actif
        if search_term:
            filtered_students = []
            for student in students:
                # Récupérer les champs de recherche
                student_id = str(student.get("student_id", student.get("id", ""))).lower()
                prenom = str(student.get("prenom", "")).lower()
                nom = str(student.get("nom", "")).lower()
                nom_complet = f"{prenom} {nom}".strip()
                numero_eleve = str(student.get("numero_eleve", "")).lower()
                
                # Vérifier si le terme de recherche correspond à l'un des champs
                if (search_term in student_id or 
                    search_term in prenom or 
                    search_term in nom or 
                    search_term in nom_complet or
                    search_term in numero_eleve):
                    filtered_students.append(student)
            students = filtered_students
        
        # Trier les étudiants par ID avec gestion des différents formats
        def get_sort_key(student):
            student_id = student.get("student_id", student.get("id", 0))
            # Convertir en chaîne puis extraire les chiffres pour le tri
            id_str = str(student_id)
            # Si l'ID contient des lettres (comme STU0001), extraire seulement les chiffres
            import re
            numbers = re.findall(r'\d+', id_str)
            if numbers:
                return int(numbers[0])  # Prendre le premier groupe de chiffres
            else:
                return 0  # Valeur par défaut si aucun chiffre trouvé
        
        students.sort(key=get_sort_key)
        
        # Créer la table avec scrollbars
        students_table = self.create_filtered_students_table(students, selected_class)
        self.students_table_container.content = students_table
        
        if hasattr(self, 'page') and self.page:
            self.page.update()
    
    def create_filtered_students_table(self, students, selected_class):
        """Créer la table des élèves filtrée avec scrollbars"""
        
        # Debug: afficher le nombre d'élèves reçus
        print(f"[DEBUG] create_filtered_students_table - Nombre d'élèves reçus: {len(students) if students else 0}")
        for i, student in enumerate(students or []):
            print(f"[DEBUG] Élève {i}: ID={student.get('id')}, nom_complet={student.get('nom_complet')}")
        
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
        
        # Créer les lignes du tableau avec gestion de la visibilité des colonnes
        rows = []
        for student in students:
            student_id = student.get("student_id", student.get("id", ""))
            row_cells = []
            
            # Construire les cellules selon la visibilité des colonnes
            # ID (toujours visible)
            if self.column_visibility.get("id", True):
                row_cells.append(ft.DataCell(ft.Text(str(student_id), size=12, weight=ft.FontWeight.BOLD)))
            
            # Prénom
            if self.column_visibility.get("prenom", True):
                row_cells.append(ft.DataCell(ft.Text(student.get("prenom", ""), size=12, weight=ft.FontWeight.W_500)))
            
            # Nom
            if self.column_visibility.get("nom", True):
                row_cells.append(ft.DataCell(ft.Text(student.get("nom", ""), size=12, weight=ft.FontWeight.W_500)))
            
            # Date de naissance
            if self.column_visibility.get("date_naissance", True):
                row_cells.append(ft.DataCell(ft.Text(student.get("date_naissance", ""), size=12)))
            
            # Lieu de naissance (après date de naissance)
            if self.column_visibility.get("lieu_naissance", False):
                row_cells.append(ft.DataCell(ft.Text(student.get("lieu_naissance", ""), size=12)))
            
            # Genre
            if self.column_visibility.get("genre", True):
                row_cells.append(ft.DataCell(ft.Text(student.get("genre", ""), size=12)))
            
            # Classe (seulement si "Toutes les classes" est sélectionné et colonne visible)
            if selected_class == "Toutes les classes" and self.column_visibility.get("classe", True):
                row_cells.append(ft.DataCell(ft.Text(student.get("classe", ""), size=12)))
            
            # N° Élève
            if self.column_visibility.get("numero_eleve", True):
                row_cells.append(ft.DataCell(ft.Text(student.get("numero_eleve", ""), size=12)))
            
            # N° Parent
            if self.column_visibility.get("telephone_parent", True):
                row_cells.append(ft.DataCell(ft.Text(student.get("telephone_parent", ""), size=12)))
            
            # Actions (toujours visibles)
            if self.column_visibility.get("actions", True):
                row_cells.append(ft.DataCell(
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
                ))
            
            rows.append(ft.DataRow(row_cells))
        
        # Créer les colonnes selon la visibilité configurée
        columns = []
        
        # ID (toujours visible)
        if self.column_visibility.get("id", True):
            columns.append(ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=12)))
        
        # Prénom
        if self.column_visibility.get("prenom", True):
            columns.append(ft.DataColumn(ft.Text("Prénom", weight=ft.FontWeight.BOLD, size=12)))
        
        # Nom
        if self.column_visibility.get("nom", True):
            columns.append(ft.DataColumn(ft.Text("Nom", weight=ft.FontWeight.BOLD, size=12)))
        
        # Date de naissance
        if self.column_visibility.get("date_naissance", True):
            columns.append(ft.DataColumn(ft.Text("Date naissance", weight=ft.FontWeight.BOLD, size=12)))
        
        # Lieu de naissance (après date de naissance)
        if self.column_visibility.get("lieu_naissance", False):
            columns.append(ft.DataColumn(ft.Text("Lieu naissance", weight=ft.FontWeight.BOLD, size=12)))
        
        # Genre
        if self.column_visibility.get("genre", True):
            columns.append(ft.DataColumn(ft.Text("Genre", weight=ft.FontWeight.BOLD, size=12)))
        
        # Classe (seulement si "Toutes les classes" est sélectionné et colonne visible)
        if selected_class == "Toutes les classes" and self.column_visibility.get("classe", True):
            columns.append(ft.DataColumn(ft.Text("Classe", weight=ft.FontWeight.BOLD, size=12)))
        
        # N° Élève
        if self.column_visibility.get("numero_eleve", True):
            columns.append(ft.DataColumn(ft.Text("N° Élève", weight=ft.FontWeight.BOLD, size=12)))
        
        # N° Parent
        if self.column_visibility.get("telephone_parent", True):
            columns.append(ft.DataColumn(ft.Text("N° Parent", weight=ft.FontWeight.BOLD, size=12)))
        
        # Actions (toujours visibles)
        if self.column_visibility.get("actions", True):
            columns.append(ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD, size=12)))
        
        data_table = ft.DataTable(
            columns=columns,
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
                            f"Total: {len(students)} élève(s)" + (f" - Classe: {selected_class}" if selected_class != "Toutes les classes" else ""),
                            size=14,
                            color="#64748b",
                            weight=ft.FontWeight.W_500
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Paramètres",
                            icon="settings",
                            on_click=self.show_column_settings_dialog,
                            bgcolor="#6b7280",
                            color="#ffffff",
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12)
                            )
                        )
                    ]),
                    ft.Container(height=16),
                    ft.Container(
                        content=ft.Row(
                            controls=[data_table],
                            scroll=ft.ScrollMode.ALWAYS,  # Scroll horizontal toujours visible
                            vertical_alignment=ft.CrossAxisAlignment.START
                        ),
                        height=max(120, len(students) * 45 + 60),  # Hauteur dynamique sans limitation maximale
                        border_radius=8,
                        bgcolor="#ffffff",
                        border=ft.border.all(1, "#e2e8f0"),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    )
                ]),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
    
    def show_column_settings_dialog(self, e):
        """Afficher le popup de paramètres des colonnes"""
        
        # Créer les switches pour chaque colonne
        column_switches = []
        
        column_labels = {
            "id": "ID",
            "prenom": "Prénom", 
            "nom": "Nom",
            "date_naissance": "Date de naissance",
            "lieu_naissance": "Lieu de naissance",
            "genre": "Genre",
            "numero_eleve": "N° Élève",
            "telephone_parent": "N° Parent",
            "actions": "Actions"
        }
        
        for column_key, label in column_labels.items():
            # Ne pas permettre de désactiver les colonnes essentielles
            disabled = column_key in ["id", "actions"]
            
            switch = ft.Switch(
                label=label,
                value=self.column_visibility.get(column_key, True),
                disabled=disabled,
                data=column_key
            )
            column_switches.append(switch)
        
        self.column_settings_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Paramètres d'affichage des colonnes"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Sélectionnez les colonnes à afficher dans le tableau :",
                        size=14,
                        color="#64748b"
                    ),
                    ft.Container(height=16),
                    ft.Column(
                        controls=column_switches,
                        spacing=8
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Note: Les colonnes ID et Actions ne peuvent pas être masquées.",
                        size=12,
                        color="#94a3b8",
                        italic=True
                    )
                ], 
                tight=True,
                scroll=ft.ScrollMode.AUTO),
                width=400,
                height=350
            ),
            actions=[
                ft.TextButton("Annuler", on_click=self.close_column_settings_dialog),
                ft.ElevatedButton(
                    "Appliquer",
                    bgcolor="#4f46e5",
                    color="#ffffff",
                    on_click=lambda e: self.apply_column_settings(column_switches)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.open(self.column_settings_dialog)
    
    def close_column_settings_dialog(self, e):
        """Fermer le popup de paramètres des colonnes"""
        self.page.close(self.column_settings_dialog)
    
    def apply_column_settings(self, switches):
        """Appliquer les paramètres de visibilité des colonnes"""
        # Mettre à jour la configuration de visibilité
        for switch in switches:
            column_key = switch.data
            self.column_visibility[column_key] = switch.value
        
        # Fermer le popup
        self.page.close(self.column_settings_dialog)
        
        # Reconstruire le tableau avec les nouvelles paramètres
        if hasattr(self, 'class_filter_dropdown'):
            self.filter_students_by_class(None)
        
        self.show_snackbar("Paramètres d'affichage mis à jour!")
    
    def format_date_input_edit(self, e):
        """Formater automatiquement la saisie de date pour le popup de modification"""
        if e.control.value:
            # Supprimer tous les caractères non numériques
            digits = ''.join(filter(str.isdigit, e.control.value))
            
            # Formater en JJ/MM/AAAA
            if len(digits) >= 2:
                formatted = digits[:2]
                if len(digits) >= 4:
                    formatted += '/' + digits[2:4]
                    if len(digits) >= 8:
                        formatted += '/' + digits[4:8]
                    elif len(digits) > 4:
                        formatted += '/' + digits[4:]
                elif len(digits) > 2:
                    formatted += '/' + digits[2:]
                
                e.control.value = formatted
                self.page.update()
    
    def open_date_picker_edit(self, e):
        """Ouvrir le sélecteur de date pour le popup de modification"""
        if not hasattr(self, 'edit_date_picker') or self.edit_date_picker is None:
            self.edit_date_picker = ft.DatePicker(
                first_date=datetime(1900, 1, 1),
                last_date=datetime.now(),
                on_change=self.on_date_change_edit,
            )
            if hasattr(self, 'page') and self.page and hasattr(self.page, 'overlay'):
                self.page.overlay.append(self.edit_date_picker)
        
        self.page.open(self.edit_date_picker)
    
    def on_date_change_edit(self, e):
        """Callback pour la sélection de date dans le popup de modification"""
        if e.control.value:
            # Formater la date en JJ/MM/AAAA
            formatted_date = e.control.value.strftime("%d/%m/%Y")
            self.edit_dob_field.value = formatted_date
            self.page.update()
    
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
        """Modifier un élève via popup"""
        student = self.data_manager.get_student(student_id)
        if not student:
            self.show_snackbar("Élève introuvable", error=True)
            return
        
        self.editing_student_id = student_id
        self.show_edit_student_dialog(student)
    
    def show_edit_student_dialog(self, student):
        """Afficher le popup de modification d'élève avec le même design que l'inscription"""
        
        # Récupérer les classes disponibles (même logique que l'inscription)
        classes = self.data_manager.get_all_classes()
        class_options = []
        
        if classes:
            for classe in classes:
                class_options.append(ft.dropdown.Option(classe.get("nom", "")))
        else:
            class_options.append(ft.dropdown.Option("Aucune classe disponible"))
        
        # Créer les champs exactement comme dans le formulaire d'inscription
        self.edit_prenom_field = ft.TextField(
            label="Prénom *",
            value=student.get("prenom", ""),
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.edit_nom_field = ft.TextField(
            label="Nom *",
            value=student.get("nom", ""),
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.edit_dob_field = ft.TextField(
            label="Date de naissance *",
            value=student.get("date_naissance", ""),
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            hint_text="jj/mm/aaaa",
            expand=True,
            on_change=self.format_date_input_edit,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.edit_lieu_naissance_field = ft.TextField(
            label="Lieu de naissance *",
            value=student.get("lieu_naissance", ""),
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        # Champ ID (verrouillé, même style que l'inscription)
        self.edit_student_id_field = ft.TextField(
            label="ID",
            value=str(student.get("student_id", student.get("id", ""))),
            bgcolor="#f8fafc",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#e2e8f0",
            width=80,
            read_only=True,
            text_style=ft.TextStyle(color="#64748b", weight=ft.FontWeight.BOLD),
            text_align=ft.TextAlign.CENTER
        )
        
        self.edit_numero_eleve_field = ft.TextField(
            label="Numéro d'élève",
            value=student.get("numero_eleve", ""),
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.edit_telephone_parent_field = ft.TextField(
            label="Téléphone parent *",
            value=student.get("telephone_parent", ""),
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.edit_genre_dropdown = ft.Dropdown(
            label="Genre *",
            value=student.get("genre", "Masculin"),
            options=[
                ft.dropdown.Option("Masculin"),
                ft.dropdown.Option("Féminin"),
            ],
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        self.edit_classe_dropdown = ft.Dropdown(
            label="Classe *",
            value=student.get("classe", ""),
            options=class_options,
            bgcolor="#ffffff",
            border_radius=8,
            expand=True,
            disabled=not classes
        )
        
        # Bouton de sauvegarde (même style que l'inscription)
        save_button = ft.ElevatedButton(
            "💾 Sauvegarder les modifications",
            bgcolor="#4285f4",
            color="#ffffff",
            height=48,
            width=250,
            on_click=self.save_student_changes,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )
        
        # Bouton d'annulation
        cancel_button = ft.ElevatedButton(
            "✖️ Annuler",
            bgcolor="#6b7280",
            color="#ffffff",
            height=48,
            width=150,
            on_click=self.close_edit_student_dialog,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )
        
        # Créer le formulaire avec EXACTEMENT la même structure que l'inscription
        form_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    # En-tête
                    ft.Text(
                        "Modifier l'élève",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Container(height=20),
                    
                    # Ligne ID - Champ ID déplacé vers le haut, aligné à droite (même que inscription)
                    ft.Row([
                        ft.Container(expand=1),  # Espace vide à gauche
                        self.edit_student_id_field  # Petit champ fixe à droite
                    ]),
                    ft.Container(height=20),
                    
                    # Première ligne - Prénom et Nom (même que inscription)
                    ft.Row([
                        ft.Container(self.edit_prenom_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.edit_nom_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Deuxième ligne - Date de naissance avec calendrier et Lieu de naissance (même que inscription)
                    ft.Row([
                        ft.Container(
                            content=ft.Row([
                                ft.Container(self.edit_dob_field, expand=1),
                                ft.IconButton(
                                    icon="calendar_today",
                                    icon_color="#4f46e5",
                                    tooltip="Choisir une date",
                                    on_click=self.open_date_picker_edit
                                )
                            ], spacing=8),
                            expand=1
                        ),
                        ft.Container(width=16),
                        ft.Container(self.edit_lieu_naissance_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Troisième ligne - Numéro d'élève et Téléphone parent (même que inscription)
                    ft.Row([
                        ft.Container(self.edit_numero_eleve_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.edit_telephone_parent_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Quatrième ligne - Genre et Classe (même que inscription)
                    ft.Row([
                        ft.Container(self.edit_genre_dropdown, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.edit_classe_dropdown, expand=1)
                    ]),
                    ft.Container(height=30),
                    
                    # Boutons (alignés à droite comme l'inscription)
                    ft.Row([
                        cancel_button,
                        ft.Container(width=16),
                        save_button
                    ], alignment=ft.MainAxisAlignment.END)
                ]),
                padding=32
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        # Créer le popup avec scrollbars toujours visibles
        self.edit_student_dialog = ft.AlertDialog(
            modal=True,
            content=ft.Container(
                content=ft.Column([
                    form_card
                ], scroll=ft.ScrollMode.ALWAYS),  # Scrollbars toujours visibles
                width=800,  # Même largeur que le formulaire d'inscription
                height=600  # Hauteur adaptée
            )
        )
        
        self.page.open(self.edit_student_dialog)
    
    def close_edit_student_dialog(self, e):
        """Fermer le popup de modification d'élève"""
        try:
            self.page.close(self.edit_student_dialog)
            self.page.update()
        except Exception as ex:
            print(f"Erreur lors de la fermeture du popup: {ex}")
    
    def save_student_changes(self, e):
        """Sauvegarder les modifications de l'élève"""
        try:
            # Validation des champs obligatoires
            if not self.edit_prenom_field.value or not self.edit_prenom_field.value.strip():
                self.show_snackbar("Le prénom est obligatoire", error=True)
                return
            
            if not self.edit_nom_field.value or not self.edit_nom_field.value.strip():
                self.show_snackbar("Le nom est obligatoire", error=True)
                return
            
            if not self.edit_dob_field.value or not self.edit_dob_field.value.strip():
                self.show_snackbar("La date de naissance est obligatoire", error=True)
                return
            
            if not self.edit_classe_dropdown.value:
                self.show_snackbar("La classe est obligatoire", error=True)
                return
            
            # Préparer les données mises à jour
            updated_data = {
                "prenom": self.edit_prenom_field.value.strip(),
                "nom": self.edit_nom_field.value.strip(),
                "date_naissance": self.edit_dob_field.value.strip(),
                "lieu_naissance": self.edit_lieu_naissance_field.value.strip() if self.edit_lieu_naissance_field.value else "",
                "numero_eleve": self.edit_numero_eleve_field.value.strip() if self.edit_numero_eleve_field.value else "",
                "telephone_parent": self.edit_telephone_parent_field.value.strip() if self.edit_telephone_parent_field.value else "",
                "genre": self.edit_genre_dropdown.value,
                "classe": self.edit_classe_dropdown.value,
                "date_modification": datetime.now().isoformat()
            }
            
            # Sauvegarder les modifications
            if self.data_manager.update_student(self.editing_student_id, updated_data):
                # Fermer le popup d'abord
                self.page.close(self.edit_student_dialog)
                
                # Afficher le message de succès
                self.show_snackbar("Élève modifié avec succès!")
                
                # Reconstruire le tableau avec les nouvelles données
                if hasattr(self, 'class_filter_dropdown'):
                    self.filter_students_by_class(None)
                
                # Mettre à jour la page
                self.page.update()
            else:
                self.show_snackbar("Erreur lors de la modification", error=True)
                
        except Exception as ex:
            print(f"Erreur lors de la sauvegarde: {ex}")
            self.show_snackbar("Erreur lors de la modification", error=True)
    
    def delete_student(self, student_id):
        """Supprimer un élève avec popup de confirmation"""
        student = self.data_manager.get_student(student_id)
        if not student:
            self.show_snackbar("Élève introuvable", error=True)
            return
        
        self.deleting_student_id = student_id
        self.show_delete_student_dialog(student)
    
    def show_delete_student_dialog(self, student):
        """Afficher le popup de confirmation de suppression"""
        
        student_name = f"{student.get('prenom', '')} {student.get('nom', '')}".strip()
        student_class = student.get('classe', 'Non définie')
        
        self.delete_student_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row([
                ft.Icon("warning", color="#ef4444", size=24),
                ft.Container(width=8),
                ft.Text("Confirmer la suppression", color="#ef4444", weight=ft.FontWeight.BOLD)
            ]),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Êtes-vous sûr de vouloir supprimer cet élève ?",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color="#1e293b"
                    ),
                    ft.Container(height=16),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Row([
                                    ft.Text("Nom:", weight=ft.FontWeight.BOLD, size=14, color="#64748b"),
                                    ft.Text(student_name, size=14, color="#1e293b")
                                ]),
                                ft.Row([
                                    ft.Text("Classe:", weight=ft.FontWeight.BOLD, size=14, color="#64748b"),
                                    ft.Text(student_class, size=14, color="#1e293b")
                                ]),
                                ft.Row([
                                    ft.Text("ID:", weight=ft.FontWeight.BOLD, size=14, color="#64748b"),
                                    ft.Text(str(student.get("student_id", student.get("id", ""))), size=14, color="#1e293b")
                                ])
                            ], spacing=8),
                            padding=16
                        ),
                        elevation=0,
                        color="#f8fafc"
                    ),
                    ft.Container(height=16),
                    ft.Container(
                        content=ft.Text(
                            "⚠️ Cette action est irréversible",
                            size=14,
                            color="#ef4444",
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER
                        ),
                        bgcolor="#fef2f2",
                        padding=12,
                        border_radius=8,
                        border=ft.border.all(1, "#fecaca")
                    )
                ], tight=True),
                width=400,
                height=250
            ),
            actions=[
                ft.ElevatedButton(
                    "Annuler",
                    on_click=self.close_delete_student_dialog,
                    bgcolor="#6b7280",
                    color="#ffffff"
                ),
                ft.ElevatedButton(
                    "Confirmer la suppression",
                    on_click=self.confirm_delete_student,
                    bgcolor="#ef4444",
                    color="#ffffff"
                )
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        self.page.open(self.delete_student_dialog)
    
    def close_delete_student_dialog(self, e):
        """Fermer le popup de confirmation de suppression"""
        self.page.close(self.delete_student_dialog)
    
    def confirm_delete_student(self, e):
        """Confirmer et exécuter la suppression"""
        if self.data_manager.delete_student(self.deleting_student_id):
            self.show_snackbar("Élève supprimé avec succès!")
            self.page.close(self.delete_student_dialog)
            
            # Reconstruire le tableau
            if hasattr(self, 'class_filter_dropdown'):
                self.filter_students_by_class(None)
        else:
            self.show_snackbar("Erreur lors de la suppression", error=True)
    
    def show_teacher_registration(self):
        """Afficher le formulaire d'inscription des professeurs"""
        self.current_page = "teacher_registration"
        self.clear_main_content()
        
        # En-tête
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Inscription d'un professeur",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color="#1e293b"
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Formulaire
        form_content = self.create_teacher_registration_form()
        
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
    
    def create_teacher_registration_form(self):
        """Créer le formulaire d'inscription des professeurs"""
        # Générer le prochain ID professeur (auto-incrémenté)
        next_teacher_id = self.data_manager.get_next_teacher_id()
        
        # Champ ID auto-généré (non modifiable) - identique au formulaire élève
        self.teacher_id_field = ft.TextField(
            label="ID",
            value=str(next_teacher_id),
            bgcolor="#f8fafc",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#e2e8f0",
            width=80,
            read_only=True,
            text_style=ft.TextStyle(color="#64748b", weight=ft.FontWeight.BOLD),
            text_align=ft.TextAlign.CENTER
        )
        
        # Champs du formulaire avec expand=True comme dans le formulaire élève
        self.teacher_prenom_field = ft.TextField(
            label="Prénom *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.teacher_nom_field = ft.TextField(
            label="Nom *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        # Date de naissance avec sélecteur
        self.teacher_dob_field = ft.TextField(
            label="Date de naissance *",
            hint_text="JJ/MM/AAAA",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True,
            on_change=self.format_teacher_date_input,
            suffix=ft.IconButton(
                icon="calendar_today",
                icon_color="#4f46e5",
                tooltip="Sélectionner une date",
                on_click=self.open_teacher_date_picker
            )
        )
        
        self.teacher_lieu_naissance_field = ft.TextField(
            label="Lieu de naissance",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.teacher_email_field = ft.TextField(
            label="Email *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.teacher_telephone_field = ft.TextField(
            label="Numéro de téléphone",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.teacher_residence_field = ft.TextField(
            label="Résidence",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True
        )
        
        self.teacher_experience_field = ft.TextField(
            label="Années d'expérience",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        # Champ matière avec auto-suggestion
        self.subjects_list = [
            "Mathématiques", "Sciences physiques et chimie", "SVT", "Français", 
            "Anglais", "Musique", "Philosophie", "EPS", "Informatique", 
            "Histoire-géographie", "Grec", "Latin", "Espagnol", "Portugais", "Russe"
        ]
        
        self.teacher_genre_dropdown = ft.Dropdown(
            label="Genre *",
            hint_text="Sélectionner",
            options=[
                ft.dropdown.Option("Homme"),
                ft.dropdown.Option("Femme")
            ],
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        self.teacher_matiere_field = ft.TextField(
            label="Matière enseignée *",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            expand=True,
            on_change=self.on_teacher_subject_change
        )
        
        # Liste des suggestions
        self.subject_suggestions_list = ft.ListView(
            height=0,  # Caché initialement
            visible=False,
            spacing=0
        )
        
        # Bouton d'inscription
        submit_button = ft.ElevatedButton(
            "👨‍🏫 Inscrire le professeur",
            bgcolor="#4285f4",
            color="#ffffff",
            height=48,
            width=200,
            on_click=self.register_teacher,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8)
            )
        )
        
        # Créer le formulaire selon le même design que le formulaire élève
        form_card = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    # Ligne ID - Champ ID déplacé vers le haut, aligné à droite
                    ft.Row([
                        ft.Container(expand=1),  # Espace vide à gauche
                        self.teacher_id_field  # Petit champ fixe à droite
                    ]),
                    ft.Container(height=20),
                    
                    # Première ligne - Prénom et Nom
                    ft.Row([
                        ft.Container(self.teacher_prenom_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.teacher_nom_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Deuxième ligne - Date de naissance avec calendrier et Lieu de naissance
                    ft.Row([
                        ft.Container(
                            content=ft.Row([
                                ft.Container(self.teacher_dob_field, expand=1),
                                ft.IconButton(
                                    icon="calendar_today",
                                    icon_color="#4f46e5",
                                    tooltip="Choisir une date",
                                    on_click=self.open_teacher_date_picker
                                )
                            ], spacing=8),
                            expand=1
                        ),
                        ft.Container(width=16),
                        ft.Container(self.teacher_lieu_naissance_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Troisième ligne - Email et Téléphone
                    ft.Row([
                        ft.Container(self.teacher_email_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.teacher_telephone_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Quatrième ligne - Résidence et Années d'expérience
                    ft.Row([
                        ft.Container(self.teacher_residence_field, expand=1),
                        ft.Container(width=16),
                        ft.Container(self.teacher_experience_field, expand=1)
                    ]),
                    ft.Container(height=20),
                    
                    # Cinquième ligne - Genre et Matière enseignée
                    ft.Row([
                        ft.Container(self.teacher_genre_dropdown, expand=1),
                        ft.Container(width=16),
                        ft.Container(
                            content=ft.Column([
                                self.teacher_matiere_field,
                                self.subject_suggestions_list
                            ]),
                            expand=1
                        )
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
    
    def format_teacher_date_input(self, e):
        """Formater automatiquement la saisie de date pour les professeurs"""
        if e.control.value:
            # Supprimer tous les caractères non numériques
            digits = ''.join(filter(str.isdigit, e.control.value))
            
            # Formater en JJ/MM/AAAA
            if len(digits) >= 2:
                formatted = digits[:2]
                if len(digits) >= 4:
                    formatted += '/' + digits[2:4]
                    if len(digits) >= 8:
                        formatted += '/' + digits[4:8]
                    elif len(digits) > 4:
                        formatted += '/' + digits[4:]
                elif len(digits) > 2:
                    formatted += '/' + digits[2:]
                
                e.control.value = formatted
                self.page.update()
    
    def open_teacher_date_picker(self, e):
        """Ouvrir le sélecteur de date pour les professeurs"""
        if not hasattr(self, 'teacher_date_picker') or self.teacher_date_picker is None:
            self.teacher_date_picker = ft.DatePicker(
                first_date=datetime(1900, 1, 1),
                last_date=datetime.now(),
                on_change=self.on_teacher_date_change,
            )
            if hasattr(self, 'page') and self.page and hasattr(self.page, 'overlay'):
                self.page.overlay.append(self.teacher_date_picker)
        
        self.page.open(self.teacher_date_picker)
    
    def on_teacher_date_change(self, e):
        """Callback pour la sélection de date des professeurs"""
        if e.control.value:
            # Formater la date en JJ/MM/AAAA
            formatted_date = e.control.value.strftime("%d/%m/%Y")
            self.teacher_dob_field.value = formatted_date
            self.page.update()
    
    def on_teacher_subject_change(self, e):
        """Gérer l'auto-suggestion pour les matières"""
        user_input = e.control.value.lower().strip() if e.control.value else ""
        
        if not user_input:
            # Cacher les suggestions si le champ est vide
            self.subject_suggestions_list.height = 0
            self.subject_suggestions_list.visible = False
            self.subject_suggestions_list.controls.clear()
            self.page.update()
            return
        
        # Filtrer les matières
        matching_subjects = [
            subject for subject in self.subjects_list 
            if user_input in subject.lower()
        ]
        
        if matching_subjects:
            # Créer les suggestions
            self.subject_suggestions_list.controls.clear()
            
            for subject in matching_subjects[:5]:  # Limiter à 5 suggestions
                suggestion_button = ft.Container(
                    content=ft.Text(
                        subject,
                        size=14,
                        color="#374151"
                    ),
                    bgcolor="#f9fafb",
                    border=ft.border.all(1, "#e5e7eb"),
                    border_radius=4,
                    padding=ft.padding.symmetric(horizontal=12, vertical=8),
                    on_click=lambda e, subj=subject: self.select_subject(subj)
                )
                self.subject_suggestions_list.controls.append(suggestion_button)
            
            # Afficher les suggestions
            self.subject_suggestions_list.height = min(150, len(matching_subjects) * 35)
            self.subject_suggestions_list.visible = True
        else:
            # Cacher les suggestions si aucune correspondance
            self.subject_suggestions_list.height = 0
            self.subject_suggestions_list.visible = False
            self.subject_suggestions_list.controls.clear()
        
        self.page.update()
    
    def select_subject(self, subject):
        """Sélectionner une matière depuis les suggestions"""
        self.teacher_matiere_field.value = subject
        
        # Cacher les suggestions
        self.subject_suggestions_list.height = 0
        self.subject_suggestions_list.visible = False
        self.subject_suggestions_list.controls.clear()
        
        self.page.update()
    
    def register_teacher(self, e):
        """Enregistrer un nouveau professeur"""
        try:
            # Validation des champs obligatoires
            if not self.teacher_prenom_field.value or not self.teacher_prenom_field.value.strip():
                self.show_snackbar("Le prénom est obligatoire", error=True)
                return
            
            if not self.teacher_nom_field.value or not self.teacher_nom_field.value.strip():
                self.show_snackbar("Le nom est obligatoire", error=True)  
                return
            
            if not self.teacher_dob_field.value or not self.teacher_dob_field.value.strip():
                self.show_snackbar("La date de naissance est obligatoire", error=True)
                return
            
            if not self.teacher_email_field.value or not self.teacher_email_field.value.strip():
                self.show_snackbar("L'email est obligatoire", error=True)
                return
            
            if not self.teacher_genre_dropdown.value:
                self.show_snackbar("Le genre est obligatoire", error=True)
                return
            
            if not self.teacher_matiere_field.value or not self.teacher_matiere_field.value.strip():
                self.show_snackbar("La matière enseignée est obligatoire", error=True)
                return
            
            # Validation de l'email
            email = self.teacher_email_field.value.strip()
            if "@" not in email or "." not in email:
                self.show_snackbar("Format d'email invalide", error=True)
                return
            
            # Générer l'ID du professeur
            teacher_id = self.data_manager.get_next_teacher_id()
            
            # Préparer les données du professeur
            teacher_data = {
                "id": teacher_id,
                "teacher_id": teacher_id,
                "prenom": self.teacher_prenom_field.value.strip(),
                "nom": self.teacher_nom_field.value.strip(),
                "date_naissance": self.teacher_dob_field.value.strip(),
                "lieu_naissance": self.teacher_lieu_naissance_field.value.strip() if self.teacher_lieu_naissance_field.value else "",
                "email": email,
                "telephone": self.teacher_telephone_field.value.strip() if self.teacher_telephone_field.value else "",
                "residence": self.teacher_residence_field.value.strip() if self.teacher_residence_field.value else "",
                "experience": self.teacher_experience_field.value.strip() if self.teacher_experience_field.value else "",
                "genre": self.teacher_genre_dropdown.value,
                "matiere": self.teacher_matiere_field.value.strip(),
                "date_inscription": datetime.now().isoformat()
            }
            
            # Enregistrer le professeur
            if self.data_manager.add_teacher(teacher_data):
                self.show_snackbar("Professeur inscrit avec succès!")
                
                # Réinitialiser le formulaire
                self.clear_teacher_form()
                
                # Mettre à jour l'ID pour le prochain professeur
                next_id = self.data_manager.get_next_teacher_id()
                self.teacher_id_field.value = str(next_id)
                
                self.page.update()
            else:
                self.show_snackbar("Erreur lors de l'inscription", error=True)
                
        except Exception as ex:
            print(f"Erreur lors de l'inscription du professeur: {ex}")
            self.show_snackbar("Erreur lors de l'inscription", error=True)
    
    def clear_teacher_form(self):
        """Effacer tous les champs du formulaire professeur"""
        self.teacher_prenom_field.value = ""
        self.teacher_nom_field.value = ""
        self.teacher_dob_field.value = ""
        self.teacher_lieu_naissance_field.value = ""
        self.teacher_email_field.value = ""
        self.teacher_telephone_field.value = ""
        self.teacher_residence_field.value = ""
        self.teacher_experience_field.value = ""
        self.teacher_genre_dropdown.value = None
        self.teacher_matiere_field.value = ""
        
        # Cacher les suggestions
        self.subject_suggestions_list.height = 0
        self.subject_suggestions_list.visible = False
        self.subject_suggestions_list.controls.clear()
    
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
        
        # Initialiser la visibilité des colonnes pour les professeurs si elle n'existe pas
        if not hasattr(self, 'teacher_column_visibility'):
            self.teacher_column_visibility = {
                "id": True,
                "prenom": True,
                "nom": True,
                "date_naissance": True,
                "lieu_naissance": False,
                "genre": True,
                "email": True,
                "telephone": True,
                "residence": True,
                "experience": True,
                "matiere": True,
                "actions": True
            }
        
        # Barre de recherche pour les professeurs
        self.teacher_search_field = ft.TextField(
            label="Rechercher un professeur...",
            hint_text="Saisir ID, nom, prénom ou nom complet",
            prefix_icon="search",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            width=350,
            on_change=self.search_teachers,
            autofocus=False
        )
        
        # En-tête
        header = ft.Container(
            content=ft.Column([
                ft.Row([
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
                    self.teacher_search_field
                ])
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Table des professeurs (sera mise à jour par la recherche)
        self.teachers_table_container = ft.Container()
        self.load_all_teachers()  # Charger tous les professeurs initialement
        
        # Assembler le contenu avec scrollbar comme les autres pages
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    self.teachers_table_container
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def load_all_teachers(self):
        """Charger tous les professeurs dans le tableau"""
        teachers = self.data_manager.get_all_teachers()
        self.display_teachers_table(teachers)
    
    def search_teachers(self, e):
        """Rechercher des professeurs par ID, nom, prénom ou nom complet"""
        search_term = e.control.value.lower().strip() if e.control.value else ""
        
        # Récupérer tous les professeurs
        all_teachers = self.data_manager.get_all_teachers()
        
        if not search_term:
            # Si pas de terme de recherche, afficher tous les professeurs
            filtered_teachers = all_teachers
        else:
            # Filtrer les professeurs selon le terme de recherche
            filtered_teachers = []
            for teacher in all_teachers:
                # Recherche par ID (converti en string)
                teacher_id = str(teacher.get("id", ""))
                if search_term in teacher_id.lower():
                    filtered_teachers.append(teacher)
                    continue
                
                # Recherche par prénom
                prenom = teacher.get("prenom", "").lower()
                if search_term in prenom:
                    filtered_teachers.append(teacher)
                    continue
                
                # Recherche par nom
                nom = teacher.get("nom", "").lower()
                if search_term in nom:
                    filtered_teachers.append(teacher)
                    continue
                
                # Recherche par nom complet (prénom + nom)
                nom_complet = f"{prenom} {nom}".strip()
                if search_term in nom_complet:
                    filtered_teachers.append(teacher)
                    continue
        
        # Afficher les résultats filtrés
        self.display_teachers_table(filtered_teachers)
    
    def display_teachers_table(self, teachers):
        """Afficher le tableau des professeurs avec les données fournies"""
        # Trier les professeurs par ID
        def safe_sort_key(teacher):
            try:
                return int(teacher.get("id", 0))
            except (ValueError, TypeError):
                return 0
        
        teachers = sorted(teachers, key=safe_sort_key)
        
        # Créer les lignes du tableau
        rows = []
        for teacher in teachers:
            cells = []
            
            # ID (toujours visible)
            if self.teacher_column_visibility.get("id", True):
                cells.append(ft.DataCell(ft.Text(str(teacher.get("id", "")), size=12)))
            
            # Prénom
            if self.teacher_column_visibility.get("prenom", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("prenom", ""), size=12)))
            
            # Nom
            if self.teacher_column_visibility.get("nom", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("nom", ""), size=12)))
            
            # Date de naissance
            if self.teacher_column_visibility.get("date_naissance", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("date_naissance", ""), size=12)))
            
            # Lieu de naissance (optionnel)
            if self.teacher_column_visibility.get("lieu_naissance", False):
                cells.append(ft.DataCell(ft.Text(teacher.get("lieu_naissance", ""), size=12)))
            
            # Genre
            if self.teacher_column_visibility.get("genre", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("genre", ""), size=12)))
            
            # Email
            if self.teacher_column_visibility.get("email", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("email", ""), size=12)))
            
            # Téléphone
            if self.teacher_column_visibility.get("telephone", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("telephone", ""), size=12)))
            
            # Résidence
            if self.teacher_column_visibility.get("residence", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("residence", ""), size=12)))
            
            # Années d'expérience
            if self.teacher_column_visibility.get("experience", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("experience", ""), size=12)))
            
            # Matière enseignée
            if self.teacher_column_visibility.get("matiere", True):
                cells.append(ft.DataCell(ft.Text(teacher.get("matiere", ""), size=12)))
            
            # Actions (toujours visibles)
            if self.teacher_column_visibility.get("actions", True):
                action_row = ft.Row([
                    ft.IconButton(
                        icon="edit",
                        icon_color="#4f46e5",
                        tooltip="Modifier",
                        on_click=lambda e, t=teacher: self.show_edit_teacher_dialog(t)
                    ),
                    ft.IconButton(
                        icon="delete",
                        icon_color="#ef4444",
                        tooltip="Supprimer",
                        on_click=lambda e, t=teacher: self.show_delete_teacher_confirmation(t)
                    )
                ], spacing=0)
                cells.append(ft.DataCell(action_row))
            
            rows.append(ft.DataRow(cells=cells))
        
        # Créer les colonnes selon la visibilité
        columns = []
        
        # ID (toujours visible)
        if self.teacher_column_visibility.get("id", True):
            columns.append(ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=12)))
        
        # Prénom
        if self.teacher_column_visibility.get("prenom", True):
            columns.append(ft.DataColumn(ft.Text("Prénom", weight=ft.FontWeight.BOLD, size=12)))
        
        # Nom
        if self.teacher_column_visibility.get("nom", True):
            columns.append(ft.DataColumn(ft.Text("Nom", weight=ft.FontWeight.BOLD, size=12)))
        
        # Date de naissance
        if self.teacher_column_visibility.get("date_naissance", True):
            columns.append(ft.DataColumn(ft.Text("Date de naissance", weight=ft.FontWeight.BOLD, size=12)))
        
        # Lieu de naissance (optionnel)
        if self.teacher_column_visibility.get("lieu_naissance", False):
            columns.append(ft.DataColumn(ft.Text("Lieu de naissance", weight=ft.FontWeight.BOLD, size=12)))
        
        # Genre
        if self.teacher_column_visibility.get("genre", True):
            columns.append(ft.DataColumn(ft.Text("Genre", weight=ft.FontWeight.BOLD, size=12)))
        
        # Email
        if self.teacher_column_visibility.get("email", True):
            columns.append(ft.DataColumn(ft.Text("Email", weight=ft.FontWeight.BOLD, size=12)))
        
        # Téléphone
        if self.teacher_column_visibility.get("telephone", True):
            columns.append(ft.DataColumn(ft.Text("Téléphone", weight=ft.FontWeight.BOLD, size=12)))
        
        # Résidence
        if self.teacher_column_visibility.get("residence", True):
            columns.append(ft.DataColumn(ft.Text("Résidence", weight=ft.FontWeight.BOLD, size=12)))
        
        # Années d'expérience
        if self.teacher_column_visibility.get("experience", True):
            columns.append(ft.DataColumn(ft.Text("Expérience", weight=ft.FontWeight.BOLD, size=12)))
        
        # Matière enseignée
        if self.teacher_column_visibility.get("matiere", True):
            columns.append(ft.DataColumn(ft.Text("Matière", weight=ft.FontWeight.BOLD, size=12)))
        
        # Actions (toujours visibles)
        if self.teacher_column_visibility.get("actions", True):
            columns.append(ft.DataColumn(ft.Text("Actions", weight=ft.FontWeight.BOLD, size=12)))
        
        data_table = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, "#e2e8f0"),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, "#f1f5f9"),
            horizontal_lines=ft.border.BorderSide(1, "#f1f5f9"),
            heading_row_color="#f8fafc"
        )
        
        # Mettre à jour le container avec le nouveau tableau
        self.teachers_table_container.content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            f"Total: {len(teachers)} professeur(s)",
                            size=14,
                            color="#64748b",
                            weight=ft.FontWeight.W_500
                        ),
                        ft.Container(expand=True),
                        ft.ElevatedButton(
                            "Paramètres",
                            icon="settings",
                            on_click=self.show_teacher_column_settings_dialog,
                            bgcolor="#6b7280",
                            color="#ffffff",
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=12)
                            )
                        )
                    ]),
                    ft.Container(height=16),
                    ft.Container(
                        content=ft.Row(
                            controls=[data_table],
                            scroll=ft.ScrollMode.ALWAYS,  # Scroll horizontal toujours visible
                            vertical_alignment=ft.CrossAxisAlignment.START
                        ),
                        height=min(300, max(120, len(teachers) * 45 + 60)),  # Hauteur dynamique basée sur le nombre de professeurs
                        border_radius=8,
                        bgcolor="#ffffff",
                        border=ft.border.all(1, "#e2e8f0"),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    )
                ]),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        self.page.update()
    
    def show_teacher_column_settings_dialog(self, e):
        """Afficher le popup de paramètres des colonnes pour les professeurs"""
        
        # Créer les switches pour chaque colonne
        column_switches = []
        
        column_labels = {
            "id": "ID",
            "prenom": "Prénom", 
            "nom": "Nom",
            "date_naissance": "Date de naissance",
            "lieu_naissance": "Lieu de naissance",
            "genre": "Genre",
            "email": "Email",
            "telephone": "Téléphone",
            "residence": "Résidence",
            "experience": "Expérience",
            "matiere": "Matière",
            "actions": "Actions"
        }
        
        for column_key, label in column_labels.items():
            # Ne pas permettre de désactiver les colonnes essentielles
            disabled = column_key in ["id", "actions"]
            
            switch = ft.Switch(
                label=label,
                value=self.teacher_column_visibility.get(column_key, True),
                disabled=disabled,
                data=column_key
            )
            column_switches.append(switch)
        
        self.teacher_column_settings_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Paramètres d'affichage des colonnes"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Sélectionnez les colonnes à afficher dans le tableau :",
                        size=14,
                        color="#64748b"
                    ),
                    ft.Container(height=16),
                    ft.Column(
                        controls=column_switches,
                        spacing=8
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "Note: Les colonnes ID et Actions ne peuvent pas être masquées.",
                        size=12,
                        color="#94a3b8",
                        italic=True
                    )
                ], 
                tight=True,
                scroll=ft.ScrollMode.AUTO),
                width=400,
                height=350
            ),
            actions=[
                ft.TextButton("Annuler", on_click=self.close_teacher_column_settings_dialog),
                ft.ElevatedButton(
                    "Appliquer",
                    bgcolor="#4f46e5",
                    color="#ffffff",
                    on_click=lambda e: self.apply_teacher_column_settings(column_switches)
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.open(self.teacher_column_settings_dialog)
    
    def close_teacher_column_settings_dialog(self, e):
        """Fermer le popup de paramètres des colonnes pour les professeurs"""
        self.page.close(self.teacher_column_settings_dialog)
    
    def apply_teacher_column_settings(self, switches):
        """Appliquer les paramètres de visibilité des colonnes pour les professeurs"""
        # Mettre à jour la configuration de visibilité
        for switch in switches:
            column_key = switch.data
            self.teacher_column_visibility[column_key] = switch.value
        
        # Fermer le popup
        self.page.close(self.teacher_column_settings_dialog)
        
        # Reconstruire le tableau avec les nouvelles paramètres
        self.load_all_teachers()
        
        self.show_snackbar("Paramètres d'affichage mis à jour!")
    
    def show_edit_teacher_dialog(self, teacher):
        """Afficher le popup de modification d'un professeur"""
        
        # Champs pré-remplis pour la modification
        edit_prenom = ft.TextField(
            label="Prénom *",
            value=teacher.get("prenom", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        edit_nom = ft.TextField(
            label="Nom *",
            value=teacher.get("nom", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        edit_dob = ft.TextField(
            label="Date de naissance *",
            value=teacher.get("date_naissance", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True,
            on_change=self.format_date_input_edit
        )
        
        edit_lieu_naissance = ft.TextField(
            label="Lieu de naissance",
            value=teacher.get("lieu_naissance", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        edit_genre = ft.Dropdown(
            label="Genre *",
            value=teacher.get("genre", ""),
            options=[
                ft.dropdown.Option("Homme"),
                ft.dropdown.Option("Femme")
            ],
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        edit_email = ft.TextField(
            label="Email *",
            value=teacher.get("email", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        edit_telephone = ft.TextField(
            label="Téléphone",
            value=teacher.get("telephone", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        edit_residence = ft.TextField(
            label="Résidence",
            value=teacher.get("residence", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        edit_experience = ft.TextField(
            label="Années d'expérience",
            value=teacher.get("experience", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        edit_matiere = ft.TextField(
            label="Matière enseignée *",
            value=teacher.get("matiere", ""),
            bgcolor="#ffffff",
            border_radius=8,
            expand=True
        )
        
        # ID non modifiable
        id_display = ft.TextField(
            label="ID",
            value=str(teacher.get("id", "")),
            read_only=True,
            bgcolor="#f8fafc",
            border_color="#e2e8f0",
            focused_border_color="#e2e8f0",
            text_style=ft.TextStyle(color="#64748b"),
            expand=True
        )
        
        def save_teacher_changes(e):
            """Sauvegarder les modifications du professeur"""
            # Validation des champs obligatoires
            if not edit_prenom.value or not edit_prenom.value.strip():
                self.show_snackbar("Le prénom est obligatoire", error=True)
                return
            
            if not edit_nom.value or not edit_nom.value.strip():
                self.show_snackbar("Le nom est obligatoire", error=True)
                return
            
            if not edit_dob.value or not edit_dob.value.strip():
                self.show_snackbar("La date de naissance est obligatoire", error=True)
                return
            
            if not edit_genre.value:
                self.show_snackbar("Le genre est obligatoire", error=True)
                return
            
            if not edit_email.value or not edit_email.value.strip():
                self.show_snackbar("L'email est obligatoire", error=True)
                return
            
            if not edit_matiere.value or not edit_matiere.value.strip():
                self.show_snackbar("La matière est obligatoire", error=True)
                return
            
            # Validation de l'email
            email = edit_email.value.strip()
            if "@" not in email or "." not in email:
                self.show_snackbar("Format d'email invalide", error=True)
                return
            
            # Préparer les données mises à jour
            updated_teacher = {
                "id": teacher["id"],
                "teacher_id": teacher.get("teacher_id", teacher["id"]),
                "prenom": edit_prenom.value.strip(),
                "nom": edit_nom.value.strip(),
                "date_naissance": edit_dob.value.strip(),
                "lieu_naissance": edit_lieu_naissance.value.strip() if edit_lieu_naissance.value else "",
                "genre": edit_genre.value,
                "email": email,
                "telephone": edit_telephone.value.strip() if edit_telephone.value else "",
                "residence": edit_residence.value.strip() if edit_residence.value else "",
                "experience": edit_experience.value.strip() if edit_experience.value else "",
                "matiere": edit_matiere.value.strip(),
                "date_inscription": teacher.get("date_inscription", datetime.now().isoformat())
            }
            
            # Sauvegarder les modifications
            if self.data_manager.update_teacher(teacher["id"], updated_teacher):
                self.page.close(self.edit_teacher_dialog)
                self.show_snackbar("Professeur modifié avec succès!")
                
                # Recharger le tableau
                self.load_all_teachers()
            else:
                self.show_snackbar("Erreur lors de la modification", error=True)
        
        # Créer le popup de modification avec scrollbars
        self.edit_teacher_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Modifier le professeur"),
            content=ft.Container(
                content=ft.Column([
                    # ID non modifiable
                    id_display,
                    ft.Container(height=16),
                    
                    # Première ligne - Prénom et Nom
                    ft.Row([
                        edit_prenom,
                        ft.Container(width=16),
                        edit_nom
                    ]),
                    ft.Container(height=16),
                    
                    # Deuxième ligne - Date et lieu de naissance
                    ft.Row([
                        edit_dob,
                        ft.Container(width=16),
                        edit_lieu_naissance
                    ]),
                    ft.Container(height=16),
                    
                    # Troisième ligne - Genre et Email
                    ft.Row([
                        edit_genre,
                        ft.Container(width=16),
                        edit_email
                    ]),
                    ft.Container(height=16),
                    
                    # Quatrième ligne - Téléphone et Résidence
                    ft.Row([
                        edit_telephone,
                        ft.Container(width=16),
                        edit_residence
                    ]),
                    ft.Container(height=16),
                    
                    # Cinquième ligne - Expérience et Matière
                    ft.Row([
                        edit_experience,
                        ft.Container(width=16),
                        edit_matiere
                    ])
                ], scroll=ft.ScrollMode.ALWAYS),
                width=600,
                height=500
            ),
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.page.close(self.edit_teacher_dialog)),
                ft.ElevatedButton(
                    "Sauvegarder",
                    bgcolor="#4f46e5",
                    color="#ffffff",
                    on_click=save_teacher_changes
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.open(self.edit_teacher_dialog)
    
    def show_delete_teacher_confirmation(self, teacher):
        """Afficher le popup de confirmation de suppression d'un professeur"""
        
        # Informations du professeur à supprimer
        teacher_info = f"ID: {teacher.get('id', 'N/A')}\n"
        teacher_info += f"Nom: {teacher.get('prenom', '')} {teacher.get('nom', '')}\n"
        teacher_info += f"Email: {teacher.get('email', 'N/A')}\n"
        teacher_info += f"Matière: {teacher.get('matiere', 'N/A')}"
        
        def confirm_delete(e):
            """Confirmer et effectuer la suppression"""
            if self.data_manager.delete_teacher(teacher["id"]):
                self.page.close(self.delete_teacher_dialog)
                self.show_snackbar("Professeur supprimé avec succès!")
                
                # Recharger le tableau
                self.load_all_teachers()
            else:
                self.show_snackbar("Erreur lors de la suppression", error=True)
        
        self.delete_teacher_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmer la suppression", color="#ef4444"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Êtes-vous sûr de vouloir supprimer ce professeur ?",
                        size=16,
                        weight=ft.FontWeight.W_500
                    ),
                    ft.Container(height=16),
                    ft.Container(
                        content=ft.Text(
                            teacher_info,
                            size=14,
                            color="#64748b"
                        ),
                        bgcolor="#f8fafc",
                        padding=16,
                        border_radius=8,
                        border=ft.border.all(1, "#e2e8f0")
                    ),
                    ft.Container(height=16),
                    ft.Text(
                        "⚠️ Cette action est irréversible !",
                        size=14,
                        color="#ef4444",
                        weight=ft.FontWeight.W_500
                    )
                ]),
                width=400
            ),
            actions=[
                ft.TextButton("Annuler", on_click=lambda e: self.page.close(self.delete_teacher_dialog)),
                ft.ElevatedButton(
                    "Supprimer",
                    bgcolor="#ef4444",
                    color="#ffffff",
                    on_click=confirm_delete
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        self.page.open(self.delete_teacher_dialog)
    
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
        """Afficher la gestion des notes - Sélection du semestre"""
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
                    "Sélectionnez un semestre pour commencer",
                    size=15,
                    color="#64748b",
                    weight=ft.FontWeight.W_400
                )
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Boutons de sélection du semestre
        semester_buttons = ft.Row([
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Column([
                        ft.Text("📚", size=32),
                        ft.Text("Premier semestre", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("Septembre - Janvier", size=12, color="#64748b")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    on_click=lambda e: self.show_semester_classes("premier"),
                    bgcolor="#4f46e5",
                    color="#ffffff",
                    width=250,
                    height=120
                ),
                margin=ft.margin.only(right=16)
            ),
            ft.Container(
                content=ft.ElevatedButton(
                    content=ft.Column([
                        ft.Text("📖", size=32),
                        ft.Text("Deuxième semestre", size=16, weight=ft.FontWeight.BOLD),
                        ft.Text("Février - Juin", size=12, color="#64748b")
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    on_click=lambda e: self.show_semester_classes("deuxieme"),
                    bgcolor="#059669",
                    color="#ffffff",
                    width=250,
                    height=120
                ),
                margin=ft.margin.only(left=16)
            )
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        content = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "📊 Choisir le semestre",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b"
                    ),
                    ft.Container(height=24),
                    semester_buttons,
                    ft.Container(height=24),
                    ft.Text(
                        "Sélectionnez le semestre pour lequel vous souhaitez gérer les notes.",
                        size=14,
                        color="#64748b",
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=48
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    content
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def show_semester_classes(self, semester):
        """Afficher les classes du semestre sélectionné"""
        self.current_semester = semester
        self.clear_main_content()
        
        semester_name = "Premier semestre" if semester == "premier" else "Deuxième semestre"
        
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon="arrow_back",
                        on_click=lambda e: self.show_grade_management(),
                        bgcolor="#ffffff",
                        icon_color="#64748b"
                    ),
                    ft.Column([
                        ft.Text(
                            f"Sélection de classe - {semester_name}",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        ),
                        ft.Text(
                            "Choisissez une classe pour gérer ses matières et notes",
                            size=15,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        )
                    ], expand=True)
                ])
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Grille des classes
        self.classes_grid = ft.GridView(
            expand=True,
            runs_count=3,
            max_extent=250,
            child_aspect_ratio=1.2,
            spacing=20,
            run_spacing=20
        )
        
        # Charger les classes existantes
        self.load_classes_for_semester()
        
        # Bouton "Calculer les moyennes"
        calculate_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon("calculate", color="#ffffff"),
                ft.Text("Calculer les moyennes", color="#ffffff", weight=ft.FontWeight.BOLD)
            ], spacing=8),
            on_click=lambda e: self.show_average_calculation_options(),
            bgcolor="#059669",
            height=48,
            tooltip="Calculer les moyennes générales des élèves"
        )
        
        content = ft.Column([
            ft.Container(
                content=ft.Row([
                    calculate_button
                ], alignment=ft.MainAxisAlignment.CENTER),
                margin=ft.margin.only(bottom=24)
            ),
            ft.Container(
                content=self.classes_grid,
                expand=True
            )
        ])
        
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    content
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
        
    def load_classes_for_semester(self):
        """Charger les classes disponibles"""
        classes = self.data_manager.get_all_classes()
        self.classes_grid.controls.clear()
        
        if not classes:
            # Message si aucune classe
            empty_state = ft.Container(
                content=ft.Column([
                    ft.Text("🏫", size=48),
                    ft.Text(
                        "Aucune classe créée",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#64748b"
                    ),
                    ft.Text(
                        "Veuillez d'abord créer des classes depuis la gestion des classes",
                        size=14,
                        color="#94a3b8",
                        text_align=ft.TextAlign.CENTER
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=48
            )
            self.classes_grid.controls.append(empty_state)
        else:
            for classe in classes:
                # Compter les élèves dans cette classe
                students = self.data_manager.get_all_students()
                student_count = len([s for s in students if s.get("classe") == classe.get("nom", "")])
                
                class_card = ft.Container(
                    content=ft.Column([
                        ft.Text(
                            classe.get("nom", ""),
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            f"{student_count} élève(s)",
                            size=14,
                            color="#64748b",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=12),
                        ft.ElevatedButton(
                            content=ft.Row([
                                ft.Icon("subject", color="#ffffff", size=16),
                                ft.Text("Matières", color="#ffffff", weight=ft.FontWeight.BOLD)
                            ], spacing=4, alignment=ft.MainAxisAlignment.CENTER),
                            on_click=lambda e, c=classe: self.show_class_subjects(c),
                            bgcolor="#4f46e5",
                            height=40,
                            width=120
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                    bgcolor="#ffffff",
                    border_radius=12,
                    padding=20,
                    border=ft.border.all(1, "#e2e8f0"),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        offset=ft.Offset(0, 2),
                        color="#00000010"
                    )
                )
                self.classes_grid.controls.append(class_card)
        
        self.page.update()
    
    def show_average_calculation_options(self):
        """Afficher les options de calcul des moyennes"""
        def option_best_two_homeworks(e):
            self.page.close(self.calculation_dialog)
            self.show_class_selection_for_averages("best_two")
        
        def option_all_homeworks(e):
            self.page.close(self.calculation_dialog)
            self.show_class_selection_for_averages("all")
        
        def cancel_calculation(e):
            self.page.close(self.calculation_dialog)
        
        self.calculation_dialog = ft.AlertDialog(
            title=ft.Text("Méthode de calcul des moyennes", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Choisissez la méthode de calcul des moyennes :",
                        size=16,
                        color="#1e293b"
                    ),
                    ft.Container(height=20),
                    ft.ElevatedButton(
                        content=ft.Column([
                            ft.Text("Option 1 : Utiliser les 2 meilleurs devoirs", 
                                   weight=ft.FontWeight.BOLD, 
                                   size=14,
                                   text_align=ft.TextAlign.CENTER),
                            ft.Container(height=8),
                            ft.Text("Seulement les 2 meilleures notes de devoirs + composition",
                                   size=12,
                                   color="#64748b",
                                   text_align=ft.TextAlign.CENTER)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        on_click=option_best_two_homeworks,
                        bgcolor="#4f46e5",
                        color="#ffffff",
                        width=400,
                        height=80
                    ),
                    ft.Container(height=16),
                    ft.ElevatedButton(
                        content=ft.Column([
                            ft.Text("Option 2 : Utiliser tous les devoirs", 
                                   weight=ft.FontWeight.BOLD, 
                                   size=14,
                                   text_align=ft.TextAlign.CENTER),
                            ft.Container(height=8),
                            ft.Text("Toutes les notes de devoirs + composition",
                                   size=12,
                                   color="#64748b",
                                   text_align=ft.TextAlign.CENTER)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        on_click=option_all_homeworks,
                        bgcolor="#059669",
                        color="#ffffff",
                        width=400,
                        height=80
                    )
                ]),
                width=450
            ),
            actions=[
                ft.TextButton("Annuler", on_click=cancel_calculation)
            ],
            modal=True
        )
        
        self.page.open(self.calculation_dialog)
    
    def show_class_selection_for_averages(self, calculation_method):
        """Afficher la sélection de classe pour le calcul des moyennes"""
        self.calculation_method = calculation_method
        
        def select_class_for_averages(classe):
            self.calculate_class_averages(classe, calculation_method)
        
        # Modifier temporairement le comportement des cartes de classe
        self.temp_class_click_handler = select_class_for_averages
        
        # Recharger les classes avec le nouveau comportement
        self.load_classes_for_semester_averages()
    
    def load_classes_for_semester_averages(self):
        """Charger les classes pour le calcul des moyennes"""
        classes = self.data_manager.get_all_classes()
        self.classes_grid.controls.clear()
        
        if not classes:
            empty_state = ft.Container(
                content=ft.Column([
                    ft.Text("🏫", size=48),
                    ft.Text(
                        "Aucune classe créée",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#64748b"
                    ),
                    ft.Text(
                        "Veuillez d'abord créer des classes",
                        size=14,
                        color="#94a3b8"
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=48
            )
            self.classes_grid.controls.append(empty_state)
        else:
            for classe in classes:
                class_card = ft.Container(
                    content=ft.Column([
                        ft.Text("🏫", size=32),
                        ft.Text(
                            classe.get("nom", ""),
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Cliquer pour calculer les moyennes",
                            size=12,
                            color="#64748b",
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                    bgcolor="#ffffff",
                    border_radius=12,
                    padding=16,
                    border=ft.border.all(1, "#e2e8f0"),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=4,
                        offset=ft.Offset(0, 2),
                        color="#00000010"
                    ),
                    on_click=lambda e, cls=classe: self.temp_class_click_handler(cls)
                )
                self.classes_grid.controls.append(class_card)
        
        self.page.update()
    
    def calculate_class_averages(self, classe, method):
        """Calculer les moyennes d'une classe selon la méthode choisie"""
        try:
            class_name = classe.get('nom', '')
            
            # Récupérer tous les élèves de cette classe
            all_students = self.data_manager.get_all_students()
            students = [s for s in all_students if s.get("classe") == class_name]
            
            if not students:
                self.show_snackbar("Aucun élève trouvé dans cette classe", error=True)
                return
            
            # Récupérer toutes les matières de cette classe pour le semestre actuel
            all_subjects = self.data_manager.get_all_subjects()
            subjects = [s for s in all_subjects 
                       if s.get("classe") == class_name and s.get("semestre") == self.current_semester]
            
            if not subjects:
                self.show_snackbar("Aucune matière trouvée pour cette classe dans ce semestre", error=True)
                return
            
            # Calculer les moyennes
            students_averages = []
            
            for student in students:
                student_id = student.get("student_id", student.get("id", ""))
                student_name = f"{student.get('prenom', '')} {student.get('nom', '')}"
                
                somme_points_eleve = 0
                somme_coef_eleve = 0
                subject_details = []
                
                for subject in subjects:
                    subject_id = subject.get("id", "")
                    subject_name = subject.get("nom", "")
                    coefficient = float(subject.get("coefficient", 1))
                    
                    # Récupérer les notes de l'élève pour cette matière
                    grades = self.data_manager.get_student_subject_grades(student_id, subject_id)
                    
                    if not grades:
                        continue  # Pas de notes pour cette matière
                    
                    # Séparer les devoirs et la composition
                    homework_notes = []
                    composition_note = None
                    
                    for grade in grades:
                        grade_type = grade.get("type", "")
                        grade_value = grade.get("note")
                        
                        if grade_value is not None and grade_value != "":
                            try:
                                grade_float = float(grade_value)
                                if grade_type == "composition":
                                    composition_note = grade_float
                                elif grade_type.startswith("devoir"):
                                    homework_notes.append(grade_float)
                            except ValueError:
                                continue
                    
                    # Calculer la moyenne de la matière selon la méthode
                    if composition_note is not None and homework_notes:
                        if method == "best_two":
                            # Option 1: Utiliser les 2 meilleurs devoirs
                            homework_notes.sort(reverse=True)  # Trier par ordre décroissant
                            if len(homework_notes) >= 2:
                                meilleur_devoir1 = homework_notes[0]
                                meilleur_devoir2 = homework_notes[1]
                                total_points = meilleur_devoir1 + meilleur_devoir2 + composition_note
                                moyenne_matiere = total_points / 3
                            elif len(homework_notes) == 1:
                                # Si un seul devoir, utiliser celui-ci deux fois
                                total_points = homework_notes[0] * 2 + composition_note
                                moyenne_matiere = total_points / 3
                            else:
                                continue
                        else:
                            # Option 2: Utiliser tous les devoirs
                            total_devoirs = sum(homework_notes)
                            total_points = total_devoirs + composition_note
                            denominateur = len(homework_notes) + 1  # +1 pour la composition
                            moyenne_matiere = total_points / denominateur
                        
                        # Ajouter à la moyenne générale
                        points_pondérés = moyenne_matiere * coefficient
                        somme_points_eleve += points_pondérés
                        somme_coef_eleve += coefficient
                        
                        subject_details.append({
                            "name": subject_name,
                            "average": round(moyenne_matiere, 2),
                            "coefficient": coefficient,
                            "homework_count": len(homework_notes)
                        })
                
                # Calculer la moyenne générale
                if somme_coef_eleve > 0:
                    moyenne_generale_eleve = somme_points_eleve / somme_coef_eleve
                    students_averages.append({
                        "student_id": student_id,
                        "name": student_name,
                        "general_average": round(moyenne_generale_eleve, 2),
                        "total_points": round(somme_points_eleve, 2),
                        "total_coefficient": int(somme_coef_eleve),
                        "subjects": subject_details
                    })
            
            # Afficher les résultats
            self.show_averages_results(classe, method, students_averages)
            
        except Exception as e:
            print(f"Erreur lors du calcul des moyennes: {e}")
            self.show_snackbar("Erreur lors du calcul des moyennes", error=True)
    
    def show_averages_results(self, classe, method, students_averages):
        """Afficher les résultats du calcul des moyennes"""
        self.clear_main_content()
        
        method_text = "2 meilleurs devoirs" if method == "best_two" else "tous les devoirs"
        semester_name = "Premier semestre" if self.current_semester == "premier" else "Deuxième semestre"
        
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon="arrow_back",
                        on_click=lambda e: self.show_semester_classes(self.current_semester),
                        bgcolor="#ffffff",
                        icon_color="#64748b"
                    ),
                    ft.Column([
                        ft.Text(
                            f"Moyennes - {classe.get('nom', '')} ({semester_name})",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        ),
                        ft.Text(
                            f"Méthode : {method_text}",
                            size=15,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        )
                    ], expand=True)
                ])
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        if not students_averages:
            content = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon("info", size=64, color="#cbd5e1"),
                        ft.Container(height=16),
                        ft.Text(
                            "Aucune moyenne calculable",
                            size=16,
                            color="#64748b",
                            text_align=ft.TextAlign.CENTER
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Les élèves doivent avoir au moins une composition et un devoir dans chaque matière",
                            size=14,
                            color="#94a3b8",
                            text_align=ft.TextAlign.CENTER
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=40,
                    alignment=ft.alignment.center
                ),
                elevation=0,
                surface_tint_color="#ffffff",
                color="#ffffff"
            )
        else:
            # Créer le tableau des résultats avec les nouvelles colonnes
            columns = [
                ft.DataColumn(ft.Text("Rang", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Prénom", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Nom", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Points totaux", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Coeff. total", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Moyenne", weight=ft.FontWeight.BOLD, size=12)),
                ft.DataColumn(ft.Text("Mention", weight=ft.FontWeight.BOLD, size=12))
            ]
            
            rows = []
            # Trier par moyenne décroissante pour le classement
            sorted_students = sorted(students_averages, key=lambda x: x["general_average"], reverse=True)
            
            for rank, student_data in enumerate(sorted_students, 1):
                # Fonction pour déterminer la mention
                def get_mention(average):
                    if average >= 16:
                        return "Très Bien"
                    elif average >= 14:
                        return "Bien"
                    elif average >= 12:
                        return "Assez Bien"
                    elif average >= 10:
                        return "Passable"
                    else:
                        return "Insuffisant"
                
                # Couleur selon la moyenne
                avg = student_data["general_average"]
                if avg >= 16:
                    avg_color = "#059669"  # Vert
                elif avg >= 14:
                    avg_color = "#0ea5e9"  # Bleu
                elif avg >= 10:
                    avg_color = "#f59e0b"  # Orange
                else:
                    avg_color = "#ef4444"  # Rouge
                
                # Couleur pour la mention
                mention = get_mention(avg)
                if mention == "Très Bien":
                    mention_color = "#059669"
                elif mention == "Bien":
                    mention_color = "#0ea5e9"
                elif mention == "Assez Bien":
                    mention_color = "#f59e0b"
                elif mention == "Passable":
                    mention_color = "#f59e0b"
                else:
                    mention_color = "#ef4444"
                
                # Séparer prénom et nom
                name_parts = student_data["name"].split(" ", 1)
                prenom = name_parts[0] if len(name_parts) > 0 else ""
                nom = name_parts[1] if len(name_parts) > 1 else ""
                
                rows.append(ft.DataRow([
                    ft.DataCell(ft.Text(str(rank), size=12, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(str(student_data["student_id"]), size=12, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(prenom, size=12, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(nom, size=12, weight=ft.FontWeight.W_500)),
                    ft.DataCell(ft.Text(f"{student_data['total_points']:.2f}", size=12)),
                    ft.DataCell(ft.Text(str(student_data["total_coefficient"]), size=12)),
                    ft.DataCell(ft.Text(f"{avg:.2f}/20", size=12, weight=ft.FontWeight.BOLD, color=avg_color)),
                    ft.DataCell(ft.Text(mention, size=12, weight=ft.FontWeight.BOLD, color=mention_color))
                ]))
            
            results_table = ft.DataTable(
                columns=columns,
                rows=rows,
                border=ft.border.all(1, "#e2e8f0"),
                border_radius=8,
                vertical_lines=ft.border.BorderSide(1, "#e2e8f0"),
                horizontal_lines=ft.border.BorderSide(1, "#e2e8f0"),
                heading_row_color="#f8fafc"
            )
            
            content = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Container(
                            content=results_table,
                            border_radius=8,
                            bgcolor="#ffffff"
                        )
                    ]),
                    padding=20
                ),
                elevation=0,
                surface_tint_color="#ffffff",
                color="#ffffff"
            )
        
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    content
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def show_class_subjects(self, classe):
        """Afficher les matières d'une classe spécifique"""
        self.current_class = classe
        self.clear_main_content()
        
        semester_name = "Premier semestre" if self.current_semester == "premier" else "Deuxième semestre"
        
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon="arrow_back",
                        on_click=lambda e: self.show_semester_classes(self.current_semester),
                        bgcolor="#ffffff",
                        icon_color="#64748b"
                    ),
                    ft.Column([
                        ft.Text(
                            f"Matières - {classe['nom']} ({semester_name})",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        ),
                        ft.Text(
                            "Gérez les matières et saisissez les notes",
                            size=15,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        )
                    ], expand=True)
                ])
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Bouton Ajouter une matière
        add_subject_button = ft.ElevatedButton(
            content=ft.Row([
                ft.Icon("add", color="#ffffff"),
                ft.Text("Ajouter une matière", color="#ffffff", weight=ft.FontWeight.BOLD)
            ], spacing=8),
            on_click=lambda e: self.show_add_subject_dialog(),
            bgcolor="#4f46e5",
            height=48
        )
        
        # Bouton Synchroniser (uniquement pour le deuxième semestre)
        sync_button = None
        if self.current_semester == "deuxieme":
            sync_button = ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon("sync", color="#ffffff"),
                    ft.Text("Synchroniser", color="#ffffff", weight=ft.FontWeight.BOLD)
                ], spacing=8),
                on_click=lambda e: self.sync_subjects_from_first_semester(),
                bgcolor="#059669",
                height=48,
                tooltip="Copier les matières et coefficients du Premier semestre"
            )
        
        # Grille des matières
        self.subjects_grid = ft.GridView(
            expand=True,
            runs_count=4,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=16,
            run_spacing=16
        )
        
        # Charger les matières existantes pour cette classe
        self.load_class_subjects()
        
        # Création de la ligne de boutons selon le semestre
        if sync_button:
            buttons_row = ft.Row([
                add_subject_button,
                ft.Container(width=16),  # Espacement
                sync_button
            ], alignment=ft.MainAxisAlignment.START)
        else:
            buttons_row = ft.Row([
                add_subject_button
            ], alignment=ft.MainAxisAlignment.START)
        
        content = ft.Column([
            buttons_row,
            ft.Container(height=24),
            ft.Container(
                content=self.subjects_grid,
                expand=True
            )
        ])
        
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    content
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.all(32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def load_class_subjects(self):
        """Charger les matières de la classe et semestre actuels"""
        subjects = self.data_manager.get_all_subjects()
        filtered_subjects = [s for s in subjects if s.get("semestre") == self.current_semester and s.get("classe") == self.current_class.get("nom", "")]
        self.subjects_grid.controls.clear()
        
        for subject in filtered_subjects:
            # Limiter le nom à 14 caractères avec des points de suspension
            subject_name = subject["nom"]
            if len(subject_name) > 14:
                display_name = subject_name[:14] + "..."
            else:
                display_name = subject_name
            
            subject_card = ft.Container(
                content=ft.Column([
                    ft.Text(
                        display_name,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color="#1e293b",
                        text_align=ft.TextAlign.CENTER,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS
                    ),
                    ft.Container(height=12),
                    ft.IconButton(
                        icon="edit_note",
                        bgcolor="#4f46e5",
                        icon_color="#ffffff",
                        on_click=lambda e, subj=subject: self.show_grades_table(subj),
                        tooltip="Saisir les notes"
                    ),
                    ft.Container(height=8),
                    ft.IconButton(
                        icon="delete",
                        icon_color="#ef4444",
                        icon_size=18,
                        tooltip="Supprimer la matière",
                        on_click=lambda e, subj=subject: self.delete_subject(subj)
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
                bgcolor="#ffffff",
                border_radius=12,
                padding=16,
                border=ft.border.all(1, "#e2e8f0"),
                shadow=ft.BoxShadow(
                    spread_radius=0,
                    blur_radius=4,
                    offset=ft.Offset(0, 2),
                    color="#00000010"
                )
            )
            self.subjects_grid.controls.append(subject_card)
        
        if not filtered_subjects:
            empty_state = ft.Container(
                content=ft.Column([
                    ft.Text("📚", size=48),
                    ft.Text(
                        "Aucune matière ajoutée",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color="#64748b"
                    ),
                    ft.Text(
                        "Cliquez sur 'Ajouter une matière' pour commencer",
                        size=14,
                        color="#94a3b8"
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                padding=48
            )
            self.subjects_grid.controls.append(empty_state)
        
        self.page.update()
    
    def show_add_subject_dialog(self):
        """Afficher le dialog d'ajout de matière"""
        # Champ de saisie avec auto-suggestion
        self.subject_name_field = ft.TextField(
            label="Nom de la matière",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            on_change=self.on_subject_name_change
        )
        
        # Champ coefficient
        self.subject_coeff_field = ft.TextField(
            label="Coefficient",
            bgcolor="#ffffff",
            border_radius=8,
            border_color="#e2e8f0",
            focused_border_color="#4f46e5",
            hint_text="Ex: 2, 3, 4...",
            width=150
        )
        
        # Liste des suggestions
        self.subject_suggestions_list = ft.Column(
            controls=[],
            spacing=0,
            height=0,
            visible=False
        )
        
        # Boutons du dialog
        save_button = ft.ElevatedButton(
            "Ajouter",
            on_click=self.save_subject,
            bgcolor="#4f46e5",
            color="#ffffff"
        )
        
        cancel_button = ft.TextButton(
            "Annuler",
            on_click=self.close_subject_dialog
        )
        
        # Contenu du dialog
        dialog_content = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Ajouter une matière",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color="#1e293b"
                ),
                ft.Container(height=16),
                self.subject_name_field,
                self.subject_suggestions_list,
                ft.Container(height=16),
                self.subject_coeff_field,
                ft.Container(height=24),
                ft.Row([
                    cancel_button,
                    save_button
                ], alignment=ft.MainAxisAlignment.END, spacing=12)
            ]),
            padding=24,
            width=400
        )
        
        self.subject_dialog = ft.AlertDialog(
            content=dialog_content,
            modal=True
        )
        
        self.page.open(self.subject_dialog)
    
    def on_subject_name_change(self, e):
        """Gérer les suggestions de matières"""
        query = e.control.value.lower()
        
        # Liste des matières communes
        common_subjects = [
            "Mathématiques", "Français", "Anglais", "Histoire", "Géographie",
            "Sciences", "Physique", "Chimie", "Biologie", "Philosophie",
            "Économie", "Arts plastiques", "Musique", "Sport", "Informatique",
            "Allemand", "Espagnol", "Latin", "Grec", "Sciences sociales"
        ]
        
        if len(query) >= 2:
            suggestions = [s for s in common_subjects if query in s.lower()]
            
            if suggestions:
                self.subject_suggestions_list.controls.clear()
                for suggestion in suggestions[:5]:  # Limiter à 5 suggestions
                    suggestion_button = ft.Container(
                        content=ft.Text(suggestion, size=14),
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        bgcolor="#f8fafc",
                        border_radius=4,
                        on_click=lambda e, subj=suggestion: self.select_subject_suggestion(subj)
                    )
                    self.subject_suggestions_list.controls.append(suggestion_button)
                
                self.subject_suggestions_list.height = len(suggestions) * 36
                self.subject_suggestions_list.visible = True
            else:
                self.subject_suggestions_list.height = 0
                self.subject_suggestions_list.visible = False
        else:
            self.subject_suggestions_list.height = 0
            self.subject_suggestions_list.visible = False
        
        self.page.update()
    
    def select_subject_suggestion(self, subject_name):
        """Sélectionner une suggestion de matière"""
        self.subject_name_field.value = subject_name
        self.subject_suggestions_list.height = 0
        self.subject_suggestions_list.visible = False
        self.page.update()
    
    def save_subject(self, e):
        """Sauvegarder une nouvelle matière"""
        if not self.subject_name_field.value:
            self.show_snackbar("Le nom de la matière est obligatoire", error=True)
            return
        
        if not self.subject_coeff_field.value:
            self.show_snackbar("Le coefficient est obligatoire", error=True)
            return
        
        try:
            coefficient = float(self.subject_coeff_field.value)
            if coefficient <= 0:
                self.show_snackbar("Le coefficient doit être positif", error=True)
                return
        except ValueError:
            self.show_snackbar("Le coefficient doit être un nombre", error=True)
            return
        
        subject_data = {
            "id": f"{self.current_semester}_{self.current_class.get('nom', '')}_{len([s for s in self.data_manager.get_all_subjects() if s.get('semestre') == self.current_semester and s.get('classe') == self.current_class.get('nom', '')]) + 1}",
            "nom": self.subject_name_field.value,
            "coefficient": coefficient,
            "semestre": self.current_semester,
            "classe": self.current_class.get("nom", ""),
            "date_creation": datetime.now().isoformat()
        }
        
        if self.data_manager.add_subject(subject_data):
            self.show_snackbar("Matière ajoutée avec succès!")
            self.close_subject_dialog(None)
            # Recharger immédiatement sans délai
            self.load_class_subjects()
            self.page.update()
        else:
            self.show_snackbar("Erreur lors de l'ajout de la matière", error=True)
    
    def close_subject_dialog(self, e):
        """Fermer le dialog de matière"""
        if hasattr(self, 'subject_dialog'):
            self.page.close(self.subject_dialog)
    
    def sync_subjects_from_first_semester(self):
        """Synchroniser les matières du premier semestre vers le deuxième semestre"""
        if self.current_semester != "deuxieme":
            self.show_snackbar("La synchronisation n'est disponible que pour le deuxième semestre", error=True)
            return
        
        # Récupérer toutes les matières
        all_subjects = self.data_manager.get_all_subjects()
        
        # Filtrer les matières du premier semestre pour la classe actuelle
        first_semester_subjects = [
            s for s in all_subjects 
            if s.get("semestre") == "premier" and s.get("classe") == self.current_class.get("nom", "")
        ]
        
        if not first_semester_subjects:
            self.show_snackbar("Aucune matière trouvée dans le premier semestre pour cette classe", error=True)
            return
        
        # Vérifier s'il existe déjà des matières dans le deuxième semestre
        second_semester_subjects = [
            s for s in all_subjects 
            if s.get("semestre") == "deuxieme" and s.get("classe") == self.current_class.get("nom", "")
        ]
        
        if second_semester_subjects:
            # Demander confirmation pour remplacer les matières existantes
            def confirm_sync(e):
                self.page.close(self.sync_dialog)
                self.perform_sync(first_semester_subjects)
            
            def cancel_sync(e):
                self.page.close(self.sync_dialog)
            
            self.sync_dialog = ft.AlertDialog(
                title=ft.Text("Confirmer la synchronisation", weight=ft.FontWeight.BOLD),
                content=ft.Text(
                    f"Il existe déjà {len(second_semester_subjects)} matière(s) dans le deuxième semestre.\n"
                    f"Voulez-vous les remplacer par les {len(first_semester_subjects)} matière(s) du premier semestre ?"
                ),
                actions=[
                    ft.TextButton("Annuler", on_click=cancel_sync),
                    ft.ElevatedButton(
                        "Synchroniser",
                        on_click=confirm_sync,
                        bgcolor="#059669",
                        color="#ffffff"
                    )
                ],
                modal=True
            )
            self.page.open(self.sync_dialog)
        else:
            # Aucune matière existante, synchroniser directement
            self.perform_sync(first_semester_subjects)
    
    def perform_sync(self, first_semester_subjects):
        """Effectuer la synchronisation des matières"""
        success_count = 0
        
        # Supprimer d'abord toutes les matières existantes du deuxième semestre
        all_subjects = self.data_manager.get_all_subjects()
        existing_second_subjects = [
            s for s in all_subjects 
            if s.get("semestre") == "deuxieme" and s.get("classe") == self.current_class.get("nom", "")
        ]
        
        for subject in existing_second_subjects:
            self.data_manager.delete_subject(subject["id"])
        
        # Copier les matières du premier semestre
        for i, subject in enumerate(first_semester_subjects):
            new_subject_data = {
                "id": f"deuxieme_{self.current_class.get('nom', '')}_{i + 1}",
                "nom": subject["nom"],
                "coefficient": subject["coefficient"],
                "semestre": "deuxieme",
                "classe": self.current_class.get("nom", ""),
                "date_creation": datetime.now().isoformat(),
                "sync_from": subject["id"]  # Référence à la matière d'origine
            }
            
            if self.data_manager.add_subject(new_subject_data):
                success_count += 1
        
        # Afficher le résultat et recharger
        if success_count > 0:
            self.show_snackbar(f"{success_count} matière(s) synchronisée(s) avec succès!")
            self.load_class_subjects()
            self.page.update()
        else:
            self.show_snackbar("Erreur lors de la synchronisation", error=True)
    
    def delete_subject(self, subject):
        """Supprimer une matière avec confirmation"""
        def confirm_delete(e):
            if self.data_manager.delete_subject(subject["id"]):
                self.show_snackbar("Matière supprimée avec succès!")
                self.page.close(self.delete_dialog)
                self.load_class_subjects()
                self.page.update()
            else:
                self.show_snackbar("Erreur lors de la suppression", error=True)
        
        def close_delete_dialog(e):
            self.page.close(self.delete_dialog)
        
        # Dialog de confirmation
        self.delete_dialog = ft.AlertDialog(
            title=ft.Text("Confirmer la suppression", weight=ft.FontWeight.BOLD),
            content=ft.Text(f"Êtes-vous sûr de vouloir supprimer la matière '{subject['nom']}' ?"),
            actions=[
                ft.TextButton("Annuler", on_click=close_delete_dialog),
                ft.ElevatedButton(
                    "Supprimer",
                    on_click=confirm_delete,
                    bgcolor="#ef4444",
                    color="#ffffff"
                )
            ],
            modal=True
        )
        
        self.page.open(self.delete_dialog)
    
    def show_grades_table(self, subject):
        """Afficher le tableau de saisie des notes pour une matière"""
        self.current_subject = subject
        self.clear_main_content()
        
        # Récupérer le nombre de devoirs configuré pour cette classe+matière+semestre
        class_name = self.current_class.get('nom', '')
        subject_id = subject.get('id', '')
        self.num_devoirs = self.data_manager.get_homework_config(
            class_name, subject_id, self.current_semester
        )
        
        semester_name = "Premier semestre" if self.current_semester == "premier" else "Deuxième semestre"
        
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon="arrow_back",
                        on_click=lambda e: self.show_class_subjects(self.current_class),
                        bgcolor="#ffffff",
                        icon_color="#64748b"
                    ),
                    ft.Column([
                        ft.Text(
                            f"Notes - {subject['nom']} - {self.current_class.get('nom', '')} ({semester_name})",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        ),
                        ft.Text(
                            "Saisissez les notes des élèves",
                            size=15,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        )
                    ], expand=True)
                ])
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Sélecteur de nombre de devoirs
        self.num_devoirs_dropdown = ft.Dropdown(
            label="Nombre de devoirs",
            width=180,
            options=[
                ft.dropdown.Option("2", "2 devoirs"),
                ft.dropdown.Option("3", "3 devoirs"),
                ft.dropdown.Option("4", "4 devoirs")
            ],
            value=str(self.num_devoirs),
            on_change=self.on_num_devoirs_change,
            bgcolor="#ffffff",
            border_color="#e2e8f0",
            focused_border_color="#4f46e5"
        )
        
        # Structure EXACTE comme la gestion des élèves avec conteneur
        self.grades_table_container = ft.Container()
        self.create_grades_table()
        
        self.main_content.content = ft.Column([
            header,
            # Conteneur 1: Boutons fixes (sans scroll)
            ft.Container(
                content=ft.Row([
                    self.num_devoirs_dropdown,
                    ft.Container(expand=True),  # Espacement
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon("settings", color="#ffffff"),
                            ft.Text("Paramètres matière", color="#ffffff", weight=ft.FontWeight.BOLD)
                        ], spacing=8),
                        on_click=lambda e: self.show_subject_settings(subject),
                        bgcolor="#6b7280",
                        height=48
                    ),
                    ft.Container(width=16),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon("save", color="#ffffff"),
                            ft.Text("Sauvegarder", color="#ffffff", weight=ft.FontWeight.BOLD)
                        ], spacing=8),
                        on_click=self.save_all_grades,
                        bgcolor="#059669",
                        height=48
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.only(left=32, right=32, top=32, bottom=16)
            ),
            # Conteneur 2: Tableau avec scroll
            ft.Container(
                content=ft.Column([
                    self.grades_table_container
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.only(left=32, right=32, bottom=32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def on_num_devoirs_change(self, e):
        """Changer le nombre de devoirs et recréer le tableau"""
        self.num_devoirs = int(e.control.value)
        
        # Sauvegarder la configuration pour cette classe+matière+semestre
        class_name = self.current_class.get('nom', '')
        subject_id = self.current_subject.get('id', '')
        self.data_manager.set_homework_config(
            class_name, subject_id, self.current_semester, self.num_devoirs
        )
        
        # Créer le conteneur avant d'appeler create_grades_table
        self.grades_table_container = ft.Container()
        self.create_grades_table()
        
        # Garder le header existant et mettre à jour seulement le contenu
        header = self.main_content.content.controls[0]  # Récupérer l'en-tête existant
        
        self.main_content.content = ft.Column([
            header,
            # Conteneur 1: Boutons fixes (sans scroll)
            ft.Container(
                content=ft.Row([
                    self.num_devoirs_dropdown,
                    ft.Container(expand=True),  # Espacement
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon("settings", color="#ffffff"),
                            ft.Text("Paramètres matière", color="#ffffff", weight=ft.FontWeight.BOLD)
                        ], spacing=8),
                        on_click=lambda e: self.show_subject_settings(self.current_subject),
                        bgcolor="#6b7280",
                        height=48
                    ),
                    ft.Container(width=16),
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon("save", color="#ffffff"),
                            ft.Text("Sauvegarder", color="#ffffff", weight=ft.FontWeight.BOLD)
                        ], spacing=8),
                        on_click=self.save_all_grades,
                        bgcolor="#059669",
                        height=48
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.only(left=32, right=32, top=32, bottom=16)
            ),
            # Conteneur 2: Tableau avec scroll
            ft.Container(
                content=ft.Column([
                    self.grades_table_container
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.only(left=32, right=32, bottom=32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def create_grades_table(self):
        """Créer le tableau des notes avec exactement le même style que les autres tableaux"""
        # Récupérer les élèves de la classe sélectionnée
        all_students = self.data_manager.get_all_students()
        students = [s for s in all_students if s.get("classe") == self.current_class.get("nom", "")]
        
        if not students:
            # Message si aucun élève - même style que les autres sections
            self.grades_table = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon("school", size=64, color="#cbd5e1"),
                        ft.Container(height=16),
                        ft.Text(
                            "Aucun élève inscrit",
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
            return
        
        # Créer les lignes du tableau
        rows = []
        self.grade_fields = {}  # Stocker les références des champs
        
        for student in students:
            student_id = student.get("student_id", student.get("id", ""))
            nom = student.get("nom", "")
            prenom = student.get("prenom", "")
            date_naissance = student.get("date_naissance", "")
            lieu_naissance = student.get("lieu_naissance", "")
            
            # Récupérer les notes existantes
            existing_grades = self.data_manager.get_student_subject_grades(
                student_id, self.current_subject["id"]
            )
            
            # Créer dictionnaire pour stocker les valeurs des devoirs
            devoir_values = {}
            composition_value = ""
            
            for grade in existing_grades:
                grade_type = grade.get("type", "")
                if grade_type.startswith("devoir"):
                    devoir_values[grade_type] = str(grade.get("note", ""))
                elif grade_type == "composition":
                    composition_value = str(grade.get("note", ""))
            
            # Créer les champs de saisie selon le nombre de devoirs
            student_fields = {}
            row_cells = [
                ft.DataCell(ft.Text(str(student_id), size=12, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(nom, size=12, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(prenom, size=12, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(date_naissance, size=12)),
                ft.DataCell(ft.Text(lieu_naissance, size=12))
            ]
            
            # Ajouter les champs pour chaque devoir
            for i in range(1, self.num_devoirs + 1):
                devoir_key = f"devoir{i}"
                devoir_value = devoir_values.get(devoir_key, "")
                
                devoir_field = ft.TextField(
                    value=devoir_value,
                    width=70,
                    height=35,
                    text_align=ft.TextAlign.CENTER,
                    border_radius=4,
                    border_color="#e2e8f0",
                    focused_border_color="#4f46e5",
                    content_padding=ft.padding.all(4),
                    text_size=12
                )
                
                student_fields[devoir_key] = devoir_field
                row_cells.append(ft.DataCell(devoir_field))
            
            # Ajouter le champ composition
            composition_field = ft.TextField(
                value=composition_value,
                width=70,
                height=35,
                text_align=ft.TextAlign.CENTER,
                border_radius=4,
                border_color="#e2e8f0",
                focused_border_color="#4f46e5",
                content_padding=ft.padding.all(4),
                text_size=12
            )
            
            student_fields["composition"] = composition_field
            row_cells.append(ft.DataCell(composition_field))
            
            # Stocker les références
            self.grade_fields[student_id] = student_fields
            
            rows.append(ft.DataRow(row_cells))
        
        # Plus de lignes vides - utilisation d'espacement via conteneur
        
        # Créer les colonnes avec le même style
        columns = [
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Nom", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Prénom", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Date naissance", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Lieu naissance", weight=ft.FontWeight.BOLD, size=12))
        ]
        
        # Ajouter les colonnes pour chaque devoir
        for i in range(1, self.num_devoirs + 1):
            columns.append(ft.DataColumn(ft.Text(f"Devoir {i}", weight=ft.FontWeight.BOLD, size=12)))
        
        # Ajouter la colonne composition
        columns.append(ft.DataColumn(ft.Text("Composition", weight=ft.FontWeight.BOLD, size=12)))
        
        # Créer le tableau avec exactement le même style que les autres
        data_table = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, "#e2e8f0"),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, "#f1f5f9"),
            horizontal_lines=ft.border.BorderSide(1, "#f1f5f9"),
            heading_row_color="#f8fafc"
        )
        
        # Structure EXACTE comme dans la gestion des élèves - juste le tableau dans une Card
        grades_table = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            f"Total: {len(students)} élève(s) - Matière: {self.current_subject['nom']}",
                            size=14,
                            color="#64748b",
                            weight=ft.FontWeight.W_500
                        )
                    ]),
                    ft.Container(height=16),
                    ft.Container(
                        content=ft.Column([
                            ft.Row(
                                controls=[data_table],
                                scroll=ft.ScrollMode.ALWAYS,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            # Espacement rigoureux en bas via conteneur vide
                            ft.Container(height=100, bgcolor="#ffffff")  
                        ], spacing=0),
                        height=max(120, len(students) * 45 + 150),
                        border_radius=8,
                        bgcolor="#ffffff",
                        border=ft.border.all(1, "#e2e8f0"),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    )
                ]),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        # Mettre à jour le conteneur comme dans gestion élèves (seulement s'il existe)
        if hasattr(self, 'grades_table_container'):
            self.grades_table_container.content = grades_table
    
    def save_all_grades(self, e):
        """Sauvegarder toutes les notes du tableau"""
        saved_count = 0
        
        for student_id, fields in self.grade_fields.items():
            # Sauvegarder chaque type de note
            for grade_type, field in fields.items():
                if field.value and field.value.strip():
                    try:
                        note = float(field.value.strip())
                        if 0 <= note <= 20:  # Validation de la note
                            grade_data = {
                                "id": f"{student_id}_{self.current_subject['id']}_{grade_type}",
                                "student_id": student_id,
                                "subject_id": self.current_subject["id"],
                                "subject_name": self.current_subject["nom"],
                                "semester": self.current_semester,
                                "type": grade_type,
                                "note": note,
                                "date_creation": datetime.now().isoformat()
                            }
                            
                            if self.data_manager.add_grade(grade_data):
                                saved_count += 1
                    except ValueError:
                        continue  # Ignorer les valeurs non numériques
        
        if saved_count > 0:
            self.show_snackbar(f"{saved_count} notes sauvegardées avec succès!")
        else:
            self.show_snackbar("Aucune note valide à sauvegarder", error=True)
    
    def show_subject_settings(self, subject):
        """Afficher la page des paramètres de matière pour gérer les élèves"""
        self.clear_main_content()
        
        semester_name = "Premier semestre" if self.current_semester == "premier" else "Deuxième semestre"
        
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.IconButton(
                        icon="arrow_back",
                        on_click=lambda e: self.show_grades_table(subject),
                        bgcolor="#ffffff",
                        icon_color="#64748b"
                    ),
                    ft.Column([
                        ft.Text(
                            f"Paramètres - {subject['nom']} - {self.current_class.get('nom', '')} ({semester_name})",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        ),
                        ft.Text(
                            "Gérez les élèves concernés par cette matière et leurs coefficients",
                            size=15,
                            color="#64748b",
                            weight=ft.FontWeight.W_400
                        )
                    ], expand=True)
                ])
            ]),
            padding=ft.padding.all(32),
            bgcolor="#f8fafc"
        )
        
        # Structure EXACTE comme la gestion des élèves avec conteneur
        self.subject_settings_table_container = ft.Container()
        self.create_subject_settings_table(subject)
        
        self.main_content.content = ft.Column([
            header,
            # Conteneur 1: Bouton fixe (sans scroll)
            ft.Container(
                content=ft.Row([
                    ft.Container(expand=True),  # Espacement
                    ft.ElevatedButton(
                        content=ft.Row([
                            ft.Icon("save", color="#ffffff"),
                            ft.Text("Enregistrer les paramètres", color="#ffffff", weight=ft.FontWeight.BOLD)
                        ], spacing=8),
                        on_click=lambda e: self.save_subject_settings(subject),
                        bgcolor="#059669",
                        height=48
                    )
                ], alignment=ft.MainAxisAlignment.END),
                padding=ft.padding.only(left=32, right=32, top=32, bottom=16)
            ),
            # Conteneur 2: Tableau avec scroll
            ft.Container(
                content=ft.Column([
                    self.subject_settings_table_container
                ], scroll=ft.ScrollMode.AUTO),
                padding=ft.padding.only(left=32, right=32, bottom=32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def create_subject_settings_table(self, subject):
        """Créer le tableau des paramètres d'élèves pour une matière"""
        # Récupérer les élèves de la classe sélectionnée
        all_students = self.data_manager.get_all_students()
        students = [s for s in all_students if s.get("classe") == self.current_class.get("nom", "")]
        
        if not students:
            # Message si aucun élève
            self.subject_settings_table = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Icon("school", size=64, color="#cbd5e1"),
                        ft.Container(height=16),
                        ft.Text(
                            "Aucun élève inscrit",
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
            return
        
        # Récupérer les paramètres existants pour cette matière
        class_name = self.current_class.get('nom', '')
        subject_id = subject.get('id', '')
        existing_settings = self.data_manager.get_student_subject_settings(
            class_name, subject_id, self.current_semester
        )
        
        # Coefficient par défaut de la matière
        default_coefficient = float(subject.get('coefficient', 1))
        
        # Créer les lignes du tableau
        rows = []
        self.subject_settings_fields = {}  # Stocker les références des champs
        
        for student in students:
            student_id = student.get("student_id", student.get("id", ""))
            nom = student.get("nom", "")
            prenom = student.get("prenom", "")
            date_naissance = student.get("date_naissance", "")
            lieu_naissance = student.get("lieu_naissance", "")
            
            # Récupérer les paramètres existants pour cet élève
            student_settings = existing_settings.get(str(student_id), {})
            is_active = student_settings.get("active", True)  # Par défaut ON
            custom_coefficient = student_settings.get("coefficient", default_coefficient)
            
            # Créer les champs
            # Switch ON/OFF
            active_switch = ft.Switch(
                value=is_active,
                active_color="#059669",
                inactive_track_color="#e2e8f0"
            )
            
            # Champ coefficient personnalisé
            coefficient_field = ft.TextField(
                value=str(custom_coefficient),
                width=80,
                height=35,
                text_align=ft.TextAlign.CENTER,
                border_radius=4,
                border_color="#e2e8f0",
                focused_border_color="#4f46e5",
                content_padding=ft.padding.all(4),
                text_size=12
            )
            
            # Stocker les références
            self.subject_settings_fields[student_id] = {
                "active": active_switch,
                "coefficient": coefficient_field
            }
            
            row_cells = [
                ft.DataCell(ft.Text(str(student_id), size=12, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(nom, size=12, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(prenom, size=12, weight=ft.FontWeight.W_500)),
                ft.DataCell(ft.Text(date_naissance, size=12)),
                ft.DataCell(ft.Text(lieu_naissance, size=12)),
                ft.DataCell(active_switch),
                ft.DataCell(coefficient_field)
            ]
            
            rows.append(ft.DataRow(row_cells))
        
        # Plus de lignes vides - utilisation d'espacement via conteneur
        
        # Créer les colonnes
        columns = [
            ft.DataColumn(ft.Text("ID", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Nom", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Prénom", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Date naissance", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Lieu naissance", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Statut matière", weight=ft.FontWeight.BOLD, size=12)),
            ft.DataColumn(ft.Text("Coefficient personnalisé", weight=ft.FontWeight.BOLD, size=12))
        ]
        
        # Créer le tableau
        data_table = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, "#e2e8f0"),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, "#f1f5f9"),
            horizontal_lines=ft.border.BorderSide(1, "#f1f5f9"),
            heading_row_color="#f8fafc"
        )
        
        # Retourner directement la Card comme dans la gestion des élèves
        # Structure EXACTE comme dans la gestion des élèves - juste le tableau dans une Card
        subject_settings_table = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            f"Total: {len(students)} élève(s) - Matière: {subject['nom']} (Coeff. par défaut: {default_coefficient})",
                            size=14,
                            color="#64748b",
                            weight=ft.FontWeight.W_500
                        )
                    ]),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Text(
                            "• ON = matière activée pour l'élève | OFF = élève dispensé",
                            size=12,
                            color="#64748b",
                            italic=True
                        )
                    ]),
                    ft.Container(height=16),
                    ft.Container(
                        content=ft.Column([
                            ft.Row(
                                controls=[data_table],
                                scroll=ft.ScrollMode.ALWAYS,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            # Espacement rigoureux en bas via conteneur vide
                            ft.Container(height=100, bgcolor="#ffffff")
                        ], spacing=0),
                        height=max(120, len(students) * 45 + 150),
                        border_radius=8,
                        bgcolor="#ffffff",
                        border=ft.border.all(1, "#e2e8f0"),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    )
                ]),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        # Mettre à jour le conteneur comme dans gestion élèves (seulement s'il existe)
        if hasattr(self, 'subject_settings_table_container'):
            self.subject_settings_table_container.content = subject_settings_table
    
    def save_subject_settings(self, subject):
        """Sauvegarder les paramètres des élèves pour cette matière"""
        student_settings = {}
        
        for student_id, fields in self.subject_settings_fields.items():
            try:
                is_active = fields["active"].value
                coefficient_value = fields["coefficient"].value.strip()
                
                if coefficient_value:
                    coefficient = float(coefficient_value)
                    if coefficient > 0:  # Validation du coefficient
                        student_settings[str(student_id)] = {
                            "active": is_active,
                            "coefficient": coefficient
                        }
            except ValueError:
                continue  # Ignorer les coefficients non valides
        
        # Sauvegarder dans le data manager
        class_name = self.current_class.get('nom', '')
        subject_id = subject.get('id', '')
        
        if self.data_manager.save_student_subject_settings(
            class_name, subject_id, self.current_semester, student_settings
        ):
            self.show_snackbar("Paramètres sauvegardés avec succès!")
        else:
            self.show_snackbar("Erreur lors de la sauvegarde", error=True)
    
    def show_schedule(self):
        """Afficher l'emploi du temps - Interface professionnelle inspirée du code HTML"""
        self.current_page = "schedule"
        self.clear_main_content()
        
        # Initialiser les variables
        self.schedule_mode = "classes"
        self.selected_class = None
        self.selected_teacher = None
        
        # Header principal
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Emploi du Temps",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                    color="#111827"
                ),
                ft.Text(
                    "Gestion simple et efficace des plannings",
                    size=16,
                    color="#6b7280"
                )
            ], 
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(32),
            bgcolor="#ffffff",
            border_radius=12,
            border=ft.border.all(1, "#e5e7eb"),
            margin=ft.margin.only(bottom=32)
        )
        
        # Menu de navigation principal (comme dans le HTML)
        nav_menu = ft.Row([
            # Carte Classes
            ft.Container(
                content=ft.Column([
                    ft.Icon(
                        "groups",
                        size=48,
                        color="#1f2937"
                    ),
                    ft.Text(
                        "Classes",
                        size=20,
                        weight=ft.FontWeight.W_600,
                        color="#111827"
                    ),
                    ft.Text(
                        "Gérer les emplois du temps par classe",
                        size=14,
                        color="#6b7280",
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16),
                bgcolor="#ffffff",
                border=ft.border.all(1, "#e5e7eb"),
                border_radius=12,
                padding=ft.padding.all(32),
                expand=True,
                on_click=lambda e: self.show_class_schedule_interface(),
                ink=True
            ),
            ft.Container(width=24),  # Espacement
            # Carte Professeurs
            ft.Container(
                content=ft.Column([
                    ft.Icon(
                        "school",
                        size=48,
                        color="#1f2937"
                    ),
                    ft.Text(
                        "Professeurs",
                        size=20,
                        weight=ft.FontWeight.W_600,
                        color="#111827"
                    ),
                    ft.Text(
                        "Consulter les plannings des enseignants",
                        size=14,
                        color="#6b7280",
                        text_align=ft.TextAlign.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16),
                bgcolor="#ffffff",
                border=ft.border.all(1, "#e5e7eb"),
                border_radius=12,
                padding=ft.padding.all(32),
                expand=True,
                on_click=lambda e: self.show_teacher_schedule_interface(),
                ink=True
            )
        ])
        
        # Conteneur principal pour les interfaces
        self.schedule_main_container = ft.Container()
        
        # Interface par défaut (menu principal)
        self.schedule_main_container.content = ft.Column([
            nav_menu
        ])
        
        self.main_content.content = ft.Column([
            header,
            ft.Container(
                content=self.schedule_main_container,
                padding=ft.padding.symmetric(horizontal=32),
                expand=True
            )
        ])
        
        self.page.update()
    
    def show_class_schedule_interface(self):
        """Interface d'emploi du temps des classes - Style professionnel"""
        
        # Header avec bouton retour
        header = ft.Container(
            content=ft.Row([
                ft.Text(
                    "Emploi du temps - Classes",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color="#111827"
                ),
                ft.Row([
                    ft.ElevatedButton(
                        text="← Retour",
                        on_click=lambda e: self.show_schedule(),
                        style=ft.ButtonStyle(
                            bgcolor="#f3f4f6",
                            color="#374151",
                            padding=ft.padding.symmetric(horizontal=16, vertical=8)
                        )
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(24),
            bgcolor="#ffffff",
            border_radius=12,
            border=ft.border.all(1, "#e5e7eb"),
            margin=ft.margin.only(bottom=24)
        )
        
        # Récupérer données
        classes = self.data_manager.get_all_classes()
        teachers = self.data_manager.get_all_teachers()
        
        # Options pour les dropdowns
        class_options = [ft.dropdown.Option(key=cls['nom'], text=cls['nom']) for cls in classes]
        teacher_options = [ft.dropdown.Option(key=f"{t['prenom']} {t['nom']}", text=f"{t['prenom']} {t['nom']}") for t in teachers]
        
        # Créer les options d'horaires (07:00 à 19:30 par tranches de 30min)
        time_options = []
        for hour in range(7, 20):
            for minute in [0, 30]:
                if hour == 19 and minute == 30:
                    break
                time_str = f"{hour:02d}:{minute:02d}"
                time_options.append(ft.dropdown.Option(key=time_str, text=time_str))
        
        # Formulaire d'ajout - Style moderne
        self.class_dropdown = ft.Dropdown(
            label="Classe",
            options=class_options,
            on_change=self.on_class_selected_new,
            border_color="#d1d5db",
            expand=True
        )
        
        self.day_dropdown = ft.Dropdown(
            label="Jour",
            options=[
                ft.dropdown.Option(key="Lundi", text="Lundi"),
                ft.dropdown.Option(key="Mardi", text="Mardi"),
                ft.dropdown.Option(key="Mercredi", text="Mercredi"),
                ft.dropdown.Option(key="Jeudi", text="Jeudi"),
                ft.dropdown.Option(key="Vendredi", text="Vendredi"),
                ft.dropdown.Option(key="Samedi", text="Samedi")
            ],
            border_color="#d1d5db",
            expand=True
        )
        
        self.start_time_dropdown = ft.Dropdown(
            label="Début",
            options=time_options,
            border_color="#d1d5db",
            expand=True
        )
        
        self.end_time_dropdown = ft.Dropdown(
            label="Fin",
            options=time_options,
            border_color="#d1d5db",
            expand=True
        )
        
        self.teacher_dropdown = ft.Dropdown(
            label="Professeur",
            options=teacher_options,
            border_color="#d1d5db",
            expand=True
        )
        
        self.subject_field = ft.TextField(
            label="Matière",
            border_color="#d1d5db",
            expand=True
        )
        
        # Conteneur formulaire
        form_container = ft.Container(
            content=ft.Column([
                # Première ligne: Classe, Jour, Début, Fin, Couleur
                ft.Row([
                    self.class_dropdown,
                    ft.Container(width=16),
                    self.day_dropdown,
                    ft.Container(width=16),
                    self.start_time_dropdown,
                    ft.Container(width=16),
                    self.end_time_dropdown
                ]),
                ft.Container(height=16),
                # Deuxième ligne: Professeur, Matière, Bouton
                ft.Row([
                    self.teacher_dropdown,
                    ft.Container(width=16),
                    self.subject_field,
                    ft.Container(width=16),
                    ft.ElevatedButton(
                        text="+ Ajouter",
                        on_click=self.add_course_new,
                        style=ft.ButtonStyle(
                            bgcolor="#1f2937",
                            color="#ffffff",
                            padding=ft.padding.symmetric(horizontal=24, vertical=16)
                        )
                    )
                ])
            ]),
            padding=ft.padding.all(24),
            bgcolor="#f9fafb",
            border_radius=8,
            margin=ft.margin.only(bottom=24)
        )
        
        # Conteneur pour la grille d'emploi du temps
        self.schedule_grid_container = ft.Container()
        
        # Interface complète
        content = ft.Column([
            header,
            ft.Container(
                content=ft.Column([
                    form_container,
                    self.schedule_grid_container
                ]),
                padding=ft.padding.all(24),
                bgcolor="#ffffff",
                border_radius=12,
                border=ft.border.all(1, "#e5e7eb")
            )
        ])
        
        self.schedule_main_container.content = content
        
        # Créer la grille vide au démarrage
        self.create_schedule_grid()
        
        # Sélectionner la première classe si disponible
        if classes:
            self.class_dropdown.value = classes[0]['nom']
            self.selected_class = classes[0]['nom']
            self.load_class_schedule()
        
        self.page.update()
    
    def create_schedule_grid(self):
        """Créer la grille d'emploi du temps - Style HTML professionnel"""
        
        # Jours de la semaine
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        
        # Créneaux horaires (8h à 19h)
        time_slots = []
        for hour in range(8, 20):
            time_slots.append(f"{hour}h")
        
        # Créer la grille avec Stack pour permettre le positionnement absolu
        grid_columns = []
        
        # Colonne des horaires
        time_column = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Text(
                        "Horaires",
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color="#111827"
                    ),
                    height=65,
                    bgcolor="#f9fafb",
                    border=ft.border.only(bottom=ft.border.BorderSide(2, "#e5e7eb")),
                    padding=ft.padding.all(16),
                    alignment=ft.alignment.center
                ),
                # Créneaux horaires
                *[
                    ft.Container(
                        content=ft.Text(
                            slot,
                            size=14,
                            weight=ft.FontWeight.W_500,
                            color="#6b7280"
                        ),
                        height=65,
                        bgcolor="#f9fafb",
                        border=ft.border.only(bottom=ft.border.BorderSide(1, "#f3f4f6")),
                        padding=ft.padding.all(8),
                        alignment=ft.alignment.center
                    ) for slot in time_slots
                ]
            ], spacing=0),
            width=80,
            bgcolor="#f9fafb",
            border=ft.border.only(right=ft.border.BorderSide(2, "#e5e7eb"))
        )
        grid_columns.append(time_column)
        
        # Colonnes des jours
        self.day_columns = {}
        for day in days:
            # Stack pour permettre le positionnement absolu des cours
            day_stack = ft.Stack(
                controls=[
                    # Background avec les lignes de séparation
                    ft.Container(
                        content=ft.Column([
                            # Header du jour
                            ft.Container(
                                content=ft.Text(
                                    day,
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color="#111827"
                                ),
                                height=65,
                                bgcolor="#f9fafb",
                                border=ft.border.only(bottom=ft.border.BorderSide(2, "#e5e7eb")),
                                alignment=ft.alignment.center
                            ),
                            # Lignes horaires
                            *[
                                ft.Container(
                                    height=65,
                                    border=ft.border.only(bottom=ft.border.BorderSide(1, "#f3f4f6"))
                                ) for _ in time_slots
                            ]
                        ], spacing=0),
                        expand=True
                    )
                ],
                expand=True
            )
            
            day_column = ft.Container(
                content=day_stack,
                border=ft.border.only(left=ft.border.BorderSide(1, "#f3f4f6")),
                expand=True
            )
            
            self.day_columns[day] = day_stack
            grid_columns.append(day_column)
        
        # Grille finale
        schedule_grid = ft.Container(
            content=ft.Row(grid_columns, spacing=0),
            bgcolor="#ffffff",
            border=ft.border.all(1, "#e5e7eb"),
            border_radius=12,
            height=780,  # 12 heures × 65px = 780px
            clip_behavior=ft.ClipBehavior.HARD_EDGE
        )
        
        self.schedule_grid_container.content = schedule_grid
    
    def on_class_selected_new(self, e):
        """Quand une classe est sélectionnée dans la nouvelle interface"""
        self.selected_class = e.control.value
        self.load_class_schedule()
    
    def load_class_schedule(self):
        """Charger l'emploi du temps d'une classe"""
        if not self.selected_class:
            return
        
        # Effacer les cours existants
        for day_stack in self.day_columns.values():
            # Garder seulement le background (premier élément)
            day_stack.controls = day_stack.controls[:1]
        
        # Récupérer les cours de cette classe
        schedules = self.data_manager.get_schedule_by_class(self.selected_class)
        
        # Ajouter chaque cours à la grille
        for schedule in schedules:
            self.add_course_to_grid(schedule)
        
        self.page.update()
    
    def add_course_to_grid(self, course_data):
        """Ajouter un bloc de cours à la grille"""
        day = course_data.get('day')
        start_time = course_data.get('start_time', '08:00')
        end_time = course_data.get('end_time', '09:00')
        subject = course_data.get('subject', '')
        teacher_name = course_data.get('teacher_name', '')
        
        if day not in self.day_columns:
            return
        
        # Calculer la position et la taille du bloc
        position = self.calculate_course_position(start_time, end_time)
        
        # Couleurs par matière
        subject_colors = {
            "Mathématiques": "#3b82f6",
            "Français": "#ef4444", 
            "Anglais": "#10b981",
            "Sciences": "#f59e0b",
            "Histoire": "#8b5cf6",
            "Géographie": "#06b6d4",
            "Sport": "#84cc16",
            "Philosophie": "#f97316",
            "Physique": "#ec4899",
            "Chimie": "#14b8a6"
        }
        
        course_color = subject_colors.get(subject, "#1f2937")
        
        # Créer le bloc de cours
        course_block = ft.Container(
            content=ft.Column([
                ft.Text(
                    subject,
                    size=12,
                    weight=ft.FontWeight.BOLD,
                    color="#ffffff",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    teacher_name,
                    size=11,
                    color="rgba(255,255,255,0.8)",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(
                    content=ft.Text(
                        f"{start_time}-{end_time}",
                        size=10,
                        color="#ffffff"
                    ),
                    bgcolor="rgba(255,255,255,0.2)",
                    padding=ft.padding.symmetric(horizontal=6, vertical=2),
                    border_radius=4
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=4),
            left=6,
            right=6,
            top=position['top'],
            height=position['height'],
            bgcolor=course_color,
            border_radius=8,
            padding=ft.padding.all(8),
            on_click=lambda e, course_id=course_data.get('id'): self.delete_course_from_grid(course_id)
        )
        
        # Ajouter le bloc à la colonne du jour
        self.day_columns[day].controls.append(course_block)
    
    def calculate_course_position(self, start_time, end_time):
        """Calculer la position d'un cours dans la grille"""
        # Convertir les heures en minutes depuis 8h00
        def time_to_minutes(time_str):
            hour, minute = map(int, time_str.split(':'))
            return (hour - 8) * 60 + minute  # Relatif à 8h00
        
        start_minutes = time_to_minutes(start_time)
        end_minutes = time_to_minutes(end_time)
        duration_minutes = end_minutes - start_minutes
        
        # Chaque heure = 65px, donc 1 minute = 65/60 px
        pixels_per_minute = 65 / 60
        
        top_position = 65 + (start_minutes * pixels_per_minute) + 2  # +65 pour le header, +2 pour marge
        height = (duration_minutes * pixels_per_minute) - 4  # -4 pour espacement
        
        return {
            'top': max(67, int(top_position)),  # Minimum après le header
            'height': max(30, int(height))  # Hauteur minimale
        }
    
    def add_course_new(self, e):
        """Ajouter un nouveau cours avec la nouvelle interface"""
        try:
            # Validation des champs
            if not all([
                self.class_dropdown.value,
                self.day_dropdown.value,
                self.start_time_dropdown.value,
                self.end_time_dropdown.value,
                self.teacher_dropdown.value,
                self.subject_field.value
            ]):
                self.show_snackbar("Veuillez remplir tous les champs", error=True)
                return
            
            # Vérifier que l'heure de fin est après l'heure de début
            start_hour, start_min = map(int, self.start_time_dropdown.value.split(':'))
            end_hour, end_min = map(int, self.end_time_dropdown.value.split(':'))
            
            if (end_hour * 60 + end_min) <= (start_hour * 60 + start_min):
                self.show_snackbar("L'heure de fin doit être après l'heure de début", error=True)
                return
            
            # Vérifier les conflits
            if self.data_manager.check_schedule_conflict(
                self.class_dropdown.value,
                self.day_dropdown.value,
                self.start_time_dropdown.value,
                self.end_time_dropdown.value
            ):
                self.show_snackbar("Conflit d'horaire détecté", error=True)
                return
            
            # Créer les données du cours
            course_data = {
                "class_name": self.class_dropdown.value,
                "day": self.day_dropdown.value,
                "start_time": self.start_time_dropdown.value,
                "end_time": self.end_time_dropdown.value,
                "teacher_name": self.teacher_dropdown.value,
                "subject": self.subject_field.value.strip()
            }
            
            # Sauvegarder
            if self.data_manager.add_schedule_slot(course_data):
                self.show_snackbar("Cours ajouté avec succès !")
                
                # Réinitialiser les champs
                self.day_dropdown.value = None
                self.start_time_dropdown.value = None
                self.end_time_dropdown.value = None
                self.teacher_dropdown.value = None
                self.subject_field.value = ""
                
                # Recharger l'emploi du temps
                self.load_class_schedule()
                self.page.update()
            else:
                self.show_snackbar("Erreur lors de l'ajout", error=True)
                
        except Exception as e:
            print(f"Erreur lors de l'ajout du cours: {e}")
            self.show_snackbar("Erreur lors de l'ajout", error=True)
    
    def delete_course_from_grid(self, course_id):
        """Supprimer un cours de la grille"""
        try:
            if self.data_manager.delete_schedule_slot(course_id):
                self.show_snackbar("Cours supprimé avec succès !")
                self.load_class_schedule()
            else:
                self.show_snackbar("Erreur lors de la suppression", error=True)
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            self.show_snackbar("Erreur lors de la suppression", error=True)
    
    def show_teacher_schedule_interface(self):
        """Interface d'emploi du temps des professeurs - Style moderne"""
        
        # Header avec bouton retour
        header = ft.Container(
            content=ft.Row([
                ft.Text(
                    "Emploi du temps - Professeurs",
                    size=24,
                    weight=ft.FontWeight.W_600,
                    color="#111827"
                ),
                ft.Row([
                    ft.ElevatedButton(
                        text="← Retour",
                        on_click=lambda e: self.show_schedule(),
                        style=ft.ButtonStyle(
                            bgcolor="#f3f4f6",
                            color="#374151",
                            padding=ft.padding.symmetric(horizontal=16, vertical=8)
                        )
                    )
                ])
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(24),
            bgcolor="#ffffff",
            border_radius=12,
            border=ft.border.all(1, "#e5e7eb"),
            margin=ft.margin.only(bottom=24)
        )
        
        # Interface simplifiée pour l'instant
        content = ft.Container(
            content=ft.Column([
                ft.Icon(
                    "school",
                    size=64,
                    color="#6b7280"
                ),
                ft.Container(height=24),
                ft.Text(
                    "Emploi du temps des professeurs",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#111827",
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=16),
                ft.Text(
                    "Cette fonctionnalité sera développée prochainement.\n\n"
                    "Elle permettra de :\n"
                    "• Voir l'emploi du temps d'un professeur spécifique\n"
                    "• Gérer les conflits d'horaires des enseignants\n"
                    "• Optimiser la répartition des cours\n"
                    "• Visualiser la charge de travail par professeur",
                    size=16,
                    color="#6b7280",
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.padding.all(80),
            bgcolor="#ffffff",
            border_radius=12,
            border=ft.border.all(1, "#e5e7eb"),
            alignment=ft.alignment.center
        )
        
        # Interface complète
        interface = ft.Column([
            header,
            content
        ])
        
        self.schedule_main_container.content = interface
        self.page.update()
    
    # =================== SUPPRESSION DES ANCIENNES FONCTIONS D'EMPLOI DU TEMPS ===================
    # Les fonctions suivantes ont été remplacées par la nouvelle interface professionnelle
    # Elles seront supprimées lors du prochain nettoyage de code
        
        if teacher_id:
            # Chercher le professeur par ID
            teachers = self.data_manager.get_all_teachers()
            teacher = None
            
            for t in teachers:
                if str(t.get('id', '')) == teacher_id:
                    teacher = t
                    break
            
            if teacher:
                # Remplir automatiquement les champs
                self.teacher_prenom_field.value = teacher.get('prenom', '')
                self.teacher_nom_field.value = teacher.get('nom', '')
                self.teacher_birth_field.value = teacher.get('date_naissance', '')
                self.teacher_subject_field.value = teacher.get('matiere', '')
                
                # Sauvegarder les infos pour utilisation ultérieure
                self.selected_teacher = teacher
            else:
                # Vider les champs si professeur non trouvé
                self.teacher_prenom_field.value = ""
                self.teacher_nom_field.value = ""
                self.teacher_birth_field.value = ""
                self.teacher_subject_field.value = ""
                self.selected_teacher = None
        else:
            # Vider tous les champs si ID vide
            self.teacher_prenom_field.value = ""
            self.teacher_nom_field.value = ""
            self.teacher_birth_field.value = ""
            self.teacher_subject_field.value = ""
            self.selected_teacher = None
        
        self.page.update()
    
    def add_schedule_slot(self, e):
        """Ajouter un créneau à l'emploi du temps"""
        try:
            # Valider les champs obligatoires
            if not self.selected_class:
                self.show_snackbar("Veuillez sélectionner une classe", error=True)
                return
            
            if not self.selected_teacher:
                self.show_snackbar("Veuillez saisir un ID professeur valide", error=True)
                return
            
            if not self.day_dropdown.value:
                self.show_snackbar("Veuillez sélectionner un jour", error=True)
                return
            
            if not self.start_time_dropdown.value or not self.end_time_dropdown.value:
                self.show_snackbar("Veuillez sélectionner les horaires", error=True)
                return
            
            # Vérifier que l'heure de fin est après l'heure de début
            start_hour = int(self.start_time_dropdown.value.split(':')[0])
            end_hour = int(self.end_time_dropdown.value.split(':')[0])
            
            if end_hour <= start_hour:
                self.show_snackbar("L'heure de fin doit être après l'heure de début", error=True)
                return
            
            # Vérifier les conflits d'horaire
            if self.data_manager.check_schedule_conflict(
                self.selected_class,
                self.day_dropdown.value,
                self.start_time_dropdown.value,
                self.end_time_dropdown.value
            ):
                self.show_snackbar("Conflit d'horaire détecté pour cette classe", error=True)
                return
            
            # Créer les données du créneau
            schedule_data = {
                "class_name": self.selected_class,
                "teacher_id": self.selected_teacher['id'],
                "teacher_name": f"{self.selected_teacher['prenom']} {self.selected_teacher['nom']}",
                "subject": self.selected_teacher.get('matiere', ''),
                "day": self.day_dropdown.value,
                "start_time": self.start_time_dropdown.value,
                "end_time": self.end_time_dropdown.value
            }
            
            # Sauvegarder dans la base de données
            if self.data_manager.add_schedule_slot(schedule_data):
                self.show_snackbar("Cours ajouté avec succès!")
                
                # Réinitialiser le formulaire (partiellement)
                self.teacher_id_field.value = ""
                self.teacher_prenom_field.value = ""
                self.teacher_nom_field.value = ""
                self.teacher_birth_field.value = ""
                self.teacher_subject_field.value = ""
                self.day_dropdown.value = None
                self.start_time_dropdown.value = None
                self.end_time_dropdown.value = None
                self.selected_teacher = None
                
                # Mettre à jour le tableau
                self.update_schedule_table()
                self.page.update()
            else:
                self.show_snackbar("Erreur lors de l'ajout du cours", error=True)
                
        except Exception as e:
            print(f"Erreur lors de l'ajout du créneau: {e}")
            self.show_snackbar("Erreur lors de l'ajout du cours", error=True)
    
    def update_schedule_table(self):
        """Mettre à jour le tableau d'emploi du temps"""
        if not self.selected_class:
            return
        
        # Récupérer les créneaux pour cette classe
        schedules = self.data_manager.get_schedule_by_class(self.selected_class)
        
        # Jours de la semaine
        days = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
        
        # Horaires (7h00 à 20h00)
        hours = [f"{h:02d}:00" for h in range(7, 21)]
        
        # Créer une grille pour organiser les cours
        schedule_grid = {}
        for day in days:
            schedule_grid[day] = {}
            for hour in hours:
                schedule_grid[day][hour] = None
        
        # Placer les cours dans la grille
        for schedule in schedules:
            day = schedule.get('day')
            start_time = schedule.get('start_time')
            end_time = schedule.get('end_time')
            
            if day in schedule_grid and start_time:
                # Calculer la durée en heures
                start_hour = int(start_time.split(':')[0])
                end_hour = int(end_time.split(':')[0])
                duration = end_hour - start_hour
                
                # Marquer les créneaux occupés
                schedule_grid[day][start_time] = {
                    'schedule': schedule,
                    'duration': duration,
                    'start': True
                }
                
                # Marquer les heures suivantes comme occupées (mais pas le début)
                for h in range(start_hour + 1, end_hour):
                    hour_str = f"{h:02d}:00"
                    if hour_str in schedule_grid[day]:
                        schedule_grid[day][hour_str] = {
                            'schedule': schedule,
                            'duration': duration,
                            'start': False
                        }
        
        # Créer le tableau visual
        table_rows = []
        
        # Ligne d'en-tête avec les jours
        header_cells = [ft.DataCell(ft.Text("Horaires", weight=ft.FontWeight.BOLD, size=12))]
        for day in days:
            header_cells.append(ft.DataCell(ft.Text(day, weight=ft.FontWeight.BOLD, size=12)))
        table_rows.append(ft.DataRow(header_cells))
        
        # Créer les lignes pour chaque horaire
        for hour in hours:
            row_cells = [ft.DataCell(ft.Text(hour, size=11, weight=ft.FontWeight.W_500))]
            
            for day in days:
                cell_content = ft.Container(
                    width=120,
                    height=40,
                    bgcolor="#f8fafc",
                    border_radius=4
                )
                
                # Vérifier s'il y a un cours à cet emplacement
                if schedule_grid[day][hour]:
                    slot_info = schedule_grid[day][hour]
                    
                    if slot_info['start']:  # C'est le début du cours
                        schedule = slot_info['schedule']
                        duration = slot_info['duration']
                        
                        # Couleurs selon la matière
                        colors = {
                            "Mathématiques": "#3b82f6",
                            "Français": "#ef4444", 
                            "Anglais": "#10b981",
                            "Sciences": "#f59e0b",
                            "Histoire": "#8b5cf6",
                            "Géographie": "#06b6d4",
                            "Sport": "#84cc16",
                            "Philosophie": "#f97316"
                        }
                        
                        subject = schedule.get('subject', '')
                        color = colors.get(subject, "#64748b")
                        
                        # Créer le bloc coloré
                        cell_content = ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    subject,
                                    size=10,
                                    weight=ft.FontWeight.BOLD,
                                    color="#ffffff",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    schedule.get('teacher_name', ''),
                                    size=9,
                                    color="#ffffff",
                                    text_align=ft.TextAlign.CENTER
                                ),
                                ft.Text(
                                    f"{duration}h",
                                    size=8,
                                    color="#ffffff",
                                    text_align=ft.TextAlign.CENTER
                                )
                            ], 
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=2),
                            width=120,
                            height=40 * duration,  # Hauteur selon la durée
                            bgcolor=color,
                            border_radius=4,
                            padding=ft.padding.all(4),
                            # Ajouter une action de suppression
                            on_click=lambda e, sched_id=schedule.get('id'): self.delete_schedule_slot(sched_id)
                        )
                    else:
                        # Partie d'un cours qui continue, cellule vide visuellement
                        cell_content = ft.Container(
                            width=120,
                            height=40,
                            bgcolor="transparent"
                        )
                
                row_cells.append(ft.DataCell(cell_content))
            
            table_rows.append(ft.DataRow(row_cells))
        
        # Créer le DataTable
        data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("", size=12)),  # Colonne horaires
                *[ft.DataColumn(ft.Text(day, weight=ft.FontWeight.BOLD, size=12)) for day in days]
            ],
            rows=table_rows,
            border=ft.border.all(1, "#e2e8f0"),
            border_radius=8,
            heading_row_color="#f8fafc"
        )
        
        # Créer le conteneur avec espacement rigoureux
        schedule_table = ft.Card(
            content=ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            f"Emploi du temps - {self.selected_class}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color="#1e293b"
                        )
                    ]),
                    ft.Container(height=8),
                    ft.Row([
                        ft.Text(
                            "• Cliquer sur un cours pour le supprimer",
                            size=12,
                            color="#64748b",
                            italic=True
                        )
                    ]),
                    ft.Container(height=16),
                    ft.Container(
                        content=ft.Column([
                            ft.Row(
                                controls=[data_table],
                                scroll=ft.ScrollMode.ALWAYS,
                                vertical_alignment=ft.CrossAxisAlignment.START
                            ),
                            # Espacement rigoureux en bas
                            ft.Container(height=100, bgcolor="#ffffff")
                        ], spacing=0),
                        height=max(400, len(hours) * 45 + 150),
                        border_radius=8,
                        bgcolor="#ffffff",
                        border=ft.border.all(1, "#e2e8f0"),
                        clip_behavior=ft.ClipBehavior.HARD_EDGE
                    )
                ]),
                padding=24
            ),
            elevation=0,
            surface_tint_color="#ffffff",
            color="#ffffff"
        )
        
        self.schedule_table_container.content = schedule_table
        self.page.update()
    
    def delete_schedule_slot(self, schedule_id):
        """Supprimer un créneau d'emploi du temps"""
        try:
            if self.data_manager.delete_schedule_slot(schedule_id):
                self.show_snackbar("Cours supprimé avec succès!")
                self.update_schedule_table()
            else:
                self.show_snackbar("Erreur lors de la suppression", error=True)
        except Exception as e:
            print(f"Erreur lors de la suppression: {e}")
            self.show_snackbar("Erreur lors de la suppression", error=True)
    
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
    
    def open_teacher_date_picker(self, e):
        """Ouvrir le sélecteur de date pour le professeur"""
        if not hasattr(self, 'teacher_date_picker'):
            self.teacher_date_picker = ft.DatePicker(
                first_date=datetime(1950, 1, 1),
                last_date=datetime.now(),
                on_change=self.on_teacher_date_picked
            )
            self.page.overlay.append(self.teacher_date_picker)
        
        self.teacher_date_picker.open = True
        self.page.update()
    
    def on_teacher_date_picked(self, e):
        """Traiter la date sélectionnée pour le professeur"""
        if e.control.value:
            selected_date = e.control.value
            formatted_date = selected_date.strftime("%Y-%m-%d")
            self.teacher_dob_field.value = formatted_date
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
