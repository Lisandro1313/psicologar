"""
Vista del calendario de turnos
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QCalendarWidget, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont

class CalendarioView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del calendario"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Calendario de Turnos")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        btn_nuevo_turno = QPushButton("➕ Nuevo Turno")
        btn_nuevo_turno.clicked.connect(self.nuevo_turno)
        header_layout.addWidget(btn_nuevo_turno)
        
        layout.addLayout(header_layout)
        
        # Contenedor principal
        main_container = QHBoxLayout()
        
        # Calendario
        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        self.calendario.clicked.connect(self.fecha_seleccionada)
        main_container.addWidget(self.calendario, 2)
        
        # Panel de turnos del día
        turnos_panel = QVBoxLayout()
        
        self.label_fecha_sel = QLabel("Turnos del día")
        self.label_fecha_sel.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        turnos_panel.addWidget(self.label_fecha_sel)
        
        self.lista_turnos = QListWidget()
        self.lista_turnos.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:hover {
                background-color: #ecf0f1;
            }
        """)
        turnos_panel.addWidget(self.lista_turnos)
        
        main_container.addLayout(turnos_panel, 1)
        
        layout.addLayout(main_container)
        
        # Cargar turnos de hoy
        self.fecha_seleccionada(QDate.currentDate())
    
    def fecha_seleccionada(self, fecha):
        """Maneja el evento de selección de fecha"""
        fecha_str = fecha.toString("dd/MM/yyyy")
        self.label_fecha_sel.setText(f"Turnos del {fecha_str}")
        
        # Aquí se cargarían los turnos de la BD
        self.lista_turnos.clear()
        
        # Ejemplo de turnos (temporal)
        self.lista_turnos.addItem("📅 10:00 - Juan Pérez")
        self.lista_turnos.addItem("📅 11:30 - María García")
        self.lista_turnos.addItem("📅 15:00 - Carlos López")
    
    def nuevo_turno(self):
        """Abre el diálogo para crear un nuevo turno"""
        # Aquí se implementará el diálogo de nuevo turno
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(self, "Próximamente", "Función de nuevo turno en desarrollo")
