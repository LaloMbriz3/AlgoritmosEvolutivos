import random

from deap import base, creator, tools

from src.cargar_datos import cargar_datos
from src.sesiones import crear_sesiones
from src.opciones_horario import obtener_opciones_sesion
from src.evaluacion import evaluar_horario


def preparar_opciones(sesiones, datos):
    opciones_por_sesion = []

    for sesion in sesiones:
        opciones = obtener_opciones_sesion(sesion, datos)

        if not opciones:
            raise ValueError(
                f"No existen opciones válidas para la sesión {sesion['id']}"
            )

        opciones_por_sesion.append(opciones)

    return opciones_por_sesion


def crear_individuo(opciones_por_sesion):
    return [
        random.randrange(len(opciones))
        for opciones in opciones_por_sesion
    ]


def convertir_solucion(individuo, opciones_por_sesion):
    return [
        opciones_por_sesion[i][indice]
        for i, indice in enumerate(individuo)
    ]


def ejecutar_algoritmo(
    datos,
    tam_poblacion=50,
    generaciones=100
):
    sesiones = crear_sesiones(
        datos["asignaciones"],
        datos["materias"]
    )

    opciones_por_sesion = preparar_opciones(
        sesiones,
        datos
    )

    if not hasattr(creator, "FitnessHorario"):
        creator.create(
            "FitnessHorario",
            base.Fitness,
            weights=(-1.0,)
        )

    if not hasattr(creator, "IndividualHorario"):
        creator.create(
            "IndividualHorario",
            list,
            fitness=creator.FitnessHorario
        )

    toolbox = base.Toolbox()

    toolbox.register(
        "individual",
        tools.initIterate,
        creator.IndividualHorario,
        lambda: crear_individuo(opciones_por_sesion)
    )

    toolbox.register(
        "population",
        tools.initRepeat,
        list,
        toolbox.individual
    )

    def evaluar(individuo):
        solucion = convertir_solucion(
            individuo,
            opciones_por_sesion
        )

        penalizacion = evaluar_horario(
            solucion,
            sesiones,
            datos
        )

        return (penalizacion,)

    toolbox.register("evaluate", evaluar)

    toolbox.register(
        "mate",
        tools.cxTwoPoint
    )

    toolbox.register(
        "mutate",
        tools.mutUniformInt,
        low=0,
        up=[
            len(opciones) - 1
            for opciones in opciones_por_sesion
        ],
        indpb=0.05
    )

    toolbox.register(
        "select",
        tools.selTournament,
        tournsize=3
    )

    poblacion = toolbox.population(
        n=tam_poblacion
    )

    for individuo in poblacion:
        individuo.fitness.values = toolbox.evaluate(
            individuo
        )

    for generacion in range(generaciones):

        descendientes = toolbox.select(
            poblacion,
            len(poblacion)
        )

        descendientes = list(
            map(toolbox.clone, descendientes)
        )

        for i in range(
            0,
            len(descendientes) - 1,
            2
        ):
            if random.random() < 0.7:

                toolbox.mate(
                    descendientes[i],
                    descendientes[i + 1]
                )

                del descendientes[i].fitness.values
                del descendientes[i + 1].fitness.values

        for individuo in descendientes:

            if random.random() < 0.2:

                toolbox.mutate(individuo)

                del individuo.fitness.values

        individuos_invalidos = [
            individuo
            for individuo in descendientes
            if not individuo.fitness.valid
        ]

        for individuo in individuos_invalidos:

            individuo.fitness.values = toolbox.evaluate(
                individuo
            )

        poblacion[:] = descendientes

    mejor = tools.selBest(
        poblacion,
        1
    )[0]

    mejor_solucion = convertir_solucion(
        mejor,
        opciones_por_sesion
    )

    mejor_penalizacion = evaluar_horario(
        mejor_solucion,
        sesiones,
        datos
    )

    return {
        "sesiones": sesiones,
        "solucion": mejor_solucion,
        "penalizacion": mejor_penalizacion
    }


def imprimir_horario(resultado, datos):

    bloques_por_id = {
        bloque["id"]: bloque
        for bloque in datos["bloques"]
    }

    materias_por_id = {
        materia["id"]: materia
        for materia in datos["materias"]
    }

    profesores_por_id = {
        profesor["id"]: profesor
        for profesor in datos["profesores"]
    }

    grupos_por_id = {
        grupo["id"]: grupo
        for grupo in datos["grupos"]
    }

    salones_por_id = {
        salon["id"]: salon
        for salon in datos["salones"]
    }

    dias = {
        "Lunes": 0,
        "Martes": 1,
        "Miércoles": 2,
        "Jueves": 3,
        "Viernes": 4
    }

    clases = []

    for sesion, opcion in zip(
        resultado["sesiones"],
        resultado["solucion"]
    ):

        primer_bloque = bloques_por_id[
            opcion["bloques"][0]
        ]

        ultimo_bloque = bloques_por_id[
            opcion["bloques"][-1]
        ]

        clases.append({
            "grupo_id": sesion["grupo_id"],
            "dia": primer_bloque["dia"],
            "hora_inicio": primer_bloque["hora_inicio"],
            "hora_fin": ultimo_bloque["hora_fin"],
            "materia": materias_por_id[
                sesion["materia_id"]
            ]["nombre"],
            "profesor": profesores_por_id[
                sesion["profesor_id"]
            ]["nombre"],
            "salon": salones_por_id[
                opcion["salon_id"]
            ]["nombre"]
        })

    clases.sort(
        key=lambda clase: (
            clase["grupo_id"],
            dias[clase["dia"]],
            clase["hora_inicio"]
        )
    )

    print()
    print("=" * 100)
    print("HORARIO GENERADO")
    print("=" * 100)

    grupo_actual = None

    for clase in clases:

        if clase["grupo_id"] != grupo_actual:

            grupo_actual = clase["grupo_id"]

            print()
            print("-" * 100)
            print(
                f"GRUPO: {grupos_por_id[grupo_actual]['nombre']}"
            )
            print("-" * 100)

        print(
            f"{clase['dia']:10} | "
            f"{clase['hora_inicio']} - {clase['hora_fin']} | "
            f"{clase['materia']:30} | "
            f"{clase['profesor']:20} | "
            f"{clase['salon']}"
        )

    print()
    print("=" * 100)
    print(
        f"Sesiones: {len(resultado['sesiones'])}"
    )
    print(
        f"Penalización final: {resultado['penalizacion']}"
    )
    print("=" * 100)


if __name__ == "__main__":

    datos = cargar_datos()

    resultado = ejecutar_algoritmo(
        datos,
        tam_poblacion=50,
        generaciones=100
    )

    print("Algoritmo terminado.")

    imprimir_horario(
        resultado,
        datos
    )