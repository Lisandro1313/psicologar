"""
Modelo de Paciente
"""
from datetime import date, datetime
from typing import Optional

class Paciente:
    def __init__(self, id=None, nombre="", apellido="", dni="", fecha_nacimiento=None,
                 telefono="", email="", direccion="", obra_social="", numero_afiliado="",
                 motivo_consulta="", derivado_por="", fecha_alta=None, estado="activo",
                 notas="", created_at=None, updated_at=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.email = email
        self.direccion = direccion
        self.obra_social = obra_social
        self.numero_afiliado = numero_afiliado
        self.motivo_consulta = motivo_consulta
        self.derivado_por = derivado_por
        self.fecha_alta = fecha_alta or date.today()
        self.estado = estado
        self.notas = notas
        self.created_at = created_at
        self.updated_at = updated_at
    
    @property
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
    
    @property
    def edad(self):
        if self.fecha_nacimiento:
            if isinstance(self.fecha_nacimiento, str):
                fecha_nac = datetime.strptime(self.fecha_nacimiento, '%Y-%m-%d').date()
            else:
                fecha_nac = self.fecha_nacimiento
            hoy = date.today()
            return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
        return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'fecha_nacimiento': self.fecha_nacimiento,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'obra_social': self.obra_social,
            'numero_afiliado': self.numero_afiliado,
            'motivo_consulta': self.motivo_consulta,
            'derivado_por': self.derivado_por,
            'fecha_alta': self.fecha_alta,
            'estado': self.estado,
            'notas': self.notas
        }
    
    @staticmethod
    def from_db_row(row):
        """Crea un objeto Paciente desde una fila de la base de datos"""
        if row is None:
            return None
        return Paciente(
            id=row['id'],
            nombre=row['nombre'],
            apellido=row['apellido'],
            dni=row['dni'],
            fecha_nacimiento=row['fecha_nacimiento'],
            telefono=row['telefono'],
            email=row['email'],
            direccion=row['direccion'],
            obra_social=row['obra_social'],
            numero_afiliado=row['numero_afiliado'],
            motivo_consulta=row['motivo_consulta'],
            derivado_por=row['derivado_por'],
            fecha_alta=row['fecha_alta'],
            estado=row['estado'],
            notas=row['notas'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
