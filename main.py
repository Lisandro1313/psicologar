"""
PsicolaRG - Sistema de Gestión para Psicólogos
Aplicación de escritorio para gestión de pacientes, sesiones y análisis con IA
"""
import sys
from PyQt6.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("PsicolaRG")
    app.setOrganizationName("PsicolaRG")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
