"""
Controlador de Sesiones
Maneja la lógica de negocio para la gestión de sesiones
"""
from src.database.db_manager import db
from src.models.sesion import Sesion
from datetime import datetime

class SesionController:
    
    @staticmethod
    def crear_sesion(sesion):
        """Crea una nueva sesión en la base de datos"""
        query = '''
            INSERT INTO sesiones (paciente_id, turno_id, fecha, duracion, notas, 
                                objetivos, intervenciones, observaciones, proxima_sesion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            sesion.paciente_id, sesion.turno_id, sesion.fecha, sesion.duracion,
            sesion.notas, sesion.objetivos, sesion.intervenciones, 
            sesion.observaciones, sesion.proxima_sesion
        )
        cursor = db.execute_query(query, params)
        sesion.id = cursor.lastrowid
        return sesion
    
    @staticmethod
    def obtener_sesion(sesion_id):
        """Obtiene una sesión por su ID"""
        query = 'SELECT * FROM sesiones WHERE id = ?'
        row = db.fetch_one(query, (sesion_id,))
        return Sesion.from_db_row(row)
    
    @staticmethod
    def obtener_sesiones_paciente(paciente_id):
        """Obtiene todas las sesiones de un paciente ordenadas por fecha"""
        query = '''
            SELECT * FROM sesiones 
            WHERE paciente_id = ? 
            ORDER BY fecha DESC
        '''
        rows = db.fetch_all(query, (paciente_id,))
        return [Sesion.from_db_row(row) for row in rows]
    
    @staticmethod
    def obtener_ultima_sesion(paciente_id):
        """Obtiene la última sesión de un paciente"""
        query = '''
            SELECT * FROM sesiones 
            WHERE paciente_id = ? 
            ORDER BY fecha DESC, id DESC
            LIMIT 1
        '''
        row = db.fetch_one(query, (paciente_id,))
        return Sesion.from_db_row(row)
    
    @staticmethod
    def actualizar_sesion(sesion):
        """Actualiza los datos de una sesión"""
        query = '''
            UPDATE sesiones 
            SET turno_id = ?, fecha = ?, duracion = ?, notas = ?,
                objetivos = ?, intervenciones = ?, observaciones = ?, 
                proxima_sesion = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        params = (
            sesion.turno_id, sesion.fecha, sesion.duracion, sesion.notas,
            sesion.objetivos, sesion.intervenciones, sesion.observaciones,
            sesion.proxima_sesion, sesion.id
        )
        db.execute_query(query, params)
        return sesion
    
    @staticmethod
    def eliminar_sesion(sesion_id):
        """Elimina una sesión"""
        query = 'DELETE FROM sesiones WHERE id = ?'
        db.execute_query(query, (sesion_id,))
    
    @staticmethod
    def contar_sesiones_paciente(paciente_id):
        """Cuenta el número de sesiones de un paciente"""
        query = 'SELECT COUNT(*) as total FROM sesiones WHERE paciente_id = ?'
        row = db.fetch_one(query, (paciente_id,))
        return row['total'] if row else 0
    
    @staticmethod
    def buscar_en_sesiones(paciente_id, termino):
        """Busca un término en las notas de sesiones de un paciente"""
        query = '''
            SELECT * FROM sesiones 
            WHERE paciente_id = ? AND (
                notas LIKE ? OR 
                objetivos LIKE ? OR 
                intervenciones LIKE ? OR 
                observaciones LIKE ?
            )
            ORDER BY fecha DESC
        '''
        termino_busqueda = f'%{termino}%'
        rows = db.fetch_all(query, (paciente_id, termino_busqueda, termino_busqueda, 
                                    termino_busqueda, termino_busqueda))
        return [Sesion.from_db_row(row) for row in rows]
