"""
Controlador de Turnos
Maneja la lógica de negocio para la gestión de turnos
"""
from src.database.db_manager import db
from src.models.turno import Turno
from datetime import datetime, date

class TurnoController:
    
    @staticmethod
    def crear_turno(turno):
        """Crea un nuevo turno en la base de datos"""
        query = '''
            INSERT INTO turnos (paciente_id, fecha, hora_inicio, hora_fin, 
                              estado, tipo, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            turno.paciente_id, turno.fecha, turno.hora_inicio, turno.hora_fin,
            turno.estado, turno.tipo, turno.notas
        )
        cursor = db.execute_query(query, params)
        turno.id = cursor.lastrowid
        return turno
    
    @staticmethod
    def obtener_turno(turno_id):
        """Obtiene un turno por su ID"""
        query = 'SELECT * FROM turnos WHERE id = ?'
        row = db.fetch_one(query, (turno_id,))
        return Turno.from_db_row(row)
    
    @staticmethod
    def obtener_turnos_fecha(fecha):
        """Obtiene todos los turnos de una fecha específica"""
        query = '''
            SELECT t.*, p.nombre, p.apellido 
            FROM turnos t
            JOIN pacientes p ON t.paciente_id = p.id
            WHERE t.fecha = ?
            ORDER BY t.hora_inicio
        '''
        rows = db.fetch_all(query, (fecha,))
        return rows
    
    @staticmethod
    def obtener_turnos_paciente(paciente_id):
        """Obtiene todos los turnos de un paciente"""
        query = '''
            SELECT * FROM turnos 
            WHERE paciente_id = ? 
            ORDER BY fecha DESC, hora_inicio DESC
        '''
        rows = db.fetch_all(query, (paciente_id,))
        return [Turno.from_db_row(row) for row in rows]
    
    @staticmethod
    def obtener_turnos_hoy():
        """Obtiene los turnos de hoy"""
        hoy = date.today().isoformat()
        return TurnoController.obtener_turnos_fecha(hoy)
    
    @staticmethod
    def obtener_proximos_turnos(dias=7):
        """Obtiene los próximos turnos en los siguientes días"""
        query = '''
            SELECT t.*, p.nombre, p.apellido 
            FROM turnos t
            JOIN pacientes p ON t.paciente_id = p.id
            WHERE t.fecha >= date('now') AND t.fecha <= date('now', '+' || ? || ' days')
            AND t.estado = 'programado'
            ORDER BY t.fecha, t.hora_inicio
        '''
        rows = db.fetch_all(query, (dias,))
        return rows
    
    @staticmethod
    def actualizar_turno(turno):
        """Actualiza los datos de un turno"""
        query = '''
            UPDATE turnos 
            SET paciente_id = ?, fecha = ?, hora_inicio = ?, hora_fin = ?,
                estado = ?, tipo = ?, notas = ?
            WHERE id = ?
        '''
        params = (
            turno.paciente_id, turno.fecha, turno.hora_inicio, turno.hora_fin,
            turno.estado, turno.tipo, turno.notas, turno.id
        )
        db.execute_query(query, params)
        return turno
    
    @staticmethod
    def eliminar_turno(turno_id):
        """Elimina un turno"""
        query = 'DELETE FROM turnos WHERE id = ?'
        db.execute_query(query, (turno_id,))
    
    @staticmethod
    def contar_turnos_hoy():
        """Cuenta los turnos de hoy"""
        hoy = date.today().isoformat()
        query = 'SELECT COUNT(*) as total FROM turnos WHERE fecha = ?'
        row = db.fetch_one(query, (hoy,))
        return row['total'] if row else 0
