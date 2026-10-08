def evaluar_horario(solucion, sesiones, datos):
    """Calcula penalizaciones por conflictos y preferencias del horario.

    Args:
        solucion: Opción asignada a cada sesión.
        sesiones: Sesiones académicas asociadas a las opciones.
        datos: Catálogos, incluyendo los bloques horarios.

    Returns:
        La penalización total; los valores menores representan mejores horarios.
    """
    # Una penalización menor representa un horario preferible para el algoritmo.
    penalizacion = 0

    # set almacena claves únicas y permite comprobar pertenencia rápidamente.
    grupos_ocupados = set()
    profesores_ocupados = set()
    salones_ocupados = set()

    # Esta comprensión indexa los bloques para resolver cada ID en tiempo constante.
    bloques_por_id = {
        bloque["id"]: bloque
        for bloque in datos["bloques"]
    }

    # ==========================================
    # 1. RESTRICCIONES DURAS
    # ==========================================

    # Registra la ocupación por recurso y bloque para detectar empalmes.
    # zip combina por posición las sesiones con las opciones elegidas para cada una.
    for sesion, opcion in zip(sesiones, solucion):

        grupo_id = sesion["grupo_id"]
        profesor_id = sesion["profesor_id"]

        for bloque_id in opcion["bloques"]:

            # Las tuplas forman claves compuestas que identifican recurso y bloque.
            clave_grupo = (grupo_id, bloque_id)
            clave_profesor = (profesor_id, bloque_id)
            clave_salon = (opcion["salon_id"], bloque_id)

            # Los conflictos duros reciben un peso alto para desalentarlos.
            # Un grupo no puede tener dos clases al mismo tiempo.
            if clave_grupo in grupos_ocupados:
                penalizacion += 1000

            # Un profesor no puede impartir dos clases al mismo tiempo
            if clave_profesor in profesores_ocupados:
                penalizacion += 1000

            # Un salón no puede tener dos clases al mismo tiempo
            if clave_salon in salones_ocupados:
                penalizacion += 1000

            # add registra la clave; las comprobaciones siguientes detectan repeticiones.
            grupos_ocupados.add(clave_grupo)
            profesores_ocupados.add(clave_profesor)
            salones_ocupados.add(clave_salon)

    # ==========================================
    # 2. REDUCIR HUECOS EN EL HORARIO
    # ==========================================

    # Agrupa bloques por grupo y día para medir huecos y carga diaria.
    bloques_por_grupo = {}

    for sesion, opcion in zip(sesiones, solucion):

        grupo_id = sesion["grupo_id"]

        # Inicializa el diccionario interno solo la primera vez que aparece el grupo.
        if grupo_id not in bloques_por_grupo:
            bloques_por_grupo[grupo_id] = {}

        for bloque_id in opcion["bloques"]:

            bloque = bloques_por_id[bloque_id]

            dia = bloque["dia"]

            # Cada valor interno es una lista de bloques ocupados para un día.
            if dia not in bloques_por_grupo[grupo_id]:
                bloques_por_grupo[grupo_id][dia] = []

            bloques_por_grupo[grupo_id][dia].append(bloque)

    # El mapa mantiene explícito el orden de días usado en el calendario.
    dias = {
        "Lunes": 0,
        "Martes": 1,
        "Miércoles": 2,
        "Jueves": 3,
        "Viernes": 4
    }

    for grupo_id, dias_grupo in bloques_por_grupo.items():

        for dia, bloques in dias_grupo.items():

            # sorted crea una lista ordenada; key indica qué campo compara.
            bloques_ordenados = sorted(
                bloques,
                key=lambda bloque: bloque["hora_inicio"]
            )

            # La lista desplazada una posición permite comparar pares consecutivos.
            for anterior, actual in zip(
                bloques_ordenados,
                bloques_ordenados[1:]
            ):

                # Penaliza cada discontinuidad entre clases consecutivas del día.
                if anterior["hora_fin"] != actual["hora_inicio"]:
                    penalizacion += 5

    # ==========================================
    # 3. EVITAR DÍAS DEMASIADO CARGADOS
    # ==========================================

    for grupo_id, dias_grupo in bloques_por_grupo.items():

        for dia, bloques in dias_grupo.items():

            # La duración se mide contando bloques ocupados ese día.
            horas_del_dia = len(bloques)

            # Más de 4 horas seguidas/en el mismo día
            # genera una pequeña penalización.
            if horas_del_dia > 4:
                penalizacion += (horas_del_dia - 4) * 2

    return penalizacion