"""
PsicolaRG - Sistema de Gestión para Psicólogos
Aplicación de escritorio para gestión de pacientes, sesiones y análisis con IA
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow
from src.ui.login_dialog import LoginDialog, ConfigurarPasswordDialog
from src.services.security_service import security_service

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PsicolaRG")
    app.setOrganizationName("PsicolaRG")
    
    # Inicializar seguridad
    security_service.inicializar_seguridad()
    
    # Verificar si hay contraseña configurada
    if not security_service.password_configurado():
        # Primera vez: configurar contraseña
        dialogo_config = ConfigurarPasswordDialog()
        if dialogo_config.exec() != 1:  # Usuario canceló
            return 0
    
    # Mostrar login
    dialogo_login = LoginDialog()
    if dialogo_login.exec() != 1 or not dialogo_login.autenticado:
        return 0
    
    # Usuario autenticado correctamente
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
