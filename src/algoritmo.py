# random genera elecciones probabilísticas para crear y modificar individuos.
import random

# base, creator y tools son módulos de DEAP para definir y operar el algoritmo genético.
from deap import base, creator, tools

from src.cargar_datos import cargar_datos
from src.sesiones import crear_sesiones
from src.opciones_horario import obtener_opciones_sesion
from src.evaluacion import evaluar_horario


def preparar_opciones(sesiones, datos):
    """Calcula las alternativas válidas para cada sesión.

    Args:
        sesiones: Sesiones que deben programarse.
        datos: Catálogos de grupos, profesores, salones y bloques horarios.

    Returns:
        Una lista de opciones por sesión.

    Raises:
        ValueError: Si alguna sesión no tiene opciones válidas.
    """
    # Cada gen necesita al menos una alternativa válida para cada sesión.
    opciones_por_sesion = []

    for sesion in sesiones:
        opciones = obtener_opciones_sesion(sesion, datos)

        # Una excepción detiene el proceso con el identificador que no pudo ubicarse.
        if not opciones:
            raise ValueError(
                f"No existen opciones válidas para la sesión {sesion['id']}"
            )

        opciones_por_sesion.append(opciones)

    return opciones_por_sesion


def crear_individuo(opciones_por_sesion):
    """Crea un cromosoma eligiendo una opción al azar para cada sesión."""
    # El cromosoma guarda un índice: uno por sesión, apuntando a su alternativa.
    # La comprensión de lista produce un gen por sesión y randrange elige un índice válido.
    return [
        random.randrange(len(opciones))
        for opciones in opciones_por_sesion
    ]


def convertir_solucion(individuo, opciones_por_sesion):
    """Convierte los índices de un cromosoma en opciones de horario completas."""
    # Traduce los índices del cromosoma a bloques horarios y salones concretos.
    # enumerate entrega a la vez la posición y el gen; esa posición identifica la sesión.
    return [
        opciones_por_sesion[i][indice]
        for i, indice in enumerate(individuo)
    ]


def ejecutar_algoritmo(
    datos,
    tam_poblacion=50,
    generaciones=100
):
    """Busca una asignación de horarios con penalización baja usando DEAP.

    Args:
        datos: Datos cargados de materias, grupos, profesores, espacios y bloques.
        tam_poblacion: Cantidad de individuos que forman cada población.
        generaciones: Número de iteraciones evolutivas que se ejecutan.

    Returns:
        Un diccionario con las sesiones, la mejor solución y su penalización.
    """
    # Primero se convierte la carga semanal de cada asignación en sesiones atómicas.
    sesiones = crear_sesiones(
        datos["asignaciones"],
        datos["materias"]
    )

    opciones_por_sesion = preparar_opciones(
        sesiones,
        datos
    )

    # DEAP registra estos tipos globalmente; comprobarlos evita redefinirlos
    # cuando se generan varios horarios dentro del mismo proceso Flask.
    # hasattr consulta si el tipo ya existe en el registro global de DEAP.
    if not hasattr(creator, "FitnessHorario"):
        creator.create(
            "FitnessHorario",
            base.Fitness,
            # DEAP expresa la aptitud como tupla; un peso negativo indica minimización.
            weights=(-1.0,)
        )

    if not hasattr(creator, "IndividualHorario"):
        creator.create(
            "IndividualHorario",
            list,
            fitness=creator.FitnessHorario
        )

    toolbox = base.Toolbox()

    # register asocia un nombre operativo con la función que DEAP ejecutará después.
    toolbox.register(
        "individual",
        tools.initIterate,
        creator.IndividualHorario,
        # lambda define aquí una función breve sin argumentos que captura las opciones.
        lambda: crear_individuo(opciones_por_sesion)
    )

    toolbox.register(
        "population",
        tools.initRepeat,
        list,
        toolbox.individual
    )

    def evaluar(individuo):
        """Calcula la penalización del horario representado por un individuo."""
        # DEAP espera una tupla de aptitud; el peso negativo indica que se minimiza.
        solucion = convertir_solucion(
            individuo,
            opciones_por_sesion
        )

        penalizacion = evaluar_horario(
            solucion,
            sesiones,
            datos
        )

        # La coma convierte el valor en tupla de un elemento, formato requerido por DEAP.
        return (penalizacion,)

    toolbox.register("evaluate", evaluar)

    # Configura las operaciones evolutivas aplicadas a los cromosomas.
    toolbox.register(
        "mate",
        tools.cxTwoPoint
    )

    toolbox.register(
        "mutate",
        tools.mutUniformInt,
        low=0,
        # up recibe el máximo inclusivo permitido para cada gen, según sus opciones.
        up=[
            len(opciones) - 1
            for opciones in opciones_por_sesion
        ],
        # indpb es la probabilidad de mutar individualmente cada gen.
        indpb=0.05
    )

    toolbox.register(
        "select",
        tools.selTournament,
        tournsize=3
    )

    # Construye y evalúa la población inicial antes de iniciar las generaciones.
    poblacion = toolbox.population(
        n=tam_poblacion
    )

    # Asigna a cada individuo su aptitud antes de compararlo durante la selección.
    for individuo in poblacion:
        individuo.fitness.values = toolbox.evaluate(
            individuo
        )

    # range produce los índices de generación desde cero hasta generaciones - 1.
    for generacion in range(generaciones):

        # Selección por torneo y copia para que las modificaciones no alteren
        # los individuos originales de la población actual.
        descendientes = toolbox.select(
            poblacion,
            len(poblacion)
        )

        # map aplica clone a cada seleccionado; list materializa el iterador resultante.
        descendientes = list(
            map(toolbox.clone, descendientes)
        )

        # range(start, stop, step) recorre pares sin salir del límite de la lista.
        for i in range(
            0,
            len(descendientes) - 1,
            2
        ):
            # random.random devuelve un valor entre 0 y 1 para decidir si se cruza el par.
            if random.random() < 0.7:

                toolbox.mate(
                    descendientes[i],
                    descendientes[i + 1]
                )

                # del elimina la aptitud almacenada porque el cruce cambió los genes.
                del descendientes[i].fitness.values
                del descendientes[i + 1].fitness.values

        for individuo in descendientes:

            # La comparación con 0.2 aplica la probabilidad de mutación configurada.
            if random.random() < 0.2:

                toolbox.mutate(individuo)

                del individuo.fitness.values

        # Solo se recalcula la aptitud de individuos que cambiaron por cruza o mutación.
        # Esta comprensión filtra los descendientes cuya aptitud quedó invalidada.
        individuos_invalidos = [
            individuo
            for individuo in descendientes
            if not individuo.fitness.valid
        ]

        for individuo in individuos_invalidos:

            individuo.fitness.values = toolbox.evaluate(
                individuo
            )

        # La asignación a [:] reemplaza el contenido sin cambiar el objeto lista original.
        poblacion[:] = descendientes

    # Selecciona el mejor individuo de la última población y materializa su solución.
    # selBest retorna una lista ordenada; [0] toma el individuo de mejor aptitud.
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

    # Devuelve un diccionario con claves nombradas para que los llamadores lean el resultado.
    return {
        "sesiones": sesiones,
        "solucion": mejor_solucion,
        "penalizacion": mejor_penalizacion
    }


def imprimir_horario(resultado, datos):
    """Imprime en consola la solución ordenada y un resumen de su penalización."""

    # Prepara índices para resolver las referencias de la solución al imprimirla.
    # Estas comprensiones de diccionario convierten catálogos en índices de consulta directa.
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

    # Forma registros completos para ordenarlos y agruparlos por grupo.
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

    # Una tupla como clave ordena primero por grupo, luego por día y finalmente por hora.
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
            # Los especificadores :10 y :30 reservan ancho para alinear columnas de texto.
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


# El bloque solo se ejecuta al lanzar este archivo, no al importarlo desde Flask.
if __name__ == "__main__":

    # Permite ejecutar el algoritmo directamente desde la consola para inspección.
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