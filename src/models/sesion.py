"""
Modelo de Sesión
"""
from datetime import date, datetime
from typing import Optional

class Sesion:
    def __init__(self, id=None, paciente_id=None, turno_id=None, fecha=None,
                 duracion=None, notas="", objetivos="", intervenciones="",
                 observaciones="", proxima_sesion="", created_at=None, updated_at=None):
        self.id = id
        self.paciente_id = paciente_id
        self.turno_id = turno_id
        self.fecha = fecha or date.today()
        self.duracion = duracion  # en minutos
        self.notas = notas
        self.objetivos = objetivos
        self.intervenciones = intervenciones
        self.observaciones = observaciones
        self.proxima_sesion = proxima_sesion
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'turno_id': self.turno_id,
            'fecha': self.fecha,
            'duracion': self.duracion,
            'notas': self.notas,
            'objetivos': self.objetivos,
            'intervenciones': self.intervenciones,
            'observaciones': self.observaciones,
            'proxima_sesion': self.proxima_sesion
        }
    
    @staticmethod
    def from_db_row(row):
        """Crea un objeto Sesion desde una fila de la base de datos"""
        if row is None:
            return None
        return Sesion(
            id=row['id'],
            paciente_id=row['paciente_id'],
            turno_id=row['turno_id'],
            fecha=row['fecha'],
            duracion=row['duracion'],
            notas=row['notas'],
            objetivos=row['objetivos'],
            intervenciones=row['intervenciones'],
            observaciones=row['observaciones'],
            proxima_sesion=row['proxima_sesion'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
