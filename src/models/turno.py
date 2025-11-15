"""
Modelo de Turno
"""
from datetime import date, time, datetime
from typing import Optional

class Turno:
    def __init__(self, id=None, paciente_id=None, fecha=None, hora_inicio=None,
                 hora_fin=None, estado="programado", tipo="sesion", notas="",
                 recordatorio_enviado=0, created_at=None):
        self.id = id
        self.paciente_id = paciente_id
        self.fecha = fecha or date.today()
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin
        self.estado = estado  # programado, realizado, cancelado, ausente
        self.tipo = tipo  # sesion, evaluacion, seguimiento
        self.notas = notas
        self.recordatorio_enviado = recordatorio_enviado
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'fecha': self.fecha,
            'hora_inicio': self.hora_inicio,
            'hora_fin': self.hora_fin,
            'estado': self.estado,
            'tipo': self.tipo,
            'notas': self.notas,
            'recordatorio_enviado': self.recordatorio_enviado
        }
    
    @staticmethod
    def from_db_row(row):
        """Crea un objeto Turno desde una fila de la base de datos"""
        if row is None:
            return None
        return Turno(
            id=row['id'],
            paciente_id=row['paciente_id'],
            fecha=row['fecha'],
            hora_inicio=row['hora_inicio'],
            hora_fin=row['hora_fin'],
            estado=row['estado'],
            tipo=row['tipo'],
            notas=row['notas'],
            recordatorio_enviado=row['recordatorio_enviado'],
            created_at=row['created_at']
        )
