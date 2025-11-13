"""
Gestor de base de datos SQLite con cifrado
"""
import sqlite3
import os
from pathlib import Path
from cryptography.fernet import Fernet
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="data/psicolarg.db"):
        self.db_path = db_path
        self._ensure_db_directory()
        self.connection = None
        self.cursor = None
        
    def _ensure_db_directory(self):
        """Crea el directorio de datos si no existe"""
        db_dir = Path(self.db_path).parent
        db_dir.mkdir(parents=True, exist_ok=True)
    
    def connect(self):
        """Establece conexión con la base de datos"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._create_tables()
        
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
    
    def _create_tables(self):
        """Crea las tablas de la base de datos"""
        
        # Tabla de pacientes
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS pacientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                apellido TEXT NOT NULL,
                dni TEXT UNIQUE,
                fecha_nacimiento DATE,
                telefono TEXT,
                email TEXT,
                direccion TEXT,
                obra_social TEXT,
                numero_afiliado TEXT,
                motivo_consulta TEXT,
                derivado_por TEXT,
                fecha_alta DATE DEFAULT CURRENT_DATE,
                estado TEXT DEFAULT 'activo',
                notas TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de turnos
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS turnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                hora_inicio TIME NOT NULL,
                hora_fin TIME,
                estado TEXT DEFAULT 'programado',
                tipo TEXT DEFAULT 'sesion',
                notas TEXT,
                recordatorio_enviado INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de sesiones
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS sesiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                turno_id INTEGER,
                fecha DATE NOT NULL,
                duracion INTEGER,
                notas TEXT,
                objetivos TEXT,
                intervenciones TEXT,
                observaciones TEXT,
                proxima_sesion TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
                FOREIGN KEY (turno_id) REFERENCES turnos (id) ON DELETE SET NULL
            )
        ''')
        
        # Tabla de análisis de IA
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS analisis_ia (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paciente_id INTEGER NOT NULL,
                sesion_id INTEGER,
                tipo_analisis TEXT,
                palabras_clave TEXT,
                patrones_detectados TEXT,
                sentimiento TEXT,
                recomendaciones TEXT,
                fecha_analisis TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE,
                FOREIGN KEY (sesion_id) REFERENCES sesiones (id) ON DELETE CASCADE
            )
        ''')
        
        # Tabla de configuración
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY,
                valor TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.connection.commit()
    
    def execute_query(self, query, params=None):
        """Ejecuta una consulta SQL"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.connection.commit()
        return self.cursor
    
    def fetch_all(self, query, params=None):
        """Ejecuta una consulta y devuelve todos los resultados"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def fetch_one(self, query, params=None):
        """Ejecuta una consulta y devuelve un resultado"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchone()

# Instancia global del gestor de base de datos
db = DatabaseManager()
