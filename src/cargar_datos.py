import json
from pathlib import Path


DATA_DIR = Path(__file__).parent.parent / "data"


def cargar_json(nombre_archivo):
    ruta = DATA_DIR / nombre_archivo

    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def cargar_datos():
    materias = cargar_json("materias.json")
    profesores = cargar_json("profesores.json")
    grupos = cargar_json("grupos.json")
    salones = cargar_json("salones.json")
    asignaciones = cargar_json("asignaciones.json")
    bloques = cargar_json("bloques_horarios.json")

    return {
        "materias": materias,
        "profesores": profesores,
        "grupos": grupos,
        "salones": salones,
        "asignaciones": asignaciones,
        "bloques": bloques
    }


if __name__ == "__main__":
    datos = cargar_datos()

    print("Datos cargados correctamente.")
    print(f"Materias: {len(datos['materias'])}")
    print(f"Profesores: {len(datos['profesores'])}")
    print(f"Grupos: {len(datos['grupos'])}")
    print(f"Salones: {len(datos['salones'])}")
    print(f"Asignaciones: {len(datos['asignaciones'])}")
    print(f"Bloques horarios: {len(datos['bloques'])}")