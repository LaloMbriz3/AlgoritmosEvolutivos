def obtener_bloque_por_id(bloques):
    return {bloque["id"]: bloque for bloque in bloques}


def obtener_grupo_por_id(grupos):
    return {grupo["id"]: grupo for grupo in grupos}


def obtener_profesor_por_id(profesores):
    return {profesor["id"]: profesor for profesor in profesores}


def obtener_salon_por_id(salones):
    return {salon["id"]: salon for salon in salones}


def bloque_permitido(bloque, grupo, profesor):
    dia = bloque["dia"]

    if dia not in profesor["disponibilidad"]:
        return False

    if bloque["hora_inicio"] < grupo["hora_inicio"]:
        return False

    if bloque["hora_fin"] > grupo["hora_fin"]:
        return False

    return True


def salon_permitido(salon, grupo):
    return salon["capacidad"] >= grupo["cantidad_alumnos"]


def obtener_opciones_sesion(sesion, datos):
    bloques = datos["bloques"]
    grupos = obtener_grupo_por_id(datos["grupos"])
    profesores = obtener_profesor_por_id(datos["profesores"])
    salones = datos["salones"]

    grupo = grupos[sesion["grupo_id"]]
    profesor = profesores[sesion["profesor_id"]]

    opciones = []

    for i, bloque in enumerate(bloques):

        if not bloque_permitido(bloque, grupo, profesor):
            continue

        if sesion["duracion"] == 1:
            bloques_sesion = [bloque]

        else:
            if i + 1 >= len(bloques):
                continue

            siguiente = bloques[i + 1]

            if (
                bloque["dia"] != siguiente["dia"]
                or bloque["hora_fin"] != siguiente["hora_inicio"]
            ):
                continue

            if not bloque_permitido(siguiente, grupo, profesor):
                continue

            bloques_sesion = [bloque, siguiente]

        for salon in salones:
            if salon_permitido(salon, grupo):
                opciones.append({
                    "bloques": [b["id"] for b in bloques_sesion],
                    "salon_id": salon["id"]
                })

    return opciones