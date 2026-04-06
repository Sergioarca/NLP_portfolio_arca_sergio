# Informe de Desarrollo: Smart Chat Assistant (Lab_Exercises_3)

Este documento detalla el proceso de diseño, implementación y optimización de la aplicación desarrollada para el ejercicio de laboratorio número 3 de la asignatura **Procesamiento del Lenguaje Natural**.

## 1. Objetivo del Proyecto
El objetivo principal era construir un sistema de procesamiento de lenguaje natural completo que utilizara un modelo de lenguaje de gran tamaño (LLM) alojado localmente. La aplicación supera la interacción básica de "pregunta-respuesta" mediante un pipeline de razonamiento avanzado y refinamiento automático.

## 2. Decisiones Técnicas y Optimización

### Elección del Modelo Local
Se ha seleccionado **Llama 3.2 (3B)** como motor principal:
- **Optimización**: Se priorizó este modelo de 2GB frente a otros de 14GB para garantizar una latencia mínima y una ejecución fluida en hardware local.
- **Rendimiento**: Permite realizar múltiples pasadas (análisis, borrador y refinamiento) en pocos segundos.

### Arquitectura de la Aplicación
- **Interfaz**: Desarrollada con **Streamlit**, utilizando una estética oscura y componentes de chat nativos.
- **Backend**: Comunicación directa con la API de Ollama mediante streaming HTTP.

## 3. Pipeline de Razonamiento (Valor Añadido)

La aplicación implementa una jerarquía de procesamiento que separa el "pensamiento" de la "respuesta final":

### Fase de Pensamiento y Análisis (Interna)
Cuando el usuario envía una consulta, el sistema activa un proceso interno visible mediante un estado de carga ("🧠 Pensando y Analizando..."):
1.  **Análisis de Intención**: El modelo identifica la mejor estrategia para responder.
2.  **Borrador Interno**: Se genera una primera versión de la respuesta basada en el historial de la conversación. Este borrador no se muestra directamente al usuario para evitar ruido visual.

### Respuesta Final Inteligente (Refinamiento)
Una vez concluido el pensamiento interno, el sistema ejecuta una **Fase de Refinamiento**. El modelo toma el borrador previo y lo pule para mejorar su claridad, estructura y precisión técnica. Esta versión refinada es la que se muestra en el chat y la que se guarda en la memoria del asistente.

## 4. Gestión de Memoria y UX
- **Contexto Persistente**: Se utiliza `st.session_state` para mantener el hilo de la conversación, pero solo almacenando las versiones refinadas de las respuestas para mantener la calidad del contexto.
- **Streaming de Alta Calidad**: El usuario ve cómo se escribe la respuesta final en tiempo real, proporcionando una sensación de interactividad natural.

## 5. Conclusión
Este laboratorio demuestra cómo el postprocesamiento (refinamiento) puede transformar una respuesta genérica en una solución experta y bien estructurada, elevando la calidad de la interacción hombre-máquina sin necesidad de modelos masivamente pesados.
