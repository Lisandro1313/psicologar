"""
Vista de gestión de pacientes
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox,
                             QHeaderView, QDialog, QFormLayout, QTextEdit, QDateEdit,
                             QComboBox, QDialogButtonBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from src.controllers.paciente_controller import PacienteController
from src.models.paciente import Paciente

class PacientesView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Gestión de Pacientes")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Barra de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar paciente...")
        self.search_input.setMinimumWidth(300)
        self.search_input.textChanged.connect(self.buscar_pacientes)
        header_layout.addWidget(self.search_input)
        
        # Botón nuevo paciente
        btn_nuevo = QPushButton("➕ Nuevo Paciente")
        btn_nuevo.clicked.connect(self.abrir_dialogo_nuevo_paciente)
        header_layout.addWidget(btn_nuevo)
        
        layout.addLayout(header_layout)
        
        # Tabla de pacientes
        self.tabla_pacientes = QTableWidget()
        self.tabla_pacientes.setColumnCount(7)
        self.tabla_pacientes.setHorizontalHeaderLabels([
            "ID", "Nombre", "Apellido", "DNI", "Edad", "Teléfono", "Estado"
        ])
        
        # Configurar tabla
        self.tabla_pacientes.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabla_pacientes.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_pacientes.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabla_pacientes.setAlternatingRowColors(True)
        self.tabla_pacientes.doubleClicked.connect(self.editar_paciente)
        
        layout.addWidget(self.tabla_pacientes)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        btn_ver = QPushButton("👁 Ver Detalles")
        btn_ver.clicked.connect(self.ver_paciente)
        buttons_layout.addWidget(btn_ver)
        
        btn_editar = QPushButton("✏ Editar")
        btn_editar.clicked.connect(self.editar_paciente)
        buttons_layout.addWidget(btn_editar)
        
        btn_eliminar = QPushButton("🗑 Dar de Baja")
        btn_eliminar.clicked.connect(self.eliminar_paciente)
        btn_eliminar.setStyleSheet("background-color: #e74c3c;")
        buttons_layout.addWidget(btn_eliminar)
        
        layout.addLayout(buttons_layout)
        
        # Cargar pacientes
        self.cargar_pacientes()
    
    def cargar_pacientes(self):
        """Carga la lista de pacientes en la tabla"""
        pacientes = PacienteController.obtener_todos_pacientes()
        self.tabla_pacientes.setRowCount(len(pacientes))
        
        for row, paciente in enumerate(pacientes):
            self.tabla_pacientes.setItem(row, 0, QTableWidgetItem(str(paciente.id)))
            self.tabla_pacientes.setItem(row, 1, QTableWidgetItem(paciente.nombre))
            self.tabla_pacientes.setItem(row, 2, QTableWidgetItem(paciente.apellido))
            self.tabla_pacientes.setItem(row, 3, QTableWidgetItem(paciente.dni or ""))
            self.tabla_pacientes.setItem(row, 4, QTableWidgetItem(str(paciente.edad) if paciente.edad else ""))
            self.tabla_pacientes.setItem(row, 5, QTableWidgetItem(paciente.telefono or ""))
            self.tabla_pacientes.setItem(row, 6, QTableWidgetItem(paciente.estado.upper()))
    
    def buscar_pacientes(self, texto):
        """Busca pacientes según el texto ingresado"""
        if texto.strip() == "":
            self.cargar_pacientes()
            return
        
        pacientes = PacienteController.buscar_pacientes(texto)
        self.tabla_pacientes.setRowCount(len(pacientes))
        
        for row, paciente in enumerate(pacientes):
            self.tabla_pacientes.setItem(row, 0, QTableWidgetItem(str(paciente.id)))
            self.tabla_pacientes.setItem(row, 1, QTableWidgetItem(paciente.nombre))
            self.tabla_pacientes.setItem(row, 2, QTableWidgetItem(paciente.apellido))
            self.tabla_pacientes.setItem(row, 3, QTableWidgetItem(paciente.dni or ""))
            self.tabla_pacientes.setItem(row, 4, QTableWidgetItem(str(paciente.edad) if paciente.edad else ""))
            self.tabla_pacientes.setItem(row, 5, QTableWidgetItem(paciente.telefono or ""))
            self.tabla_pacientes.setItem(row, 6, QTableWidgetItem(paciente.estado.upper()))
    
    def abrir_dialogo_nuevo_paciente(self):
        """Abre el diálogo para crear un nuevo paciente"""
        dialogo = PacienteDialog(self)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            paciente = dialogo.get_paciente()
            try:
                PacienteController.crear_paciente(paciente)
                QMessageBox.information(self, "Éxito", "Paciente creado correctamente")
                self.cargar_pacientes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear paciente:\n{str(e)}")
    
    def ver_paciente(self):
        """Muestra los detalles de un paciente"""
        selected_row = self.tabla_pacientes.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente")
            return
        
        paciente_id = int(self.tabla_pacientes.item(selected_row, 0).text())
        paciente = PacienteController.obtener_paciente(paciente_id)
        
        dialogo = PacienteDialog(self, paciente, solo_lectura=True)
        dialogo.exec()
    
    def editar_paciente(self):
        """Edita un paciente existente"""
        selected_row = self.tabla_pacientes.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente")
            return
        
        paciente_id = int(self.tabla_pacientes.item(selected_row, 0).text())
        paciente = PacienteController.obtener_paciente(paciente_id)
        
        dialogo = PacienteDialog(self, paciente)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            paciente_actualizado = dialogo.get_paciente()
            try:
                PacienteController.actualizar_paciente(paciente_actualizado)
                QMessageBox.information(self, "Éxito", "Paciente actualizado correctamente")
                self.cargar_pacientes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar paciente:\n{str(e)}")
    
    def eliminar_paciente(self):
        """Elimina (da de baja) un paciente"""
        selected_row = self.tabla_pacientes.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente")
            return
        
        paciente_id = int(self.tabla_pacientes.item(selected_row, 0).text())
        nombre = self.tabla_pacientes.item(selected_row, 1).text()
        apellido = self.tabla_pacientes.item(selected_row, 2).text()
        
        respuesta = QMessageBox.question(
            self, "Confirmar", 
            f"¿Está seguro de dar de baja a {nombre} {apellido}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                PacienteController.eliminar_paciente(paciente_id)
                QMessageBox.information(self, "Éxito", "Paciente dado de baja correctamente")
                self.cargar_pacientes()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al dar de baja:\n{str(e)}")
    
    def showEvent(self, event):
        """Se ejecuta cuando la vista se muestra"""
        super().showEvent(event)
        self.cargar_pacientes()


class PacienteDialog(QDialog):
    """Diálogo para crear/editar pacientes"""
    
    def __init__(self, parent=None, paciente=None, solo_lectura=False):
        super().__init__(parent)
        self.paciente = paciente
        self.solo_lectura = solo_lectura
        
        if paciente:
            titulo = "Ver Paciente" if solo_lectura else "Editar Paciente"
        else:
            titulo = "Nuevo Paciente"
        
        self.setWindowTitle(titulo)
        self.setMinimumWidth(600)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # Campos del formulario
        self.txt_nombre = QLineEdit()
        self.txt_apellido = QLineEdit()
        self.txt_dni = QLineEdit()
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setCalendarPopup(True)
        self.date_nacimiento.setDate(QDate.currentDate())
        self.txt_telefono = QLineEdit()
        self.txt_email = QLineEdit()
        self.txt_direccion = QLineEdit()
        self.txt_obra_social = QLineEdit()
        self.txt_numero_afiliado = QLineEdit()
        self.txt_motivo_consulta = QTextEdit()
        self.txt_motivo_consulta.setMaximumHeight(100)
        self.txt_derivado_por = QLineEdit()
        self.combo_estado = QComboBox()
        self.combo_estado.addItems(["activo", "inactivo"])
        self.txt_notas = QTextEdit()
        self.txt_notas.setMaximumHeight(100)
        
        # Agregar campos al formulario
        form_layout.addRow("Nombre *:", self.txt_nombre)
        form_layout.addRow("Apellido *:", self.txt_apellido)
        form_layout.addRow("DNI:", self.txt_dni)
        form_layout.addRow("Fecha de Nacimiento:", self.date_nacimiento)
        form_layout.addRow("Teléfono:", self.txt_telefono)
        form_layout.addRow("Email:", self.txt_email)
        form_layout.addRow("Dirección:", self.txt_direccion)
        form_layout.addRow("Obra Social:", self.txt_obra_social)
        form_layout.addRow("N° Afiliado:", self.txt_numero_afiliado)
        form_layout.addRow("Motivo de Consulta:", self.txt_motivo_consulta)
        form_layout.addRow("Derivado Por:", self.txt_derivado_por)
        form_layout.addRow("Estado:", self.combo_estado)
        form_layout.addRow("Notas:", self.txt_notas)
        
        layout.addLayout(form_layout)
        
        # Botones
        if not self.solo_lectura:
            button_box = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            )
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)
            layout.addWidget(button_box)
        else:
            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
            button_box.rejected.connect(self.reject)
            layout.addWidget(button_box)
        
        # Cargar datos si es edición
        if self.paciente:
            self.cargar_datos_paciente()
        
        # Deshabilitar campos si es solo lectura
        if self.solo_lectura:
            self.deshabilitar_campos()
    
    def cargar_datos_paciente(self):
        """Carga los datos del paciente en el formulario"""
        self.txt_nombre.setText(self.paciente.nombre)
        self.txt_apellido.setText(self.paciente.apellido)
        self.txt_dni.setText(self.paciente.dni or "")
        
        if self.paciente.fecha_nacimiento:
            fecha = QDate.fromString(str(self.paciente.fecha_nacimiento), "yyyy-MM-dd")
            self.date_nacimiento.setDate(fecha)
        
        self.txt_telefono.setText(self.paciente.telefono or "")
        self.txt_email.setText(self.paciente.email or "")
        self.txt_direccion.setText(self.paciente.direccion or "")
        self.txt_obra_social.setText(self.paciente.obra_social or "")
        self.txt_numero_afiliado.setText(self.paciente.numero_afiliado or "")
        self.txt_motivo_consulta.setText(self.paciente.motivo_consulta or "")
        self.txt_derivado_por.setText(self.paciente.derivado_por or "")
        self.combo_estado.setCurrentText(self.paciente.estado)
        self.txt_notas.setText(self.paciente.notas or "")
    
    def deshabilitar_campos(self):
        """Deshabilita todos los campos del formulario"""
        for widget in [self.txt_nombre, self.txt_apellido, self.txt_dni, self.date_nacimiento,
                      self.txt_telefono, self.txt_email, self.txt_direccion, self.txt_obra_social,
                      self.txt_numero_afiliado, self.txt_motivo_consulta, self.txt_derivado_por,
                      self.combo_estado, self.txt_notas]:
            widget.setEnabled(False)
    
    def get_paciente(self):
        """Obtiene el objeto Paciente con los datos del formulario"""
        if self.paciente:
            paciente = self.paciente
        else:
            paciente = Paciente()
        
        paciente.nombre = self.txt_nombre.text().strip()
        paciente.apellido = self.txt_apellido.text().strip()
        paciente.dni = self.txt_dni.text().strip()
        paciente.fecha_nacimiento = self.date_nacimiento.date().toString("yyyy-MM-dd")
        paciente.telefono = self.txt_telefono.text().strip()
        paciente.email = self.txt_email.text().strip()
        paciente.direccion = self.txt_direccion.text().strip()
        paciente.obra_social = self.txt_obra_social.text().strip()
        paciente.numero_afiliado = self.txt_numero_afiliado.text().strip()
        paciente.motivo_consulta = self.txt_motivo_consulta.toPlainText().strip()
        paciente.derivado_por = self.txt_derivado_por.text().strip()
        paciente.estado = self.combo_estado.currentText()
        paciente.notas = self.txt_notas.toPlainText().strip()
        
        return paciente
    
    def accept(self):
        """Valida los datos antes de aceptar"""
        if not self.txt_nombre.text().strip():
            QMessageBox.warning(self, "Advertencia", "El nombre es obligatorio")
            return
        
        if not self.txt_apellido.text().strip():
            QMessageBox.warning(self, "Advertencia", "El apellido es obligatorio")
            return
        
        super().accept()
