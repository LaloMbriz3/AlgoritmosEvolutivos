def obtener_bloque_por_id(bloques):
    """Crea un diccionario que permite buscar bloques mediante su ID."""
    # Crea un índice para resolver un bloque por su identificador.
    # La expresión antes de for es la clave y el objeto completo es el valor.
    return {bloque["id"]: bloque for bloque in bloques}


def obtener_grupo_por_id(grupos):
    """Crea un diccionario que permite buscar grupos mediante su ID."""
    # Esta comprensión sigue el mismo patrón: indexa registros por su campo id.
    return {grupo["id"]: grupo for grupo in grupos}


def obtener_profesor_por_id(profesores):
    """Crea un diccionario que permite buscar profesores mediante su ID."""
    # Las claves únicas simplifican la búsqueda del profesor asignado a una sesión.
    return {profesor["id"]: profesor for profesor in profesores}


def obtener_salon_por_id(salones):
    """Crea un diccionario que permite buscar salones mediante su ID."""
    # Evita recorrer toda la lista cuando se necesita recuperar un salón concreto.
    return {salon["id"]: salon for salon in salones}


def bloque_permitido(bloque, grupo, profesor):
    """Indica si el bloque coincide con la disponibilidad y el turno asignados."""
    # El bloque debe coincidir con la disponibilidad diaria del profesor
    # y quedar completamente dentro del turno del grupo.
    dia = bloque["dia"]

    # in comprueba pertenencia a la lista de días disponibles.
    if dia not in profesor["disponibilidad"]:
        return False

    if bloque["hora_inicio"] < grupo["hora_inicio"]:
        return False

    if bloque["hora_fin"] > grupo["hora_fin"]:
        return False

    return True


def salon_permitido(salon, grupo):
    """Indica si la capacidad del salón alcanza para todos los alumnos del grupo."""
    # Solo se consideran espacios con capacidad suficiente para el grupo.
    # La comparación booleana devuelve directamente True o False.
    return salon["capacidad"] >= grupo["cantidad_alumnos"]


def obtener_opciones_sesion(sesion, datos):
    """Enumera las combinaciones válidas de bloque o bloques y salón para una sesión."""
    # Prepara índices y referencias para filtrar bloques y salones candidatos.
    bloques = datos["bloques"]
    # La llamada a cada helper transforma listas de entidades en índices por ID.
    grupos = obtener_grupo_por_id(datos["grupos"])
    profesores = obtener_profesor_por_id(datos["profesores"])
    salones = datos["salones"]

    grupo = grupos[sesion["grupo_id"]]
    profesor = profesores[sesion["profesor_id"]]

    opciones = []

    # enumerate entrega tanto el índice como el bloque para poder buscar el siguiente.
    for i, bloque in enumerate(bloques):

        if not bloque_permitido(bloque, grupo, profesor):
            continue

        # Una sesión de una hora ocupa un bloque; las de dos horas requieren
        # dos bloques contiguos del mismo día.
        if sesion["duracion"] == 1:
            bloques_sesion = [bloque]

        else:
            # La condición evita indexar una posición que no existe al final de la lista.
            if i + 1 >= len(bloques):
                continue

            siguiente = bloques[i + 1]

            if (
                bloque["dia"] != siguiente["dia"]
                # or exige descartar el par si cambia el día o si las horas no empatan.
                or bloque["hora_fin"] != siguiente["hora_inicio"]
            ):
                continue

            if not bloque_permitido(siguiente, grupo, profesor):
                continue

            bloques_sesion = [bloque, siguiente]

        # Cada combinación válida de bloques se empareja con cada salón apto.
        for salon in salones:
            if salon_permitido(salon, grupo):
                # Cada opción es un diccionario que conserva IDs, no copias de los objetos.
                opciones.append({
                    # Esta comprensión reduce los bloques elegidos a una lista de IDs.
                    "bloques": [b["id"] for b in bloques_sesion],
                    "salon_id": salon["id"]
                })

    return opciones