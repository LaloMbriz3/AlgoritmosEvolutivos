def evaluar_horario(solucion, sesiones, datos):
    penalizacion = 0

    grupos_ocupados = set()
    profesores_ocupados = set()
    salones_ocupados = set()

    bloques_por_id = {
        bloque["id"]: bloque
        for bloque in datos["bloques"]
    }

    # ==========================================
    # 1. RESTRICCIONES DURAS
    # ==========================================

    for sesion, opcion in zip(sesiones, solucion):

        grupo_id = sesion["grupo_id"]
        profesor_id = sesion["profesor_id"]

        for bloque_id in opcion["bloques"]:

            clave_grupo = (grupo_id, bloque_id)
            clave_profesor = (profesor_id, bloque_id)
            clave_salon = (opcion["salon_id"], bloque_id)

            # Un grupo no puede tener dos clases al mismo tiempo
            if clave_grupo in grupos_ocupados:
                penalizacion += 1000

            # Un profesor no puede impartir dos clases al mismo tiempo
            if clave_profesor in profesores_ocupados:
                penalizacion += 1000

            # Un salón no puede tener dos clases al mismo tiempo
            if clave_salon in salones_ocupados:
                penalizacion += 1000

            grupos_ocupados.add(clave_grupo)
            profesores_ocupados.add(clave_profesor)
            salones_ocupados.add(clave_salon)

    # ==========================================
    # 2. REDUCIR HUECOS EN EL HORARIO
    # ==========================================

    bloques_por_grupo = {}

    for sesion, opcion in zip(sesiones, solucion):

        grupo_id = sesion["grupo_id"]

        if grupo_id not in bloques_por_grupo:
            bloques_por_grupo[grupo_id] = {}

        for bloque_id in opcion["bloques"]:

            bloque = bloques_por_id[bloque_id]

            dia = bloque["dia"]

            if dia not in bloques_por_grupo[grupo_id]:
                bloques_por_grupo[grupo_id][dia] = []

            bloques_por_grupo[grupo_id][dia].append(bloque)

    dias = {
        "Lunes": 0,
        "Martes": 1,
        "Miércoles": 2,
        "Jueves": 3,
        "Viernes": 4
    }

    for grupo_id, dias_grupo in bloques_por_grupo.items():

        for dia, bloques in dias_grupo.items():

            bloques_ordenados = sorted(
                bloques,
                key=lambda bloque: bloque["hora_inicio"]
            )

            for anterior, actual in zip(
                bloques_ordenados,
                bloques_ordenados[1:]
            ):

                # Si hay un hueco entre dos clases del mismo día
                if anterior["hora_fin"] != actual["hora_inicio"]:
                    penalizacion += 5

    # ==========================================
    # 3. EVITAR DÍAS DEMASIADO CARGADOS
    # ==========================================

    for grupo_id, dias_grupo in bloques_por_grupo.items():

        for dia, bloques in dias_grupo.items():

            horas_del_dia = len(bloques)

            # Más de 4 horas seguidas/en el mismo día
            # genera una pequeña penalización.
            if horas_del_dia > 4:
                penalizacion += (horas_del_dia - 4) * 2

    return penalizacion