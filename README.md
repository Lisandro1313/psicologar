# PsicolaRG 🧠

Sistema de gestión profesional para psicólogos con análisis inteligente de sesiones.

## Características

- 📋 **Gestión de Pacientes**: Registro completo con datos personales seguros
- 📅 **Calendario de Turnos**: Agenda y visualiza citas fácilmente  
- 📝 **Registro de Sesiones**: Notas detalladas, objetivos, intervenciones y observaciones
- 🤖 **Análisis con IA**: Detección de patrones, palabras clave y análisis de sentimiento
- 🔒 **Seguridad Avanzada**: Autenticación, cifrado de datos y backups
- 💾 **Sistema de Backups**: Copias de seguridad automáticas y restauración
- 📊 **Dashboard**: Estadísticas y métricas de tu práctica profesional

## Seguridad

- ✅ **Autenticación con contraseña maestra**
- ✅ **Cifrado de datos sensibles** (AES-128)
- ✅ **Almacenamiento local** (sin envío a servidores)
- ✅ **Backups comprimidos y seguros**
- ✅ **Cumplimiento con normativas de protección de datos**

> **Ver [SECURITY.md](SECURITY.md) para más información sobre seguridad**

## Instalación

1. Instalar Python 3.10 o superior
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar variables de entorno:

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

4. Ejecutar la aplicación:

```bash
python main.py
```

## Seguridad

Todos los datos se almacenan localmente en tu computadora con cifrado. No se envía información a servidores externos (excepto para análisis con IA, opcional).

## Cumplimiento Legal

Esta aplicación está diseñada para ayudar a cumplir con:

- Leyes de protección de datos personales
- Confidencialidad profesional
- Secreto profesional del psicólogo

**Nota**: Es responsabilidad del profesional cumplir con las normativas locales.
