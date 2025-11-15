"""
Diálogo de Login/Autenticación
"""
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from src.services.security_service import security_service

class LoginDialog(QDialog):
    """Diálogo de autenticación"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PsicolaRG - Inicio de Sesión")
        self.setFixedSize(400, 300)
        self.setModal(True)
        self.autenticado = False
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo/Título
        title = QLabel("🔒 PsicolaRG")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3498db;")
        layout.addWidget(title)
        
        subtitle = QLabel("Sistema de Gestión para Psicólogos")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        layout.addWidget(subtitle)
        
        layout.addSpacing(20)
        
        # Campo de contraseña
        label_pass = QLabel("Contraseña:")
        label_pass.setStyleSheet("font-weight: bold;")
        layout.addWidget(label_pass)
        
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setPlaceholderText("Ingrese su contraseña")
        self.txt_password.setMinimumHeight(35)
        self.txt_password.returnPressed.connect(self.autenticar)
        layout.addWidget(self.txt_password)
        
        # Checkbox mostrar contraseña
        self.check_mostrar = QCheckBox("Mostrar contraseña")
        self.check_mostrar.stateChanged.connect(self.toggle_password_visibility)
        layout.addWidget(self.check_mostrar)
        
        layout.addStretch()
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_cancelar.setStyleSheet("background-color: #95a5a6;")
        buttons_layout.addWidget(btn_cancelar)
        
        btn_ingresar = QPushButton("Ingresar")
        btn_ingresar.clicked.connect(self.autenticar)
        btn_ingresar.setDefault(True)
        btn_ingresar.setMinimumHeight(35)
        buttons_layout.addWidget(btn_ingresar)
        
        layout.addLayout(buttons_layout)
        
        # Aplicar estilos
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # Enfocar el campo de contraseña
        self.txt_password.setFocus()
    
    def toggle_password_visibility(self, state):
        """Muestra u oculta la contraseña"""
        if state:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
    
    def autenticar(self):
        """Intenta autenticar al usuario"""
        password = self.txt_password.text()
        
        if not password:
            QMessageBox.warning(self, "Error", "Ingrese una contraseña")
            return
        
        if security_service.autenticar(password):
            self.autenticado = True
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Contraseña incorrecta")
            self.txt_password.clear()
            self.txt_password.setFocus()


class ConfigurarPasswordDialog(QDialog):
    """Diálogo para configurar la contraseña por primera vez"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configurar Contraseña Maestra")
        self.setFixedSize(450, 400)
        self.setModal(True)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Título
        title = QLabel("🔐 Configuración Inicial")
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #3498db;")
        layout.addWidget(title)
        
        # Mensaje informativo
        info = QLabel(
            "Configure una contraseña maestra para proteger los datos de sus pacientes.\n\n"
            "Requisitos:\n"
            "• Mínimo 8 caracteres\n"
            "• Mayúsculas y minúsculas\n"
            "• Números\n"
            "• Caracteres especiales"
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #7f8c8d; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        layout.addWidget(info)
        
        # Advertencia
        warning = QLabel("⚠️ IMPORTANTE: No olvide esta contraseña. No hay forma de recuperarla.")
        warning.setWordWrap(True)
        warning.setStyleSheet("color: #e74c3c; font-weight: bold; padding: 10px;")
        layout.addWidget(warning)
        
        # Campos
        layout.addWidget(QLabel("Nueva contraseña:"))
        self.txt_password = QLineEdit()
        self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_password.setMinimumHeight(35)
        layout.addWidget(self.txt_password)
        
        layout.addWidget(QLabel("Confirmar contraseña:"))
        self.txt_confirm = QLineEdit()
        self.txt_confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.txt_confirm.setMinimumHeight(35)
        layout.addWidget(self.txt_confirm)
        
        # Checkbox mostrar contraseña
        self.check_mostrar = QCheckBox("Mostrar contraseñas")
        self.check_mostrar.stateChanged.connect(self.toggle_password_visibility)
        layout.addWidget(self.check_mostrar)
        
        layout.addStretch()
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_cancelar.setStyleSheet("background-color: #95a5a6;")
        buttons_layout.addWidget(btn_cancelar)
        
        btn_guardar = QPushButton("Guardar")
        btn_guardar.clicked.connect(self.guardar_password)
        btn_guardar.setDefault(True)
        btn_guardar.setMinimumHeight(35)
        buttons_layout.addWidget(btn_guardar)
        
        layout.addLayout(buttons_layout)
        
        # Estilos
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 8px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
    
    def toggle_password_visibility(self, state):
        """Muestra u oculta las contraseñas"""
        if state:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.txt_confirm.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.txt_password.setEchoMode(QLineEdit.EchoMode.Password)
            self.txt_confirm.setEchoMode(QLineEdit.EchoMode.Password)
    
    def guardar_password(self):
        """Guarda la contraseña configurada"""
        password = self.txt_password.text()
        confirm = self.txt_confirm.text()
        
        if not password or not confirm:
            QMessageBox.warning(self, "Error", "Complete todos los campos")
            return
        
        if password != confirm:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden")
            return
        
        # Validar fortaleza
        valida, mensaje = security_service.validar_fortaleza_password(password)
        if not valida:
            QMessageBox.warning(self, "Contraseña débil", mensaje)
            return
        
        # Configurar contraseña
        security_service.configurar_password(password)
        
        QMessageBox.information(
            self, "Éxito",
            "Contraseña configurada exitosamente.\n\n"
            "Por favor, guárdela en un lugar seguro."
        )
        
        self.accept()
