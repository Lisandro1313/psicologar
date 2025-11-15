"""
Vista del Dashboard - Resumen y estadísticas
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.controllers.paciente_controller import PacienteController
from src.controllers.turno_controller import TurnoController
from datetime import date

class DashboardView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del dashboard"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("Dashboard")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Grid de tarjetas de estadísticas
        stats_grid = QGridLayout()
        stats_grid.setSpacing(20)
        
        # Tarjeta: Pacientes Activos
        self.card_pacientes = self.create_stat_card(
            "👥", "Pacientes Activos", "0", "#3498db"
        )
        stats_grid.addWidget(self.card_pacientes, 0, 0)
        
        # Tarjeta: Citas Hoy
        self.card_citas_hoy = self.create_stat_card(
            "📅", "Citas Hoy", "0", "#2ecc71"
        )
        stats_grid.addWidget(self.card_citas_hoy, 0, 1)
        
        # Tarjeta: Sesiones Este Mes
        self.card_sesiones_mes = self.create_stat_card(
            "📊", "Sesiones Este Mes", "0", "#9b59b6"
        )
        stats_grid.addWidget(self.card_sesiones_mes, 0, 2)
        
        # Tarjeta: Próximas Citas
        self.card_proximas = self.create_stat_card(
            "⏰", "Próximas 24h", "0", "#e74c3c"
        )
        stats_grid.addWidget(self.card_proximas, 0, 3)
        
        layout.addLayout(stats_grid)
        
        # Sección de accesos rápidos
        quick_access = QLabel("Accesos Rápidos")
        quick_access.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout.addWidget(quick_access)
        
        quick_buttons = QHBoxLayout()
        quick_buttons.setSpacing(15)
        
        layout.addLayout(quick_buttons)
        
        layout.addStretch()
        
        # Cargar datos
        self.load_stats()
    
    def create_stat_card(self, icon, title, value, color):
        """Crea una tarjeta de estadística"""
        card = QFrame()
        card.setObjectName("stat-card")
        card.setStyleSheet(f"""
            #stat-card {{
                background-color: white;
                border-radius: 10px;
                border-left: 5px solid {color};
                padding: 20px;
            }}
            #stat-card:hover {{
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(10)
        
        # Icono
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 32))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(icon_label)
        
        # Valor
        value_label = QLabel(value)
        value_label.setObjectName("stat-value")
        value_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(value_label)
        
        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #7f8c8d;")
        card_layout.addWidget(title_label)
        
        card.value_label = value_label  # Guardar referencia para actualizar
        
        return card
    
    def load_stats(self):
        """Carga las estadísticas del dashboard"""
        # Contar pacientes activos
        total_pacientes = PacienteController.contar_pacientes_activos()
        self.card_pacientes.value_label.setText(str(total_pacientes))
        
        # Contar citas de hoy
        citas_hoy = TurnoController.contar_turnos_hoy()
        self.card_citas_hoy.value_label.setText(str(citas_hoy))
        
        # Sesiones del mes (se implementará con el controlador)
        # Por ahora dejamos en 0
        self.card_sesiones_mes.value_label.setText("0")
        
        # Próximas citas en 24h
        proximos = TurnoController.obtener_proximos_turnos(1)
        self.card_proximas.value_label.setText(str(len(proximos)))
    
    def showEvent(self, event):
        """Se ejecuta cuando la vista se muestra"""
        super().showEvent(event)
        self.load_stats()
