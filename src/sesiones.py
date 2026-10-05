def crear_sesiones(asignaciones, materias):
    sesiones = []

    materias_por_id = {
        materia["id"]: materia
        for materia in materias
    }

    contador = 1

    for asignacion in asignaciones:
        materia = materias_por_id[asignacion["materia_id"]]

        horas = materia["horas_semana"]
        duracion_preferida = materia["duracion_preferida"]

        while horas >= duracion_preferida:
            sesiones.append({
                "id": f"S{contador:03d}",
                "asignacion_id": asignacion["id"],
                "materia_id": asignacion["materia_id"],
                "grupo_id": asignacion["grupo_id"],
                "profesor_id": asignacion["profesor_id"],
                "duracion": duracion_preferida
            })

            horas -= duracion_preferida
            contador += 1

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

    return sesiones