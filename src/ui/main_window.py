"""
Ventana principal de la aplicación
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from src.database.db_manager import db
from src.ui.pacientes_view import PacientesView
from src.ui.calendario_view import CalendarioView
from src.ui.dashboard_view import DashboardView
from src.ui.sesiones_view import SesionesView
from src.ui.analisis_ia_view import AnalisisIAView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PsicolaRG - Sistema de Gestión para Psicólogos")
        self.setMinimumSize(1200, 800)
        
        # Conectar a la base de datos
        try:
            db.connect()
        except Exception as e:
            QMessageBox.critical(self, "Error de Base de Datos", 
                               f"No se pudo conectar a la base de datos:\n{str(e)}")
            return
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Panel lateral de navegación
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Área de contenido
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area)
        
        # Crear vistas
        self.dashboard_view = DashboardView()
        self.pacientes_view = PacientesView()
        self.calendario_view = CalendarioView()
        self.sesiones_view = SesionesView()
        self.analisis_ia_view = AnalisisIAView()
        
        # Agregar vistas al stack
        self.content_area.addWidget(self.dashboard_view)
        self.content_area.addWidget(self.pacientes_view)
        self.content_area.addWidget(self.calendario_view)
        self.content_area.addWidget(self.sesiones_view)
        self.content_area.addWidget(self.analisis_ia_view)
        
        # Mostrar dashboard por defecto
        self.content_area.setCurrentWidget(self.dashboard_view)
        
        # Aplicar estilos
        self.apply_styles()
    
    def create_sidebar(self):
        """Crea el panel lateral de navegación"""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        
        layout = QVBoxLayout(sidebar)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 20, 10, 10)
        
        # Logo/Título
        title = QLabel("PsicolaRG")
        title.setObjectName("app-title")
        title_font = QFont("Arial", 24, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        subtitle = QLabel("Gestión Profesional")
        subtitle.setObjectName("app-subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addSpacing(30)
        
        # Botones de navegación
        self.btn_dashboard = self.create_nav_button("🏠 Dashboard", 0)
        self.btn_pacientes = self.create_nav_button("👥 Pacientes", 1)
        self.btn_calendario = self.create_nav_button("📅 Calendario", 2)
        self.btn_sesiones = self.create_nav_button("📝 Sesiones", 3)
        self.btn_analisis_ia = self.create_nav_button("🤖 Análisis IA", 4)
        
        layout.addWidget(self.btn_dashboard)
        layout.addWidget(self.btn_pacientes)
        layout.addWidget(self.btn_calendario)
        layout.addWidget(self.btn_sesiones)
        layout.addWidget(self.btn_analisis_ia)
        
        layout.addStretch()
        
        # Información del usuario
        user_info = QLabel("👤 Dr. Usuario")
        user_info.setObjectName("user-info")
        layout.addWidget(user_info)
        
        return sidebar
    
    def create_nav_button(self, text, index):
        """Crea un botón de navegación"""
        btn = QPushButton(text)
        btn.setObjectName("nav-button")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setMinimumHeight(50)
        btn.clicked.connect(lambda: self.change_view(index))
        return btn
    
    def change_view(self, index):
        """Cambia la vista actual"""
        self.content_area.setCurrentIndex(index)
        
        # Actualizar estilos de botones activos
        buttons = [self.btn_dashboard, self.btn_pacientes, self.btn_calendario, self.btn_sesiones, self.btn_analisis_ia]
        for i, btn in enumerate(buttons):
            if i == index:
                btn.setProperty("active", True)
            else:
                btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
    
    def apply_styles(self):
        """Aplica estilos CSS a la aplicación"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            
            #sidebar {
                background-color: #2c3e50;
                color: white;
            }
            
            #app-title {
                color: #3498db;
                margin: 20px 0 5px 0;
            }
            
            #app-subtitle {
                color: #bdc3c7;
                font-size: 12px;
                margin-bottom: 10px;
            }
            
            #nav-button {
                background-color: transparent;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
            }
            
            #nav-button:hover {
                background-color: #34495e;
            }
            
            #nav-button[active="true"] {
                background-color: #3498db;
            }
            
            #user-info {
                color: #bdc3c7;
                padding: 10px;
                border-top: 1px solid #34495e;
                font-size: 13px;
            }
            
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #2980b9;
            }
            
            QPushButton:pressed {
                background-color: #21618c;
            }
            
            QLineEdit, QTextEdit, QDateEdit, QComboBox {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
            }
            
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #3498db;
            }
            
            QLabel {
                font-size: 13px;
            }
        """)
    
    def closeEvent(self, event):
        """Maneja el cierre de la aplicación"""
        db.disconnect()
        event.accept()
