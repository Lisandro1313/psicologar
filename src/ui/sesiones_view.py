"""
Vista de gestión de sesiones
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QListWidget, QListWidgetItem, QTextEdit, QLineEdit,
                             QMessageBox, QDialog, QFormLayout, QDateEdit, QSpinBox,
                             QDialogButtonBox, QSplitter, QGroupBox, QComboBox)
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QFont
from src.controllers.sesion_controller import SesionController
from src.controllers.paciente_controller import PacienteController
from src.models.sesion import Sesion
from src.services.ia_analysis_service import ia_service

class SesionesView(QWidget):
    def __init__(self):
        super().__init__()
        self.paciente_actual = None
        self.sesion_actual = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Registro de Sesiones")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Selector de paciente
        self.combo_pacientes = QComboBox()
        self.combo_pacientes.setMinimumWidth(300)
        self.combo_pacientes.currentIndexChanged.connect(self.cambiar_paciente)
        header_layout.addWidget(QLabel("Paciente:"))
        header_layout.addWidget(self.combo_pacientes)
        
        # Botón nueva sesión
        btn_nueva = QPushButton("➕ Nueva Sesión")
        btn_nueva.clicked.connect(self.nueva_sesion)
        header_layout.addWidget(btn_nueva)
        
        layout.addLayout(header_layout)
        
        # Splitter principal (lista de sesiones | detalles)
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Panel izquierdo: Lista de sesiones
        panel_izq = QWidget()
        layout_izq = QVBoxLayout(panel_izq)
        layout_izq.setContentsMargins(0, 0, 0, 0)
        
        # Barra de búsqueda
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Buscar en sesiones...")
        self.search_input.textChanged.connect(self.buscar_sesiones)
        layout_izq.addWidget(self.search_input)
        
        # Lista de sesiones
        self.lista_sesiones = QListWidget()
        self.lista_sesiones.itemClicked.connect(self.seleccionar_sesion)
        self.lista_sesiones.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #ecf0f1;
            }
        """)
        layout_izq.addWidget(self.lista_sesiones)
        
        # Contador de sesiones
        self.label_total = QLabel("Total de sesiones: 0")
        self.label_total.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout_izq.addWidget(self.label_total)
        
        splitter.addWidget(panel_izq)
        
        # Panel derecho: Detalles de la sesión
        panel_der = QWidget()
        layout_der = QVBoxLayout(panel_der)
        layout_der.setContentsMargins(10, 0, 0, 0)
        
        # Info de la sesión seleccionada
        self.label_sesion_titulo = QLabel("Seleccione una sesión")
        self.label_sesion_titulo.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        layout_der.addWidget(self.label_sesion_titulo)
        
        self.label_sesion_fecha = QLabel("")
        self.label_sesion_fecha.setStyleSheet("color: #7f8c8d;")
        layout_der.addWidget(self.label_sesion_fecha)
        
        # Objetivos
        grupo_objetivos = QGroupBox("Objetivos de la Sesión")
        layout_objetivos = QVBoxLayout()
        self.txt_objetivos = QTextEdit()
        self.txt_objetivos.setMaximumHeight(100)
        self.txt_objetivos.setReadOnly(True)
        layout_objetivos.addWidget(self.txt_objetivos)
        grupo_objetivos.setLayout(layout_objetivos)
        layout_der.addWidget(grupo_objetivos)
        
        # Notas principales
        grupo_notas = QGroupBox("Notas de la Sesión")
        layout_notas = QVBoxLayout()
        self.txt_notas = QTextEdit()
        self.txt_notas.setReadOnly(True)
        layout_notas.addWidget(self.txt_notas)
        grupo_notas.setLayout(layout_notas)
        layout_der.addWidget(grupo_notas)
        
        # Intervenciones
        grupo_intervenciones = QGroupBox("Intervenciones Realizadas")
        layout_intervenciones = QVBoxLayout()
        self.txt_intervenciones = QTextEdit()
        self.txt_intervenciones.setMaximumHeight(100)
        self.txt_intervenciones.setReadOnly(True)
        layout_intervenciones.addWidget(self.txt_intervenciones)
        grupo_intervenciones.setLayout(layout_intervenciones)
        layout_der.addWidget(grupo_intervenciones)
        
        # Observaciones
        grupo_observaciones = QGroupBox("Observaciones")
        layout_observaciones = QVBoxLayout()
        self.txt_observaciones = QTextEdit()
        self.txt_observaciones.setMaximumHeight(80)
        self.txt_observaciones.setReadOnly(True)
        layout_observaciones.addWidget(self.txt_observaciones)
        grupo_observaciones.setLayout(layout_observaciones)
        layout_der.addWidget(grupo_observaciones)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.btn_editar = QPushButton("✏ Editar")
        self.btn_editar.clicked.connect(self.editar_sesion)
        self.btn_editar.setEnabled(False)
        buttons_layout.addWidget(self.btn_editar)
        
        self.btn_eliminar = QPushButton("🗑 Eliminar")
        self.btn_eliminar.clicked.connect(self.eliminar_sesion)
        self.btn_eliminar.setStyleSheet("background-color: #e74c3c;")
        self.btn_eliminar.setEnabled(False)
        buttons_layout.addWidget(self.btn_eliminar)
        
        self.btn_analizar = QPushButton("🤖 Analizar con IA")
        self.btn_analizar.clicked.connect(self.analizar_con_ia)
        self.btn_analizar.setStyleSheet("background-color: #9b59b6;")
        self.btn_analizar.setEnabled(False)
        buttons_layout.addWidget(self.btn_analizar)
        
        layout_der.addLayout(buttons_layout)
        
        splitter.addWidget(panel_der)
        
        # Proporción del splitter (30% lista, 70% detalles)
        splitter.setSizes([300, 700])
        
        layout.addWidget(splitter)
        
        # Cargar pacientes
        self.cargar_pacientes()
    
    def cargar_pacientes(self):
        """Carga la lista de pacientes activos"""
        self.combo_pacientes.clear()
        self.combo_pacientes.addItem("-- Seleccione un paciente --", None)
        
        pacientes = PacienteController.obtener_todos_pacientes(estado='activo')
        for paciente in pacientes:
            self.combo_pacientes.addItem(
                f"{paciente.apellido}, {paciente.nombre}",
                paciente.id
            )
    
    def cambiar_paciente(self, index):
        """Maneja el cambio de paciente seleccionado"""
        paciente_id = self.combo_pacientes.itemData(index)
        if paciente_id:
            self.paciente_actual = PacienteController.obtener_paciente(paciente_id)
            self.cargar_sesiones()
        else:
            self.paciente_actual = None
            self.lista_sesiones.clear()
            self.limpiar_detalles()
    
    def cargar_sesiones(self):
        """Carga las sesiones del paciente actual"""
        if not self.paciente_actual:
            return
        
        self.lista_sesiones.clear()
        sesiones = SesionController.obtener_sesiones_paciente(self.paciente_actual.id)
        
        for sesion in sesiones:
            item = QListWidgetItem()
            duracion_str = f" ({sesion.duracion} min)" if sesion.duracion else ""
            item.setText(f"📅 {sesion.fecha}{duracion_str}\n{sesion.notas[:50]}...")
            item.setData(Qt.ItemDataRole.UserRole, sesion.id)
            self.lista_sesiones.addItem(item)
        
        self.label_total.setText(f"Total de sesiones: {len(sesiones)}")
        
        if sesiones:
            self.lista_sesiones.setCurrentRow(0)
            self.seleccionar_sesion(self.lista_sesiones.item(0))
    
    def seleccionar_sesion(self, item):
        """Muestra los detalles de una sesión seleccionada"""
        if not item:
            return
        
        sesion_id = item.data(Qt.ItemDataRole.UserRole)
        self.sesion_actual = SesionController.obtener_sesion(sesion_id)
        
        if self.sesion_actual:
            self.mostrar_detalles_sesion()
            self.btn_editar.setEnabled(True)
            self.btn_eliminar.setEnabled(True)
            self.btn_analizar.setEnabled(True)
    
    def mostrar_detalles_sesion(self):
        """Muestra los detalles de la sesión actual"""
        if not self.sesion_actual:
            return
        
        duracion_str = f" - {self.sesion_actual.duracion} minutos" if self.sesion_actual.duracion else ""
        self.label_sesion_titulo.setText(f"Sesión #{self.sesion_actual.id}")
        self.label_sesion_fecha.setText(f"📅 {self.sesion_actual.fecha}{duracion_str}")
        
        self.txt_objetivos.setText(self.sesion_actual.objetivos or "")
        self.txt_notas.setText(self.sesion_actual.notas or "")
        self.txt_intervenciones.setText(self.sesion_actual.intervenciones or "")
        self.txt_observaciones.setText(self.sesion_actual.observaciones or "")
    
    def limpiar_detalles(self):
        """Limpia los campos de detalles"""
        self.label_sesion_titulo.setText("Seleccione una sesión")
        self.label_sesion_fecha.setText("")
        self.txt_objetivos.clear()
        self.txt_notas.clear()
        self.txt_intervenciones.clear()
        self.txt_observaciones.clear()
        self.btn_editar.setEnabled(False)
        self.btn_eliminar.setEnabled(False)
        self.btn_analizar.setEnabled(False)
    
    def nueva_sesion(self):
        """Abre el diálogo para crear una nueva sesión"""
        if not self.paciente_actual:
            QMessageBox.warning(self, "Advertencia", "Seleccione un paciente primero")
            return
        
        dialogo = SesionDialog(self, self.paciente_actual)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            sesion = dialogo.get_sesion()
            try:
                SesionController.crear_sesion(sesion)
                QMessageBox.information(self, "Éxito", "Sesión registrada correctamente")
                self.cargar_sesiones()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al crear sesión:\n{str(e)}")
    
    def editar_sesion(self):
        """Edita la sesión seleccionada"""
        if not self.sesion_actual:
            return
        
        dialogo = SesionDialog(self, self.paciente_actual, self.sesion_actual)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            sesion = dialogo.get_sesion()
            try:
                SesionController.actualizar_sesion(sesion)
                QMessageBox.information(self, "Éxito", "Sesión actualizada correctamente")
                self.cargar_sesiones()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar sesión:\n{str(e)}")
    
    def eliminar_sesion(self):
        """Elimina la sesión seleccionada"""
        if not self.sesion_actual:
            return
        
        respuesta = QMessageBox.question(
            self, "Confirmar", 
            f"¿Está seguro de eliminar esta sesión del {self.sesion_actual.fecha}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            try:
                SesionController.eliminar_sesion(self.sesion_actual.id)
                QMessageBox.information(self, "Éxito", "Sesión eliminada correctamente")
                self.cargar_sesiones()
                self.limpiar_detalles()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar sesión:\n{str(e)}")
    
    def buscar_sesiones(self, texto):
        """Busca en las sesiones del paciente actual"""
        if not self.paciente_actual or not texto.strip():
            self.cargar_sesiones()
            return
        
        self.lista_sesiones.clear()
        sesiones = SesionController.buscar_en_sesiones(self.paciente_actual.id, texto)
        
        for sesion in sesiones:
            item = QListWidgetItem()
            duracion_str = f" ({sesion.duracion} min)" if sesion.duracion else ""
            item.setText(f"📅 {sesion.fecha}{duracion_str}\n{sesion.notas[:50]}...")
            item.setData(Qt.ItemDataRole.UserRole, sesion.id)
            self.lista_sesiones.addItem(item)
        
        self.label_total.setText(f"Resultados: {len(sesiones)}")
    
    def analizar_con_ia(self):
        """Analiza la sesión con IA"""
        if not self.sesion_actual:
            return
        
        # Preparar texto de la sesión
        texto_sesion = f"{self.sesion_actual.objetivos} {self.sesion_actual.notas} {self.sesion_actual.intervenciones} {self.sesion_actual.observaciones}"
        
        # Realizar análisis
        analisis = ia_service.analizar_sesion(texto_sesion)
        
        # Mostrar resultados en un diálogo
        dialogo = QMessageBox(self)
        dialogo.setWindowTitle("Análisis con IA")
        dialogo.setIcon(QMessageBox.Icon.Information)
        
        resultado = f"""
🤖 ANÁLISIS DE SESIÓN

📅 Fecha: {self.sesion_actual.fecha}

😊 Sentimiento: {analisis.get('sentimiento', 'N/A').upper()}

🔑 Palabras Clave:
{', '.join(analisis.get('palabras_clave', []))}

📋 Temas Principales:
{', '.join(analisis.get('temas_principales', []))}

💡 Recomendaciones:
"""
        
        for rec in analisis.get('recomendaciones', []):
            resultado += f"\n  • {rec}"
        
        dialogo.setText(resultado)
        dialogo.setStyleSheet("QLabel { min-width: 400px; }")
        dialogo.exec()
    
    def showEvent(self, event):
        """Se ejecuta cuando la vista se muestra"""
        super().showEvent(event)
        self.cargar_pacientes()


class SesionDialog(QDialog):
    """Diálogo para crear/editar sesiones"""
    
    def __init__(self, parent=None, paciente=None, sesion=None):
        super().__init__(parent)
        self.paciente = paciente
        self.sesion = sesion
        
        titulo = "Editar Sesión" if sesion else "Nueva Sesión"
        self.setWindowTitle(titulo)
        self.setMinimumSize(700, 600)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del diálogo"""
        layout = QVBoxLayout(self)
        
        # Info del paciente
        if self.paciente:
            label_paciente = QLabel(f"Paciente: {self.paciente.nombre_completo}")
            label_paciente.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            layout.addWidget(label_paciente)
        
        form_layout = QFormLayout()
        
        # Fecha
        self.date_sesion = QDateEdit()
        self.date_sesion.setCalendarPopup(True)
        self.date_sesion.setDate(QDate.currentDate())
        form_layout.addRow("Fecha:", self.date_sesion)
        
        # Duración
        self.spin_duracion = QSpinBox()
        self.spin_duracion.setRange(15, 240)
        self.spin_duracion.setValue(50)
        self.spin_duracion.setSuffix(" min")
        form_layout.addRow("Duración:", self.spin_duracion)
        
        layout.addLayout(form_layout)
        
        # Objetivos
        layout.addWidget(QLabel("Objetivos de la Sesión:"))
        self.txt_objetivos = QTextEdit()
        self.txt_objetivos.setMaximumHeight(100)
        self.txt_objetivos.setPlaceholderText("Objetivos planteados para esta sesión...")
        layout.addWidget(self.txt_objetivos)
        
        # Notas
        layout.addWidget(QLabel("Notas de la Sesión:"))
        self.txt_notas = QTextEdit()
        self.txt_notas.setPlaceholderText("Desarrollo de la sesión, temas tratados, evolución del paciente...")
        layout.addWidget(self.txt_notas)
        
        # Intervenciones
        layout.addWidget(QLabel("Intervenciones Realizadas:"))
        self.txt_intervenciones = QTextEdit()
        self.txt_intervenciones.setMaximumHeight(100)
        self.txt_intervenciones.setPlaceholderText("Técnicas aplicadas, estrategias utilizadas...")
        layout.addWidget(self.txt_intervenciones)
        
        # Observaciones
        layout.addWidget(QLabel("Observaciones:"))
        self.txt_observaciones = QTextEdit()
        self.txt_observaciones.setMaximumHeight(80)
        self.txt_observaciones.setPlaceholderText("Observaciones adicionales, estado emocional...")
        layout.addWidget(self.txt_observaciones)
        
        # Próxima sesión
        self.txt_proxima = QLineEdit()
        self.txt_proxima.setPlaceholderText("Tareas para la próxima sesión...")
        form_layout2 = QFormLayout()
        form_layout2.addRow("Próxima Sesión:", self.txt_proxima)
        layout.addLayout(form_layout2)
        
        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Cargar datos si es edición
        if self.sesion:
            self.cargar_datos_sesion()
    
    def cargar_datos_sesion(self):
        """Carga los datos de la sesión en el formulario"""
        if self.sesion.fecha:
            fecha = QDate.fromString(str(self.sesion.fecha), "yyyy-MM-dd")
            self.date_sesion.setDate(fecha)
        
        if self.sesion.duracion:
            self.spin_duracion.setValue(self.sesion.duracion)
        
        self.txt_objetivos.setText(self.sesion.objetivos or "")
        self.txt_notas.setText(self.sesion.notas or "")
        self.txt_intervenciones.setText(self.sesion.intervenciones or "")
        self.txt_observaciones.setText(self.sesion.observaciones or "")
        self.txt_proxima.setText(self.sesion.proxima_sesion or "")
    
    def get_sesion(self):
        """Obtiene el objeto Sesion con los datos del formulario"""
        if self.sesion:
            sesion = self.sesion
        else:
            sesion = Sesion()
            sesion.paciente_id = self.paciente.id if self.paciente else None
        
        sesion.fecha = self.date_sesion.date().toString("yyyy-MM-dd")
        sesion.duracion = self.spin_duracion.value()
        sesion.objetivos = self.txt_objetivos.toPlainText().strip()
        sesion.notas = self.txt_notas.toPlainText().strip()
        sesion.intervenciones = self.txt_intervenciones.toPlainText().strip()
        sesion.observaciones = self.txt_observaciones.toPlainText().strip()
        sesion.proxima_sesion = self.txt_proxima.text().strip()
        
        return sesion
    
    def accept(self):
        """Valida los datos antes de aceptar"""
        if not self.txt_notas.toPlainText().strip():
            QMessageBox.warning(self, "Advertencia", "Las notas de la sesión son obligatorias")
            return
        
        super().accept()
