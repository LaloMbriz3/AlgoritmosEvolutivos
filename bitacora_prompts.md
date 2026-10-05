# Bitácora de Prompts - Bloque 1

**Interacción 1: Búsqueda del problema realista**
* **Prompt:** "Nuestra rama es algoritmos evolutivos. Sugiere un problema real, complejo y logístico para nuestro Bloque 1 que justifique el uso de esta IA."
* **Corrección/Acción:** Elegimos el problema de asignación de horarios (Timetabling) y descartamos la optimización de rutas geográficas por falta de viabilidad para un sprint corto.

**Interacción 2: Estructura de datos**
* **Prompt:** "¿Cuáles serían los datos de entrada exactos para un algoritmo evolutivo que asigne horarios escolares?"
* **Corrección/Acción:** La IA sugirió diccionarios en el código, pero el equipo lo corrigió creando archivos JSON independientes (materias, profesores, grupos, salones) para mejorar la escalabilidad.

**Interacción 3: Densidad de Horarios (Huecos)**
* **Prompt:** "El algoritmo web genera horarios válidos pero con muchos huecos. ¿Cómo solucionamos las horas libres?"
* **Corrección/Acción:** Se identificó que las restricciones duras funcionaban, pero las suaves no. Aumentamos la carga horaria semanal en materias.json para saturar el turno matutino.
