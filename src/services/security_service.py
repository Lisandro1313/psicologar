"""
Servicio de Seguridad y Cifrado
Maneja autenticación, cifrado de datos y generación de claves
"""
import hashlib
import secrets
import os
from cryptography.fernet import Fernet
from pathlib import Path

class SecurityService:
    """
    Servicio de seguridad para la aplicación
    """
    
    def __init__(self):
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        self.key_file = self.config_dir / "secret.key"
        self.auth_file = self.config_dir / "auth.hash"
        self._cipher = None
    
    def inicializar_seguridad(self):
        """Inicializa el sistema de seguridad"""
        if not self.key_file.exists():
            self._generar_clave()
        self._cargar_clave()
    
    def _generar_clave(self):
        """Genera una clave de cifrado y la guarda"""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(key)
        
        # Establecer permisos restrictivos en el archivo (solo lectura)
        try:
            os.chmod(self.key_file, 0o600)
        except:
            pass  # Windows no soporta chmod de la misma manera
    
    def _cargar_clave(self):
        """Carga la clave de cifrado"""
        if self.key_file.exists():
            with open(self.key_file, 'rb') as f:
                key = f.read()
            self._cipher = Fernet(key)
    
    def cifrar_texto(self, texto: str) -> str:
        """
        Cifra un texto
        
        Args:
            texto: Texto a cifrar
        
        Returns:
            Texto cifrado en formato base64
        """
        if not self._cipher:
            self._cargar_clave()
        
        if not texto:
            return ""
        
        texto_bytes = texto.encode('utf-8')
        cifrado = self._cipher.encrypt(texto_bytes)
        return cifrado.decode('utf-8')
    
    def descifrar_texto(self, texto_cifrado: str) -> str:
        """
        Descifra un texto
        
        Args:
            texto_cifrado: Texto cifrado en formato base64
        
        Returns:
            Texto descifrado
        """
        if not self._cipher:
            self._cargar_clave()
        
        if not texto_cifrado:
            return ""
        
        try:
            cifrado_bytes = texto_cifrado.encode('utf-8')
            descifrado = self._cipher.decrypt(cifrado_bytes)
            return descifrado.decode('utf-8')
        except Exception as e:
            print(f"Error al descifrar: {e}")
            return texto_cifrado  # Devolver el texto original si falla
    
    def hash_password(self, password: str, salt: str = None) -> tuple:
        """
        Genera un hash seguro de una contraseña
        
        Args:
            password: Contraseña a hashear
            salt: Salt opcional (se genera uno nuevo si no se proporciona)
        
        Returns:
            Tupla (hash, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Usar PBKDF2 con SHA256
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000  # 100,000 iteraciones
        )
        
        return password_hash.hex(), salt
    
    def verificar_password(self, password: str, hash_guardado: str, salt: str) -> bool:
        """
        Verifica si una contraseña coincide con su hash
        
        Args:
            password: Contraseña a verificar
            hash_guardado: Hash guardado
            salt: Salt usado para generar el hash
        
        Returns:
            True si la contraseña es correcta
        """
        password_hash, _ = self.hash_password(password, salt)
        return password_hash == hash_guardado
    
    def configurar_password(self, password: str):
        """
        Configura la contraseña maestra de la aplicación
        
        Args:
            password: Nueva contraseña
        """
        password_hash, salt = self.hash_password(password)
        
        with open(self.auth_file, 'w') as f:
            f.write(f"{password_hash}\n{salt}")
        
        # Establecer permisos restrictivos
        try:
            os.chmod(self.auth_file, 0o600)
        except:
            pass
    
    def password_configurado(self) -> bool:
        """
        Verifica si ya se configuró una contraseña
        
        Returns:
            True si existe una contraseña configurada
        """
        return self.auth_file.exists()
    
    def autenticar(self, password: str) -> bool:
        """
        Autentica al usuario con su contraseña
        
        Args:
            password: Contraseña ingresada
        
        Returns:
            True si la autenticación es exitosa
        """
        if not self.auth_file.exists():
            return False
        
        try:
            with open(self.auth_file, 'r') as f:
                lines = f.read().strip().split('\n')
                hash_guardado = lines[0]
                salt = lines[1]
            
            return self.verificar_password(password, hash_guardado, salt)
        except Exception as e:
            print(f"Error en autenticación: {e}")
            return False
    
    def generar_token_sesion(self) -> str:
        """
        Genera un token único para la sesión
        
        Returns:
            Token de sesión
        """
        return secrets.token_urlsafe(32)
    
    def validar_fortaleza_password(self, password: str) -> tuple:
        """
        Valida la fortaleza de una contraseña
        
        Args:
            password: Contraseña a validar
        
        Returns:
            Tupla (es_valida: bool, mensaje: str)
        """
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        
        tiene_mayuscula = any(c.isupper() for c in password)
        tiene_minuscula = any(c.islower() for c in password)
        tiene_numero = any(c.isdigit() for c in password)
        tiene_especial = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        fortaleza = sum([tiene_mayuscula, tiene_minuscula, tiene_numero, tiene_especial])
        
        if fortaleza < 3:
            return False, "La contraseña debe contener mayúsculas, minúsculas, números y caracteres especiales"
        
        return True, "Contraseña válida"
    
    def cambiar_password(self, password_actual: str, password_nueva: str) -> tuple:
        """
        Cambia la contraseña maestra
        
        Args:
            password_actual: Contraseña actual
            password_nueva: Nueva contraseña
        
        Returns:
            Tupla (exito: bool, mensaje: str)
        """
        # Verificar contraseña actual
        if not self.autenticar(password_actual):
            return False, "La contraseña actual es incorrecta"
        
        # Validar nueva contraseña
        valida, mensaje = self.validar_fortaleza_password(password_nueva)
        if not valida:
            return False, mensaje
        
        # Configurar nueva contraseña
        self.configurar_password(password_nueva)
        return True, "Contraseña cambiada exitosamente"


# Instancia global del servicio de seguridad
security_service = SecurityService()
