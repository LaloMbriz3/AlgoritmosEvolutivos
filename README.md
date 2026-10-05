# Optimización Evolutiva de Horarios y Espacios Académicos

## 1. Problemática a resolver
La creación manual de horarios escolares es un proceso ineficiente, lento y propenso a errores humanos. Coordinar materias, disponibilidad docente y capacidad de aulas genera choques constantes, afectando a alumnos con tiempos muertos y a maestros con sobrecarga.

## 2. Descripción del proyecto
Generador automático de horarios mediante un algoritmo evolutivo (IA).
- **Entrada:** Archivos estructurados JSON de docentes, materias, grupos y espacios (Datos de prueba sintéticos).
- **Salida:** Asignación optimizada de horarios sin empalmes, visualizada en una interfaz web intuitiva.

## 3. Rama de IA: Algoritmos Evolutivos
Soluciona un problema de optimización combinatoria (Timetabling) creando poblaciones de horarios aleatorios, evaluando conflictos (fitness) y aplicando cruza/mutación iterativamente hasta lograr una solución viable sin colapsar el sistema.

## 4. Requisitos e Instalación

**Requisitos previos:** Python 3.10 o superior.

1. Clonar el repositorio: `git clone https://github.com/LaloMbriz3/AlgoritmosEvolutivos.git`
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar el servidor local: `python app.py`
4. Abrir en el navegador: `http://127.0.0.1:5000/`

## 5. Créditos y Licencias

**Librerías y Herramientas utilizadas:**
- **DEAP (Distributed Evolutionary Algorithms in Python):** Utilizada para la creación de la población, evaluación (fitness), cruza y mutación.
- **Flask:** Utilizada para el enrutamiento y despliegue del servidor web local.
- **Datos (Datasets):** Los archivos JSON (materias, profesores, salones, grupos) fueron creados manualmente por el equipo de análisis como datos de prueba sintéticos.

**Declaración de uso de Inteligencia Artificial (IA):**
- **Generado con asistencia de IA:** La estructura base del algoritmo con DEAP, la configuración del servidor web con Flask y el CSS base de la interfaz gráfica fueron desarrollados con asistencia de IA generativa (Gemini) actuando como copiloto de programación.
- **Modificado por el equipo:** La lógica de evaluación de restricciones (Hard y Soft constraints en `evaluacion.py`), el modelo de datos en JSON, el ajuste de hiperparámetros (tasa de mutación y tamaño de población), y la distribución de los bloques horarios para asegurar la densidad del horario (evitar huecos), fueron modificados y afinados manualmente por el equipo de desarrollo e investigación.
```eof

