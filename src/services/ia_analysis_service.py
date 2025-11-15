"""
Servicio de Análisis con IA
Utiliza OpenAI GPT para analizar sesiones y detectar patrones
"""
import os
from typing import List, Dict
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class IAAnalysisService:
    """
    Servicio para análisis de sesiones con IA
    """
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"
        self.available = bool(self.api_key and self.api_key != "tu_api_key_aqui")
    
    def analizar_sesion(self, sesion_text: str) -> Dict:
        """
        Analiza una sesión individual
        
        Args:
            sesion_text: Texto de la sesión (notas, objetivos, etc.)
        
        Returns:
            Dict con palabras_clave, sentimiento, temas_principales, recomendaciones
        """
        if not self.available:
            return self._analisis_basico(sesion_text)
        
        try:
            # Aquí iría la llamada a OpenAI API
            # Por ahora devolvemos un análisis básico
            return self._analisis_basico(sesion_text)
        except Exception as e:
            print(f"Error en análisis con IA: {e}")
            return self._analisis_basico(sesion_text)
    
    def analizar_multiples_sesiones(self, sesiones_texts: List[str]) -> Dict:
        """
        Analiza múltiples sesiones para detectar patrones longitudinales
        
        Args:
            sesiones_texts: Lista de textos de sesiones
        
        Returns:
            Dict con patrones, evolución, palabras_recurrentes, insights
        """
        if not self.available:
            return self._analisis_patron_basico(sesiones_texts)
        
        try:
            # Aquí iría la llamada a OpenAI API para análisis longitudinal
            return self._analisis_patron_basico(sesiones_texts)
        except Exception as e:
            print(f"Error en análisis de patrones: {e}")
            return self._analisis_patron_basico(sesiones_texts)
    
    def extraer_palabras_clave(self, texto: str, top_n: int = 10) -> List[str]:
        """
        Extrae las palabras clave más importantes de un texto
        
        Args:
            texto: Texto a analizar
            top_n: Número de palabras clave a retornar
        
        Returns:
            Lista de palabras clave
        """
        # Implementación básica sin IA
        # Filtrar palabras comunes
        palabras_comunes = {'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 
                           'no', 'haber', 'por', 'con', 'su', 'para', 'como', 'estar',
                           'tener', 'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o',
                           'poder', 'decir', 'este', 'ir', 'otro', 'ese', 'si', 'me',
                           'ya', 'ver', 'porque', 'dar', 'cuando', 'él', 'muy', 'sin'}
        
        palabras = texto.lower().split()
        palabras_filtradas = [p for p in palabras if len(p) > 4 and p not in palabras_comunes]
        
        # Contar frecuencias
        from collections import Counter
        contador = Counter(palabras_filtradas)
        
        return [palabra for palabra, _ in contador.most_common(top_n)]
    
    def analizar_sentimiento(self, texto: str) -> str:
        """
        Analiza el sentimiento general del texto
        
        Args:
            texto: Texto a analizar
        
        Returns:
            Sentimiento: positivo, negativo, neutral
        """
        # Implementación básica basada en palabras clave
        palabras_positivas = {'mejor', 'mejoría', 'progreso', 'bien', 'feliz', 'contento',
                             'alegre', 'optimista', 'logro', 'avance', 'satisfecho'}
        palabras_negativas = {'peor', 'mal', 'triste', 'deprimido', 'ansioso', 'ansiedad',
                             'preocupado', 'problema', 'dificultad', 'crisis', 'dolor'}
        
        texto_lower = texto.lower()
        palabras = set(texto_lower.split())
        
        positivas = len(palabras.intersection(palabras_positivas))
        negativas = len(palabras.intersection(palabras_negativas))
        
        if positivas > negativas:
            return "positivo"
        elif negativas > positivas:
            return "negativo"
        else:
            return "neutral"
    
    def _analisis_basico(self, texto: str) -> Dict:
        """Análisis básico sin IA"""
        return {
            'palabras_clave': self.extraer_palabras_clave(texto, 8),
            'sentimiento': self.analizar_sentimiento(texto),
            'temas_principales': self._extraer_temas(texto),
            'recomendaciones': self._generar_recomendaciones_basicas(texto)
        }
    
    def _analisis_patron_basico(self, textos: List[str]) -> Dict:
        """Análisis de patrones básico sin IA"""
        todas_palabras = []
        sentimientos = []
        
        for texto in textos:
            todas_palabras.extend(self.extraer_palabras_clave(texto, 5))
            sentimientos.append(self.analizar_sentimiento(texto))
        
        from collections import Counter
        palabras_recurrentes = Counter(todas_palabras).most_common(10)
        
        return {
            'palabras_recurrentes': [p[0] for p in palabras_recurrentes],
            'frecuencias': dict(palabras_recurrentes),
            'evolucion_sentimiento': sentimientos,
            'tendencia': self._calcular_tendencia(sentimientos),
            'total_sesiones': len(textos),
            'insights': self._generar_insights(palabras_recurrentes, sentimientos)
        }
    
    def _extraer_temas(self, texto: str) -> List[str]:
        """Extrae temas principales del texto"""
        temas_psicologicos = {
            'ansiedad': ['ansiedad', 'ansioso', 'nervioso', 'preocupación', 'estrés'],
            'depresión': ['depresión', 'tristeza', 'deprimido', 'desmotivación'],
            'relaciones': ['pareja', 'familia', 'relación', 'familiar', 'amistad'],
            'trabajo': ['trabajo', 'laboral', 'empleo', 'jefe', 'compañeros'],
            'autoestima': ['autoestima', 'confianza', 'valoración', 'autoimagen'],
            'trauma': ['trauma', 'pasado', 'recuerdo', 'infancia'],
        }
        
        texto_lower = texto.lower()
        temas_encontrados = []
        
        for tema, palabras in temas_psicologicos.items():
            if any(palabra in texto_lower for palabra in palabras):
                temas_encontrados.append(tema)
        
        return temas_encontrados if temas_encontrados else ['general']
    
    def _generar_recomendaciones_basicas(self, texto: str) -> List[str]:
        """Genera recomendaciones básicas"""
        recomendaciones = []
        
        if 'ansiedad' in texto.lower() or 'ansioso' in texto.lower():
            recomendaciones.append("Considerar técnicas de relajación y respiración")
        
        if 'tristeza' in texto.lower() or 'deprimido' in texto.lower():
            recomendaciones.append("Evaluar síntomas depresivos y considerar intervenciones específicas")
        
        if 'familia' in texto.lower() or 'pareja' in texto.lower():
            recomendaciones.append("Explorar dinámicas relacionales y patrones de comunicación")
        
        if not recomendaciones:
            recomendaciones.append("Continuar con el trabajo terapéutico actual")
        
        return recomendaciones
    
    def _calcular_tendencia(self, sentimientos: List[str]) -> str:
        """Calcula la tendencia de evolución"""
        if len(sentimientos) < 2:
            return "sin datos suficientes"
        
        # Convertir a valores numéricos
        valores = {'positivo': 1, 'neutral': 0, 'negativo': -1}
        numeros = [valores.get(s, 0) for s in sentimientos]
        
        # Calcular tendencia simple
        inicio = sum(numeros[:len(numeros)//2])
        fin = sum(numeros[len(numeros)//2:])
        
        if fin > inicio:
            return "mejorando"
        elif fin < inicio:
            return "empeorando"
        else:
            return "estable"
    
    def _generar_insights(self, palabras_freq: List[tuple], sentimientos: List[str]) -> List[str]:
        """Genera insights del análisis"""
        insights = []
        
        # Insight sobre palabras recurrentes
        if palabras_freq:
            palabra_mas_comun = palabras_freq[0][0]
            freq = palabras_freq[0][1]
            insights.append(f"La palabra '{palabra_mas_comun}' aparece {freq} veces en las sesiones")
        
        # Insight sobre sentimientos
        from collections import Counter
        sentimientos_count = Counter(sentimientos)
        sentimiento_predominante = sentimientos_count.most_common(1)[0][0]
        insights.append(f"El sentimiento predominante es: {sentimiento_predominante}")
        
        # Insight sobre evolución
        if len(sentimientos) >= 3:
            tendencia = self._calcular_tendencia(sentimientos)
            insights.append(f"La tendencia general es: {tendencia}")
        
        return insights


# Instancia global del servicio
ia_service = IAAnalysisService()
