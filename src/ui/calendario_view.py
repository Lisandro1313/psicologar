"""
Vista del calendario de turnos
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QCalendarWidget, QListWidget, QListWidgetItem, QDialog,
                             QFormLayout, QDateEdit, QTimeEdit, QComboBox, QTextEdit,
                             QDialogButtonBox, QMessageBox)
from PyQt6.QtCore import Qt, QDate, QTime
from PyQt6.QtGui import QFont
from src.controllers.turno_controller import TurnoController
from src.controllers.paciente_controller import PacienteController
from src.models.turno import Turno

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
        
        # Cargar turnos de la fecha seleccionada
        self.lista_turnos.clear()
        fecha_iso = fecha.toString("yyyy-MM-dd")
        turnos = TurnoController.obtener_turnos_fecha(fecha_iso)
        
        if not turnos:
            item = QListWidgetItem("📭 No hay turnos programados para este día")
            item.setForeground(Qt.GlobalColor.gray)
            self.lista_turnos.addItem(item)
        else:
            for turno in turnos:
                nombre_paciente = f"{turno['nombre']} {turno['apellido']}"
                hora = turno['hora_inicio'] or "Sin hora"
                estado_emoji = "✅" if turno['estado'] == "realizado" else "📅"
                item_text = f"{estado_emoji} {hora} - {nombre_paciente}"
                
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, turno['id'])
                self.lista_turnos.addItem(item)
    
    def nuevo_turno(self):
        """Abre el diálogo para crear un nuevo turno"""
        dialogo = TurnoDialog(self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            turno = dialogo.get_turno()
            try:
                TurnoController.crear_turno(turno)
                QMessageBox.information(self, "Éxito", "Turno creado correctamente")
                # Recargar turnos de la fecha actual
                self.fecha_seleccionada(self.calendario.selectedDate())
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear turno:\n{str(e)}")


class TurnoDialog(QDialog):
    """Diálogo para crear/editar turnos"""
    
    def __init__(self, parent=None, turno=None):
        super().__init__(parent)
        self.turno = turno
        
        titulo = "Editar Turno" if turno else "Nuevo Turno"
        self.setWindowTitle(titulo)
        self.setMinimumWidth(500)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # Paciente
        self.combo_paciente = QComboBox()
        self.cargar_pacientes()
        form_layout.addRow("Paciente:", self.combo_paciente)
        
        # Fecha
        self.date_turno = QDateEdit()
        self.date_turno.setCalendarPopup(True)
        self.date_turno.setDate(QDate.currentDate())
        form_layout.addRow("Fecha:", self.date_turno)
        
        # Hora inicio
        self.time_inicio = QTimeEdit()
        self.time_inicio.setDisplayFormat("HH:mm")
        self.time_inicio.setTime(QTime(10, 0))
        form_layout.addRow("Hora inicio:", self.time_inicio)
        
        # Hora fin
        self.time_fin = QTimeEdit()
        self.time_fin.setDisplayFormat("HH:mm")
        self.time_fin.setTime(QTime(11, 0))
        form_layout.addRow("Hora fin:", self.time_fin)
        
        # Estado
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["programado", "realizado", "cancelado", "ausente"])
        form_layout.addRow("Estado:", self.combo_estado)
        
        # Tipo
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["sesion", "evaluacion", "seguimiento"])
        form_layout.addRow("Tipo:", self.combo_tipo)
        
        # Notas
        self.txt_notas = QTextEdit()
        self.txt_notas.setMaximumHeight(100)
        self.txt_notas.setPlaceholderText("Notas adicionales sobre el turno...")
        form_layout.addRow("Notas:", self.txt_notas)
        
        layout.addLayout(form_layout)
        
        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Cargar datos si es edición
        if self.turno:
            self.cargar_datos_turno()
    
    def cargar_pacientes(self):
        """Carga la lista de pacientes activos"""
        pacientes = PacienteController.obtener_todos_pacientes(estado='activo')
        for paciente in pacientes:
            self.combo_paciente.addItem(
                f"{paciente.apellido}, {paciente.nombre}",
                paciente.id
            )
    
    def cargar_datos_turno(self):
        """Carga los datos del turno en el formulario"""
        # Aquí se cargarían los datos del turno si es edición
        pass
    
    def get_turno(self):
        """Obtiene el objeto Turno con los datos del formulario"""
        if self.turno:
            turno = self.turno
        else:
            turno = Turno()
        
        turno.paciente_id = self.combo_paciente.currentData()
        turno.fecha = self.date_turno.date().toString("yyyy-MM-dd")
        turno.hora_inicio = self.time_inicio.time().toString("HH:mm")
        turno.hora_fin = self.time_fin.time().toString("HH:mm")
        turno.estado = self.combo_estado.currentText()
        turno.tipo = self.combo_tipo.currentText()
        turno.notas = self.txt_notas.toPlainText().strip()
        
        return turno
    
    def accept(self):
        """Valida los datos antes de aceptar"""
        if not self.combo_paciente.currentData():
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente")
            return
        
        super().accept()
