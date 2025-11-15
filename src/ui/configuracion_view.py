"""
Vista de Configuración y Seguridad
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QGroupBox, QLineEdit, QMessageBox, QFileDialog, QListWidget,
                             QListWidgetItem, QDialog, QFormLayout, QDialogButtonBox,
                             QCheckBox, QSpinBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from src.services.security_service import security_service
from src.services.backup_service import backup_service

class ConfiguracionView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Título
        title = QLabel("⚙️ Configuración y Seguridad")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Sección: Seguridad
        grupo_seguridad = self.crear_grupo_seguridad()
        layout.addWidget(grupo_seguridad)
        
        # Sección: Backups
        grupo_backup = self.crear_grupo_backup()
        layout.addWidget(grupo_backup)
        
        # Sección: Información
        grupo_info = self.crear_grupo_info()
        layout.addWidget(grupo_info)
        
        layout.addStretch()
    
    def crear_grupo_seguridad(self) -> QGroupBox:
        """Crea el grupo de configuración de seguridad"""
        grupo = QGroupBox("🔒 Seguridad")
        grupo.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Info de seguridad
        if security_service.password_configurado():
            label_status = QLabel("✅ Contraseña maestra configurada")
            label_status.setStyleSheet("color: #27ae60; font-weight: bold;")
        else:
            label_status = QLabel("⚠️ Contraseña maestra no configurada")
            label_status.setStyleSheet("color: #e74c3c; font-weight: bold;")
        
        layout.addWidget(label_status)
        
        # Botón cambiar contraseña
        btn_cambiar_pass = QPushButton("🔑 Cambiar Contraseña")
        btn_cambiar_pass.clicked.connect(self.cambiar_password)
        btn_cambiar_pass.setMaximumWidth(200)
        layout.addWidget(btn_cambiar_pass)
        
        # Info adicional
        info = QLabel(
            "La contraseña maestra protege el acceso a todos los datos de la aplicación.\n"
            "Se recomienda usar una contraseña segura y guardarla en un lugar seguro."
        )
        info.setWordWrap(True)
        info.setStyleSheet("color: #7f8c8d; font-size: 12px; padding: 10px;")
        layout.addWidget(info)
        
        grupo.setLayout(layout)
        return grupo
    
    def crear_grupo_backup(self) -> QGroupBox:
        """Crea el grupo de configuración de backups"""
        grupo = QGroupBox("💾 Copias de Seguridad")
        grupo.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #27ae60;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        
        btn_crear_backup = QPushButton("💾 Crear Backup")
        btn_crear_backup.clicked.connect(self.crear_backup)
        btn_crear_backup.setStyleSheet("background-color: #27ae60;")
        buttons_layout.addWidget(btn_crear_backup)
        
        btn_restaurar = QPushButton("📥 Restaurar Backup")
        btn_restaurar.clicked.connect(self.restaurar_backup)
        btn_restaurar.setStyleSheet("background-color: #f39c12;")
        buttons_layout.addWidget(btn_restaurar)
        
        btn_gestionar = QPushButton("📋 Gestionar Backups")
        btn_gestionar.clicked.connect(self.gestionar_backups)
        buttons_layout.addWidget(btn_gestionar)
        
        layout.addLayout(buttons_layout)
        
        # Info
        backups_disponibles = len(backup_service.listar_backups())
        label_info = QLabel(f"Backups disponibles: {backups_disponibles}")
        label_info.setStyleSheet("color: #7f8c8d; padding: 10px;")
        layout.addWidget(label_info)
        
        # Recomendación
        recomendacion = QLabel(
            "💡 Recomendación: Realice backups periódicos de su base de datos.\n"
            "Guarde las copias en un lugar seguro (disco externo, nube cifrada)."
        )
        recomendacion.setWordWrap(True)
        recomendacion.setStyleSheet("color: #7f8c8d; font-size: 12px; padding: 10px; background-color: #ecf0f1; border-radius: 5px;")
        layout.addWidget(recomendacion)
        
        grupo.setLayout(layout)
        return grupo
    
    def crear_grupo_info(self) -> QGroupBox:
        """Crea el grupo de información de la aplicación"""
        grupo = QGroupBox("ℹ️ Información")
        grupo.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #95a5a6;
                border-radius: 8px;
                margin-top: 10px;
                padding: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        layout = QVBoxLayout()
        
        info_text = """
<b>PsicolaRG</b> - Sistema de Gestión para Psicólogos<br>
<b>Versión:</b> 1.0.0<br>
<b>Desarrollado con:</b> Python + PyQt6<br><br>

<b>Características de Seguridad:</b><br>
• Autenticación con contraseña maestra<br>
• Cifrado de datos sensibles<br>
• Base de datos local SQLite<br>
• Sistema de backups<br>
• Sin conexión a internet (datos seguros)<br><br>

<b>Cumplimiento:</b><br>
Esta aplicación está diseñada para cumplir con las normativas de<br>
protección de datos personales y secreto profesional.
        """
        
        label_info = QLabel(info_text)
        label_info.setWordWrap(True)
        label_info.setTextFormat(Qt.TextFormat.RichText)
        label_info.setStyleSheet("color: #2c3e50; padding: 10px;")
        layout.addWidget(label_info)
        
        grupo.setLayout(layout)
        return grupo
    
    def cambiar_password(self):
        """Abre el diálogo para cambiar la contraseña"""
        dialogo = CambiarPasswordDialog(self)
        dialogo.exec()
    
    def crear_backup(self):
        """Crea un backup de la base de datos"""
        respuesta = QMessageBox.question(
            self, "Crear Backup",
            "¿Desea crear una copia de seguridad de la base de datos?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            exito, mensaje, ruta = backup_service.crear_backup()
            
            if exito:
                QMessageBox.information(
                    self, "Backup Creado",
                    f"{mensaje}\n\nUbicación:\n{ruta}\n\n"
                    "Guarde este archivo en un lugar seguro."
                )
            else:
                QMessageBox.critical(self, "Error", mensaje)
    
    def restaurar_backup(self):
        """Restaura un backup de la base de datos"""
        # Advertencia
        respuesta = QMessageBox.warning(
            self, "⚠️ Advertencia",
            "Restaurar un backup reemplazará todos los datos actuales.\n\n"
            "Se creará un backup automático de la base de datos actual antes de continuar.\n\n"
            "¿Desea continuar?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta != QMessageBox.StandardButton.Yes:
            return
        
        # Seleccionar archivo
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Backup",
            str(backup_service.backup_dir),
            "Archivos de backup (*.zip *.db)"
        )
        
        if archivo:
            exito, mensaje = backup_service.restaurar_backup(archivo)
            
            if exito:
                QMessageBox.information(
                    self, "Éxito",
                    f"{mensaje}\n\nLa aplicación se reiniciará."
                )
                # Aquí se debería reiniciar la aplicación
            else:
                QMessageBox.critical(self, "Error", mensaje)
    
    def gestionar_backups(self):
        """Abre el gestor de backups"""
        dialogo = GestionarBackupsDialog(self)
        dialogo.exec()


class CambiarPasswordDialog(QDialog):
    """Diálogo para cambiar la contraseña"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cambiar Contraseña")
        self.setMinimumWidth(400)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        # Contraseña actual
        self.txt_actual = QLineEdit()
        self.txt_actual.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Contraseña actual:", self.txt_actual)
        
        # Nueva contraseña
        self.txt_nueva = QLineEdit()
        self.txt_nueva.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Nueva contraseña:", self.txt_nueva)
        
        # Confirmar
        self.txt_confirmar = QLineEdit()
        self.txt_confirmar.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Confirmar nueva:", self.txt_confirmar)
        
        layout.addLayout(form_layout)
        
        # Checkbox mostrar
        self.check_mostrar = QCheckBox("Mostrar contraseñas")
        self.check_mostrar.stateChanged.connect(self.toggle_visibility)
        layout.addWidget(self.check_mostrar)
        
        # Botones
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.cambiar)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def toggle_visibility(self, state):
        """Muestra u oculta las contraseñas"""
        modo = QLineEdit.EchoMode.Normal if state else QLineEdit.EchoMode.Password
        self.txt_actual.setEchoMode(modo)
        self.txt_nueva.setEchoMode(modo)
        self.txt_confirmar.setEchoMode(modo)
    
    def cambiar(self):
        """Cambia la contraseña"""
        actual = self.txt_actual.text()
        nueva = self.txt_nueva.text()
        confirmar = self.txt_confirmar.text()
        
        if not actual or not nueva or not confirmar:
            QMessageBox.warning(self, "Error", "Complete todos los campos")
            return
        
        if nueva != confirmar:
            QMessageBox.warning(self, "Error", "Las contraseñas nuevas no coinciden")
            return
        
        exito, mensaje = security_service.cambiar_password(actual, nueva)
        
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.accept()
        else:
            QMessageBox.critical(self, "Error", mensaje)


class GestionarBackupsDialog(QDialog):
    """Diálogo para gestionar backups"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gestionar Backups")
        self.setMinimumSize(600, 400)
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz"""
        layout = QVBoxLayout(self)
        
        # Lista de backups
        self.lista_backups = QListWidget()
        layout.addWidget(self.lista_backups)
        
        # Botones
        buttons_layout = QHBoxLayout()
        
        btn_actualizar = QPushButton("🔄 Actualizar")
        btn_actualizar.clicked.connect(self.cargar_backups)
        buttons_layout.addWidget(btn_actualizar)
        
        buttons_layout.addStretch()
        
        btn_abrir = QPushButton("📂 Abrir Carpeta")
        btn_abrir.clicked.connect(self.abrir_carpeta)
        buttons_layout.addWidget(btn_abrir)
        
        btn_eliminar = QPushButton("🗑 Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_backup)
        btn_eliminar.setStyleSheet("background-color: #e74c3c;")
        buttons_layout.addWidget(btn_eliminar)
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        buttons_layout.addWidget(btn_cerrar)
        
        layout.addLayout(buttons_layout)
        
        # Cargar backups
        self.cargar_backups()
    
    def cargar_backups(self):
        """Carga la lista de backups"""
        self.lista_backups.clear()
        backups = backup_service.listar_backups()
        
        if not backups:
            item = QListWidgetItem("No hay backups disponibles")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.lista_backups.addItem(item)
        else:
            for backup in backups:
                texto = f"{backup['nombre']}\n📅 {backup['fecha'].strftime('%d/%m/%Y %H:%M')} - 💾 {backup['tamaño']}"
                item = QListWidgetItem(texto)
                item.setData(Qt.ItemDataRole.UserRole, backup['ruta'])
                self.lista_backups.addItem(item)
    
    def abrir_carpeta(self):
        """Abre la carpeta de backups"""
        import os
        import subprocess
        
        ruta = str(backup_service.backup_dir.absolute())
        
        if os.name == 'nt':  # Windows
            os.startfile(ruta)
        elif os.name == 'posix':  # Linux/Mac
            subprocess.call(['xdg-open', ruta])
    
    def eliminar_backup(self):
        """Elimina el backup seleccionado"""
        item = self.lista_backups.currentItem()
        if not item or not item.data(Qt.ItemDataRole.UserRole):
            QMessageBox.warning(self, "Advertencia", "Seleccione un backup")
            return
        
        respuesta = QMessageBox.question(
            self, "Confirmar",
            "¿Está seguro de eliminar este backup?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if respuesta == QMessageBox.StandardButton.Yes:
            ruta = item.data(Qt.ItemDataRole.UserRole)
            exito, mensaje = backup_service.eliminar_backup(ruta)
            
            if exito:
                QMessageBox.information(self, "Éxito", mensaje)
                self.cargar_backups()
            else:
                QMessageBox.critical(self, "Error", mensaje)
