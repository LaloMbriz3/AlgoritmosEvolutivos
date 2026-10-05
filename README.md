# Optimización Evolutiva de Horarios y Espacios Académicos

## 1. Problemática a resolver

La creación manual de horarios es ineficiente y propensa a errores. Coordinar materias, disponibilidad docente y aulas genera choques constantes, afectando a alumnos con tiempos muertos y a maestros con sobrecarga.

## 2. Descripción del proyecto

Generador automático de horarios mediante evolución simulada.

- **Entrada:** Archivos JSON de docentes, materias, grupos y aulas.
- **Salida:** Asignación optimizada de horarios sin empalmes en interfaz web.

## 3. Rama de IA: Algoritmos Evolutivos

Soluciona un problema de optimización combinatoria (Timetabling) creando poblaciones de horarios, evaluando conflictos (fitness) y aplicando cruza/mutación hasta lograr viabilidad.

## 4. Instalación

1. Clonar: `git clone https://github.com/LaloMbriz3/AlgoritmosEvolutivos.git`
2. Instalar: `pip install -r requirements.txt`
3. Ejecutar: `python app.py`
