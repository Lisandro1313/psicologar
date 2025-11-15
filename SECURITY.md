# Guía de Seguridad - PsicolaRG

## 🔒 Características de Seguridad

PsicolaRG implementa múltiples capas de seguridad para proteger los datos sensibles de sus pacientes:

### 1. Autenticación
- **Contraseña Maestra**: Acceso protegido con contraseña al iniciar la aplicación
- **Hash Seguro**: Las contraseñas se almacenan usando PBKDF2-SHA256 con 100,000 iteraciones
- **Sin Recuperación**: Por seguridad, no hay forma de recuperar una contraseña olvidada (debe reinstalar)

### 2. Cifrado de Datos
- **Cifrado Simétrico**: Utiliza Fernet (AES-128) para cifrar datos sensibles
- **Clave Única**: Cada instalación genera su propia clave de cifrado
- **Datos Protegidos**: Notas clínicas, datos personales y toda información sensible

### 3. Almacenamiento Local
- **Base de Datos SQLite**: Los datos se almacenan localmente en tu computadora
- **Sin Conexión a Internet**: No se envía información a servidores externos (excepto IA opcional)
- **Control Total**: Tú decides dónde y cómo se almacenan tus datos

### 4. Sistema de Backups
- **Backups Manuales**: Crea copias de seguridad cuando lo necesites
- **Compresión ZIP**: Los backups se comprimen para ahorrar espacio
- **Restauración Segura**: Restaura tu base de datos en cualquier momento

## 🛡️ Mejores Prácticas

### Contraseña Maestra
1. **Usa una contraseña fuerte** (mínimo 8 caracteres)
2. Incluye mayúsculas, minúsculas, números y símbolos
3. No uses palabras comunes o datos personales
4. **Guárdala en un lugar seguro** (gestor de contraseñas)

### Backups
1. **Realiza backups periódicos** (semanal o mensual)
2. Guarda los backups en:
   - Disco externo (desconectado cuando no se use)
   - USB cifrado
   - Nube personal cifrada (Google Drive, OneDrive con cifrado adicional)
3. **No dejes backups** en la misma computadora sin protección

### Computadora
1. Mantén tu sistema operativo actualizado
2. Usa antivirus actualizado
3. No compartas tu usuario de Windows con otras personas
4. Cierra la aplicación cuando no la uses
5. Considera usar cifrado de disco completo (BitLocker en Windows)

## 📋 Cumplimiento Legal

PsicolaRG está diseñado para ayudarte a cumplir con:

### Leyes de Protección de Datos
- **GDPR** (Europa): Almacenamiento local y cifrado
- **HIPAA** (EE.UU.): Seguridad de datos de salud
- **Ley de Protección de Datos Personales** (Argentina y otros)

### Secreto Profesional
- Los datos no se comparten con terceros
- Tú mantienes el control absoluto de la información
- Posibilidad de eliminar datos permanentemente

## ⚠️ Limitaciones y Responsabilidades

### Lo que PsicolaRG NO protege
- Si tu computadora es infectada con malware
- Si alguien tiene acceso físico a tu computadora desbloqueada
- Si compartes tu contraseña maestra
- Si no realizas backups y pierdes tu disco duro

### Responsabilidad del Profesional
Como profesional de la salud mental, es TU responsabilidad:
1. Mantener la confidencialidad de tus pacientes
2. Cumplir con las leyes locales de protección de datos
3. Realizar backups regulares
4. Proteger el acceso físico a tu computadora
5. Informar a tus pacientes sobre cómo se almacenan sus datos

## 🔧 Configuración Recomendada

### Primera Instalación
1. Configura una contraseña maestra fuerte
2. Anota la contraseña en un lugar seguro
3. Realiza un backup de prueba
4. Verifica que puedes restaurar el backup

### Uso Diario
1. Siempre cierra la aplicación al terminar
2. No dejes la pantalla desbloqueada
3. Realiza backups después de sesiones importantes
4. Revisa periódicamente la configuración de seguridad

### Mantenimiento
1. Cambia la contraseña cada 3-6 meses
2. Limpia backups antiguos (mantén últimos 3-5)
3. Revisa los logs de acceso (si están habilitados)
4. Actualiza la aplicación cuando haya nuevas versiones

## 📞 Soporte

Si tienes dudas sobre seguridad:
1. Lee esta guía completamente
2. Consulta el README.md del proyecto
3. Abre un issue en GitHub (sin compartir datos sensibles)
4. Consulta con un especialista en seguridad informática

## ⚖️ Disclaimer Legal

**IMPORTANTE**: Esta aplicación es una herramienta de apoyo. El profesional es el único responsable de:
- Cumplir con las leyes locales
- Proteger la confidencialidad de sus pacientes
- Mantener la seguridad de los datos
- Realizar backups adecuados

El desarrollador de PsicolaRG no se hace responsable por el mal uso de la aplicación o pérdida de datos debido a negligencia del usuario.

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0.0
