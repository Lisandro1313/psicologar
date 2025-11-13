"""
Controlador de Pacientes
Maneja la lógica de negocio para la gestión de pacientes
"""
from src.database.db_manager import db
from src.models.paciente import Paciente
from datetime import datetime

class PacienteController:
    
    @staticmethod
    def crear_paciente(paciente):
        """Crea un nuevo paciente en la base de datos"""
        query = '''
            INSERT INTO pacientes (nombre, apellido, dni, fecha_nacimiento, telefono, 
                                 email, direccion, obra_social, numero_afiliado, 
                                 motivo_consulta, derivado_por, fecha_alta, estado, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            paciente.nombre, paciente.apellido, paciente.dni, paciente.fecha_nacimiento,
            paciente.telefono, paciente.email, paciente.direccion, paciente.obra_social,
            paciente.numero_afiliado, paciente.motivo_consulta, paciente.derivado_por,
            paciente.fecha_alta, paciente.estado, paciente.notas
        )
        cursor = db.execute_query(query, params)
        paciente.id = cursor.lastrowid
        return paciente
    
    @staticmethod
    def obtener_paciente(paciente_id):
        """Obtiene un paciente por su ID"""
        query = 'SELECT * FROM pacientes WHERE id = ?'
        row = db.fetch_one(query, (paciente_id,))
        return Paciente.from_db_row(row)
    
    @staticmethod
    def obtener_todos_pacientes(estado=None):
        """Obtiene todos los pacientes, opcionalmente filtrados por estado"""
        if estado:
            query = 'SELECT * FROM pacientes WHERE estado = ? ORDER BY apellido, nombre'
            rows = db.fetch_all(query, (estado,))
        else:
            query = 'SELECT * FROM pacientes ORDER BY apellido, nombre'
            rows = db.fetch_all(query)
        
        return [Paciente.from_db_row(row) for row in rows]
    
    @staticmethod
    def buscar_pacientes(termino):
        """Busca pacientes por nombre, apellido o DNI"""
        query = '''
            SELECT * FROM pacientes 
            WHERE nombre LIKE ? OR apellido LIKE ? OR dni LIKE ?
            ORDER BY apellido, nombre
        '''
        termino_busqueda = f'%{termino}%'
        rows = db.fetch_all(query, (termino_busqueda, termino_busqueda, termino_busqueda))
        return [Paciente.from_db_row(row) for row in rows]
    
    @staticmethod
    def actualizar_paciente(paciente):
        """Actualiza los datos de un paciente"""
        query = '''
            UPDATE pacientes 
            SET nombre = ?, apellido = ?, dni = ?, fecha_nacimiento = ?, telefono = ?,
                email = ?, direccion = ?, obra_social = ?, numero_afiliado = ?,
                motivo_consulta = ?, derivado_por = ?, estado = ?, notas = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        '''
        params = (
            paciente.nombre, paciente.apellido, paciente.dni, paciente.fecha_nacimiento,
            paciente.telefono, paciente.email, paciente.direccion, paciente.obra_social,
            paciente.numero_afiliado, paciente.motivo_consulta, paciente.derivado_por,
            paciente.estado, paciente.notas, paciente.id
        )
        db.execute_query(query, params)
        return paciente
    
    @staticmethod
    def eliminar_paciente(paciente_id):
        """Elimina un paciente (cambio de estado a 'inactivo')"""
        query = 'UPDATE pacientes SET estado = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?'
        db.execute_query(query, ('inactivo', paciente_id))
    
    @staticmethod
    def contar_pacientes_activos():
        """Cuenta el número de pacientes activos"""
        query = 'SELECT COUNT(*) as total FROM pacientes WHERE estado = ?'
        row = db.fetch_one(query, ('activo',))
        return row['total'] if row else 0
