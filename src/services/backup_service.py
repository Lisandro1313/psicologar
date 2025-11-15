"""
Servicio de Backup
Maneja copias de seguridad de la base de datos
"""
import shutil
import os
from pathlib import Path
from datetime import datetime
import zipfile

class BackupService:
    """
    Servicio para gestionar backups de la base de datos
    """
    
    def __init__(self, db_path="data/psicolarg.db"):
        self.db_path = Path(db_path)
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)
    
    def crear_backup(self) -> tuple:
        """
        Crea una copia de seguridad de la base de datos
        
        Returns:
            Tupla (exito: bool, mensaje: str, ruta: str)
        """
        if not self.db_path.exists():
            return False, "La base de datos no existe", ""
        
        try:
            # Nombre del backup con fecha y hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"psicolarg_backup_{timestamp}.db"
            backup_path = self.backup_dir / backup_name
            
            # Copiar base de datos
            shutil.copy2(self.db_path, backup_path)
            
            # Comprimir el backup
            zip_path = self.backup_dir / f"psicolarg_backup_{timestamp}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(backup_path, backup_name)
            
            # Eliminar el archivo .db sin comprimir
            backup_path.unlink()
            
            return True, f"Backup creado exitosamente", str(zip_path)
        
        except Exception as e:
            return False, f"Error al crear backup: {str(e)}", ""
    
    def restaurar_backup(self, backup_path: str) -> tuple:
        """
        Restaura una copia de seguridad
        
        Args:
            backup_path: Ruta al archivo de backup
        
        Returns:
            Tupla (exito: bool, mensaje: str)
        """
        backup_file = Path(backup_path)
        
        if not backup_file.exists():
            return False, "El archivo de backup no existe"
        
        try:
            # Crear backup de la base de datos actual antes de restaurar
            if self.db_path.exists():
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                temp_backup = self.db_path.parent / f"psicolarg_before_restore_{timestamp}.db"
                shutil.copy2(self.db_path, temp_backup)
            
            # Extraer y restaurar
            if backup_file.suffix == '.zip':
                with zipfile.ZipFile(backup_file, 'r') as zipf:
                    # Extraer el primer archivo .db encontrado
                    for file in zipf.namelist():
                        if file.endswith('.db'):
                            zipf.extract(file, self.db_path.parent)
                            extracted_path = self.db_path.parent / file
                            
                            # Mover al lugar correcto
                            if extracted_path != self.db_path:
                                shutil.move(str(extracted_path), str(self.db_path))
                            break
            else:
                # Es un archivo .db directamente
                shutil.copy2(backup_file, self.db_path)
            
            return True, "Base de datos restaurada exitosamente"
        
        except Exception as e:
            return False, f"Error al restaurar backup: {str(e)}"
    
    def listar_backups(self) -> list:
        """
        Lista todos los backups disponibles
        
        Returns:
            Lista de diccionarios con información de backups
        """
        backups = []
        
        for file in self.backup_dir.glob("psicolarg_backup_*.zip"):
            stat = file.stat()
            backups.append({
                'nombre': file.name,
                'ruta': str(file),
                'fecha': datetime.fromtimestamp(stat.st_mtime),
                'tamaño': self._format_size(stat.st_size)
            })
        
        # Ordenar por fecha (más reciente primero)
        backups.sort(key=lambda x: x['fecha'], reverse=True)
        
        return backups
    
    def eliminar_backup(self, backup_path: str) -> tuple:
        """
        Elimina un archivo de backup
        
        Args:
            backup_path: Ruta al backup a eliminar
        
        Returns:
            Tupla (exito: bool, mensaje: str)
        """
        try:
            backup_file = Path(backup_path)
            if backup_file.exists():
                backup_file.unlink()
                return True, "Backup eliminado exitosamente"
            else:
                return False, "El backup no existe"
        except Exception as e:
            return False, f"Error al eliminar backup: {str(e)}"
    
    def limpiar_backups_antiguos(self, dias: int = 30) -> int:
        """
        Elimina backups más antiguos que X días
        
        Args:
            dias: Número de días de antigüedad
        
        Returns:
            Número de backups eliminados
        """
        from datetime import timedelta
        
        limite = datetime.now() - timedelta(days=dias)
        eliminados = 0
        
        for backup in self.listar_backups():
            if backup['fecha'] < limite:
                exito, _ = self.eliminar_backup(backup['ruta'])
                if exito:
                    eliminados += 1
        
        return eliminados
    
    def _format_size(self, size_bytes: int) -> str:
        """Formatea el tamaño en bytes a formato legible"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"
    
    def backup_automatico_habilitado(self) -> bool:
        """Verifica si el backup automático está habilitado"""
        config_file = self.backup_dir / "auto_backup.conf"
        return config_file.exists()
    
    def configurar_backup_automatico(self, habilitado: bool, dias: int = 7):
        """Configura el backup automático"""
        config_file = self.backup_dir / "auto_backup.conf"
        
        if habilitado:
            with open(config_file, 'w') as f:
                f.write(f"enabled=true\n")
                f.write(f"dias={dias}\n")
        else:
            if config_file.exists():
                config_file.unlink()


# Instancia global del servicio de backup
backup_service = BackupService()
