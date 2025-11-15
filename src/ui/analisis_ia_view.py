"""
Vista de Análisis con IA
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QTextEdit, QComboBox, QGroupBox, QListWidget, QProgressBar,
                             QMessageBox, QScrollArea, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from src.controllers.paciente_controller import PacienteController
from src.controllers.sesion_controller import SesionController
from src.services.ia_analysis_service import ia_service

class AnalisisIAView(QWidget):
    def __init__(self):
        super().__init__()
        self.paciente_actual = None
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Análisis con IA")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Selector de paciente
        self.combo_pacientes = QComboBox()
        self.combo_pacientes.setMinimumWidth(300)
        self.combo_pacientes.currentIndexChanged.connect(self.cambiar_paciente)
        header_layout.addWidget(QLabel("Paciente:"))
        header_layout.addWidget(self.combo_pacientes)
        
        # Botón analizar
        self.btn_analizar = QPushButton("🤖 Analizar Sesiones")
        self.btn_analizar.clicked.connect(self.analizar_sesiones)
        self.btn_analizar.setEnabled(False)
        self.btn_analizar.setStyleSheet("background-color: #9b59b6; font-size: 14px; padding: 10px;")
        header_layout.addWidget(self.btn_analizar)
        
        layout.addLayout(header_layout)
        
        # Estado del servicio
        if not ia_service.available:
            warning = QLabel("⚠️ API de OpenAI no configurada. Usando análisis básico local.")
            warning.setStyleSheet("background-color: #f39c12; color: white; padding: 10px; border-radius: 5px;")
            layout.addWidget(warning)
        else:
            info = QLabel("✅ Servicio de IA configurado correctamente")
            info.setStyleSheet("background-color: #27ae60; color: white; padding: 10px; border-radius: 5px;")
            layout.addWidget(info)
        
        # Área de scroll para resultados
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; }")
        
        # Widget contenedor de resultados
        self.resultados_widget = QWidget()
        self.resultados_layout = QVBoxLayout(self.resultados_widget)
        self.resultados_layout.setSpacing(15)
        
        scroll.setWidget(self.resultados_widget)
        layout.addWidget(scroll)
        
        # Cargar pacientes
        self.cargar_pacientes()
        
        # Mostrar mensaje inicial
        self.mostrar_mensaje_inicial()
    
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
            self.btn_analizar.setEnabled(True)
            self.limpiar_resultados()
        else:
            self.paciente_actual = None
            self.btn_analizar.setEnabled(False)
            self.mostrar_mensaje_inicial()
    
    def mostrar_mensaje_inicial(self):
        """Muestra mensaje inicial"""
        self.limpiar_resultados()
        
        label = QLabel("👆 Seleccione un paciente y presione 'Analizar Sesiones' para comenzar")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #7f8c8d; font-size: 16px; padding: 50px;")
        self.resultados_layout.addWidget(label)
    
    def limpiar_resultados(self):
        """Limpia los resultados anteriores"""
        while self.resultados_layout.count():
            child = self.resultados_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def analizar_sesiones(self):
        """Analiza las sesiones del paciente con IA"""
        if not self.paciente_actual:
            return
        
        # Obtener sesiones del paciente
        sesiones = SesionController.obtener_sesiones_paciente(self.paciente_actual.id)
        
        if not sesiones:
            QMessageBox.warning(self, "Sin datos", 
                              "Este paciente no tiene sesiones registradas para analizar")
            return
        
        # Deshabilitar botón durante análisis
        self.btn_analizar.setEnabled(False)
        self.btn_analizar.setText("⏳ Analizando...")
        
        # Limpiar resultados anteriores
        self.limpiar_resultados()
        
        # Preparar textos de sesiones
        textos_sesiones = []
        for sesion in sesiones:
            texto_completo = f"{sesion.objetivos} {sesion.notas} {sesion.intervenciones} {sesion.observaciones}"
            textos_sesiones.append(texto_completo)
        
        # Realizar análisis
        try:
            # Análisis de patrones generales
            analisis_general = ia_service.analizar_multiples_sesiones(textos_sesiones)
            self.mostrar_analisis_general(analisis_general, len(sesiones))
            
            # Análisis de última sesión
            if sesiones:
                ultima_sesion = sesiones[0]  # Ya vienen ordenadas por fecha DESC
                texto_ultima = f"{ultima_sesion.objetivos} {ultima_sesion.notas} {ultima_sesion.intervenciones}"
                analisis_ultima = ia_service.analizar_sesion(texto_ultima)
                self.mostrar_analisis_sesion(analisis_ultima, ultima_sesion.fecha)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error durante el análisis:\n{str(e)}")
        
        # Rehabilitar botón
        self.btn_analizar.setEnabled(True)
        self.btn_analizar.setText("🤖 Analizar Sesiones")
    
    def mostrar_analisis_general(self, analisis: dict, total_sesiones: int):
        """Muestra el análisis general de todas las sesiones"""
        # Tarjeta de resumen
        card = self.crear_tarjeta("📊 Análisis General de Sesiones")
        card_layout = card.layout()
        
        # Total de sesiones
        label_total = QLabel(f"Total de sesiones analizadas: {total_sesiones}")
        label_total.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        card_layout.addWidget(label_total)
        
        # Tendencia
        tendencia = analisis.get('tendencia', 'desconocida')
        emoji_tendencia = "📈" if tendencia == "mejorando" else "📉" if tendencia == "empeorando" else "➡️"
        label_tendencia = QLabel(f"{emoji_tendencia} Tendencia: {tendencia.upper()}")
        label_tendencia.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        
        if tendencia == "mejorando":
            label_tendencia.setStyleSheet("color: #27ae60;")
        elif tendencia == "empeorando":
            label_tendencia.setStyleSheet("color: #e74c3c;")
        else:
            label_tendencia.setStyleSheet("color: #f39c12;")
        
        card_layout.addWidget(label_tendencia)
        
        self.resultados_layout.addWidget(card)
        
        # Palabras recurrentes
        if 'palabras_recurrentes' in analisis:
            card_palabras = self.crear_tarjeta("🔑 Palabras Clave Recurrentes")
            card_palabras_layout = card_palabras.layout()
            
            palabras_text = ", ".join(analisis['palabras_recurrentes'][:15])
            label_palabras = QLabel(palabras_text)
            label_palabras.setWordWrap(True)
            label_palabras.setStyleSheet("font-size: 13px; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
            card_palabras_layout.addWidget(label_palabras)
            
            self.resultados_layout.addWidget(card_palabras)
        
        # Insights
        if 'insights' in analisis and analisis['insights']:
            card_insights = self.crear_tarjeta("💡 Insights Detectados")
            card_insights_layout = card_insights.layout()
            
            for insight in analisis['insights']:
                label_insight = QLabel(f"• {insight}")
                label_insight.setWordWrap(True)
                label_insight.setStyleSheet("font-size: 13px; padding: 5px;")
                card_insights_layout.addWidget(label_insight)
            
            self.resultados_layout.addWidget(card_insights)
        
        # Evolución de sentimiento
        if 'evolucion_sentimiento' in analisis:
            card_evolucion = self.crear_tarjeta("📈 Evolución del Sentimiento")
            card_evolucion_layout = card_evolucion.layout()
            
            sentimientos = analisis['evolucion_sentimiento']
            texto_evolucion = " → ".join([s.upper() for s in sentimientos[-10:]])  # Últimas 10 sesiones
            label_evolucion = QLabel(texto_evolucion)
            label_evolucion.setWordWrap(True)
            label_evolucion.setStyleSheet("font-size: 12px; padding: 10px;")
            card_evolucion_layout.addWidget(label_evolucion)
            
            self.resultados_layout.addWidget(card_evolucion)
    
    def mostrar_analisis_sesion(self, analisis: dict, fecha: str):
        """Muestra el análisis de una sesión específica"""
        card = self.crear_tarjeta(f"📝 Análisis de Última Sesión ({fecha})")
        card_layout = card.layout()
        
        # Sentimiento
        sentimiento = analisis.get('sentimiento', 'neutral')
        emoji_sent = "😊" if sentimiento == "positivo" else "😔" if sentimiento == "negativo" else "😐"
        label_sent = QLabel(f"{emoji_sent} Sentimiento: {sentimiento.upper()}")
        label_sent.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        card_layout.addWidget(label_sent)
        
        # Palabras clave
        if 'palabras_clave' in analisis:
            label_pk = QLabel(f"Palabras clave: {', '.join(analisis['palabras_clave'])}")
            label_pk.setWordWrap(True)
            label_pk.setStyleSheet("font-size: 12px; padding: 5px;")
            card_layout.addWidget(label_pk)
        
        # Temas principales
        if 'temas_principales' in analisis:
            temas = ', '.join(analisis['temas_principales'])
            label_temas = QLabel(f"Temas: {temas}")
            label_temas.setStyleSheet("font-size: 12px; padding: 5px; color: #7f8c8d;")
            card_layout.addWidget(label_temas)
        
        # Recomendaciones
        if 'recomendaciones' in analisis and analisis['recomendaciones']:
            label_rec_titulo = QLabel("Recomendaciones:")
            label_rec_titulo.setFont(QFont("Arial", 12, QFont.Weight.Bold))
            card_layout.addWidget(label_rec_titulo)
            
            for rec in analisis['recomendaciones']:
                label_rec = QLabel(f"  ✓ {rec}")
                label_rec.setWordWrap(True)
                label_rec.setStyleSheet("font-size: 12px; padding: 3px;")
                card_layout.addWidget(label_rec)
        
        self.resultados_layout.addWidget(card)
    
    def crear_tarjeta(self, titulo: str) -> QGroupBox:
        """Crea una tarjeta con estilo para mostrar resultados"""
        card = QGroupBox(titulo)
        card.setStyleSheet("""
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #3498db;
            }
        """)
        layout = QVBoxLayout()
        layout.setSpacing(8)
        card.setLayout(layout)
        return card
    
    def showEvent(self, event):
        """Se ejecuta cuando la vista se muestra"""
        super().showEvent(event)
        self.cargar_pacientes()
