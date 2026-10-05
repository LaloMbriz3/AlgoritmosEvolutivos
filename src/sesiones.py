def crear_sesiones(asignaciones, materias):
    # Convierte horas semanales por asignación en unidades que el algoritmo puede ubicar.
    sesiones = []

    # Evita buscar la materia desde cero para cada asignación.
    # La sintaxis {clave: valor for elemento in iterable} construye el índice.
    materias_por_id = {
        materia["id"]: materia
        for materia in materias
    }

    contador = 1

    # Se recorre cada vínculo materia-grupo-profesor definido en las asignaciones.
    for asignacion in asignaciones:
        materia = materias_por_id[asignacion["materia_id"]]

        horas = materia["horas_semana"]
        duracion_preferida = materia["duracion_preferida"]

        # Genera sesiones de duración preferida y conserva cualquier remanente
        # como una última sesión más corta.
        # while repite mientras quede al menos una sesión completa de duración preferida.
        while horas >= duracion_preferida:
            sesiones.append({
                # La f-string inserta contador y :03d lo muestra con tres dígitos.
                "id": f"S{contador:03d}",
                "asignacion_id": asignacion["id"],
                "materia_id": asignacion["materia_id"],
                "grupo_id": asignacion["grupo_id"],
                "profesor_id": asignacion["profesor_id"],
                "duracion": duracion_preferida
            })

            # -= equivale a horas = horas - duracion_preferida.
            horas -= duracion_preferida
            contador += 1

        # El if crea una última sesión solo cuando queda una fracción de horas.
        if horas > 0:
            sesiones.append({
                "id": f"S{contador:03d}",
                "asignacion_id": asignacion["id"],
                "materia_id": asignacion["materia_id"],
                "grupo_id": asignacion["grupo_id"],
                "profesor_id": asignacion["profesor_id"],
                "duracion": horas
            })

            contador += 1

    # La función entrega una lista de diccionarios, uno por sesión generada.
    return sesiones