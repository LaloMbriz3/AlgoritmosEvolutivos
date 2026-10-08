# Flask aporta la aplicación web y las funciones que generan respuestas HTML y JSON.
from flask import Flask, render_template, jsonify

# Las importaciones desde src reutilizan la carga de datos y el algoritmo del proyecto.
from src.cargar_datos import cargar_datos
from src.algoritmo import ejecutar_algoritmo


# __name__ permite a Flask localizar los recursos relativos de esta aplicación.
app = Flask(__name__)


def generar_horario():
    """Genera una solución evolutiva y prepara sus datos para la interfaz web."""

    # Cada petición vuelve a leer los datos y ejecuta una nueva búsqueda evolutiva.
    datos = cargar_datos()

    resultado = ejecutar_algoritmo(
        datos,
        tam_poblacion=50,
        generaciones=100
    )

    # Una comprensión de diccionario {clave: valor for ...} crea índices por ID.
    # Los diccionarios permiten traducir rápidamente los identificadores
    # de la solución a los registros que se mostrarán en pantalla.
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

    clases = []

    # Convierte cada decisión del algoritmo a una clase legible para la interfaz.
    # zip recorre ambas listas en paralelo: la sesión y la opción elegida para ella.
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

        # Los corchetes consultan claves del diccionario; append añade este nuevo registro.
        clases.append({
            "grupo_id": sesion["grupo_id"],

            "grupo": grupos_por_id[
                sesion["grupo_id"]
            ]["nombre"],

            "dia": primer_bloque["dia"],

            "hora_inicio": primer_bloque[
                "hora_inicio"
            ],

            "hora_fin": ultimo_bloque[
                "hora_fin"
            ],

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

    # Este orden cronológico se usa para ordenar las clases en el resultado.
    dias = {
        "Lunes": 0,
        "Martes": 1,
        "Miércoles": 2,
        "Jueves": 3,
        "Viernes": 4
    }

    # key recibe una función; la tupla define criterios sucesivos de ordenamiento.
    clases.sort(
        key=lambda clase: (
            clase["grupo_id"],
            dias[clase["dia"]],
            clase["hora_inicio"]
        )
    )

    # El diccionario de salida reúne los datos que necesitan la plantilla y el cliente.
    return {
        "clases": clases,
        "penalizacion": resultado["penalizacion"],
        "sesiones": len(resultado["sesiones"]),
        "grupos": [
            {
                "id": grupo["id"],
                "nombre": grupo["nombre"]
            }
            # La comprensión de lista transforma cada grupo al formato mínimo de la UI.
            for grupo in datos["grupos"]
        ]
    }


# El decorador registra la función como manejador de una ruta HTTP.
@app.route("/")
def inicio():
    """Renderiza la página inicial con un horario y sus estadísticas."""

    # La página inicial presenta el primer horario junto con sus estadísticas.
    resultado = generar_horario()

    # Los argumentos nombrados quedan disponibles como variables Jinja en el HTML.
    return render_template(
        "index.html",
        clases=resultado["clases"],
        penalizacion=resultado["penalizacion"],
        sesiones=resultado["sesiones"],
        grupos=resultado["grupos"]
    )


# Esta ruta devuelve datos para que JavaScript actualice la página sin recargarla.
@app.route("/generar")
def generar():
    """Genera otro horario y lo devuelve como respuesta JSON."""

    # El navegador consume este endpoint para solicitar un horario nuevo sin recargar.
    resultado = generar_horario()

    # jsonify serializa el diccionario Python como una respuesta HTTP JSON.
    return jsonify(resultado)


# Esta condición evita iniciar el servidor cuando app.py se importa desde otro módulo.
if __name__ == "__main__":

    app.run(
        debug=True
    )