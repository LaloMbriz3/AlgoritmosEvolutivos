from flask import Flask, render_template, jsonify

from src.cargar_datos import cargar_datos
from src.algoritmo import ejecutar_algoritmo


app = Flask(__name__)


def generar_horario():

    datos = cargar_datos()

    resultado = ejecutar_algoritmo(
        datos,
        tam_poblacion=50,
        generaciones=100
    )

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

    dias = {
        "Lunes": 0,
        "Martes": 1,
        "Miércoles": 2,
        "Jueves": 3,
        "Viernes": 4
    }

    clases.sort(
        key=lambda clase: (
            clase["grupo_id"],
            dias[clase["dia"]],
            clase["hora_inicio"]
        )
    )

    return {
        "clases": clases,
        "penalizacion": resultado["penalizacion"],
        "sesiones": len(resultado["sesiones"]),
        "grupos": [
            {
                "id": grupo["id"],
                "nombre": grupo["nombre"]
            }
            for grupo in datos["grupos"]
        ]
    }


@app.route("/")
def inicio():

    resultado = generar_horario()

    return render_template(
        "index.html",
        clases=resultado["clases"],
        penalizacion=resultado["penalizacion"],
        sesiones=resultado["sesiones"],
        grupos=resultado["grupos"]
    )


@app.route("/generar")
def generar():

    resultado = generar_horario()

    return jsonify(resultado)


if __name__ == "__main__":

    app.run(
        debug=True
    )