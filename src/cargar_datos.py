# json convierte el contenido de los archivos JSON en listas y diccionarios Python.
import json
# Path ofrece operaciones de rutas portables entre sistemas operativos.
from pathlib import Path


# La ruta se calcula desde este módulo para que los datos se encuentren
# independientemente del directorio desde el que se inicie Python.
# __file__ señala este archivo; parent sube carpetas y / concatena un segmento de ruta.
DATA_DIR = Path(__file__).parent.parent / "data"


def cargar_json(nombre_archivo):
    # Abre cada archivo como UTF-8 para conservar correctamente los textos en español.
    # El operador / de Path une el directorio de datos con el nombre del archivo.
    ruta = DATA_DIR / nombre_archivo

    # with cierra el archivo automáticamente incluso si la lectura produce un error.
    with open(ruta, "r", encoding="utf-8") as archivo:
        # load analiza el texto JSON leído y lo convierte a objetos de Python.
        return json.load(archivo)


def cargar_datos():
    # Centraliza las entidades y catálogos que usan el generador y la evaluación.
    materias = cargar_json("materias.json")
    profesores = cargar_json("profesores.json")
    grupos = cargar_json("grupos.json")
    salones = cargar_json("salones.json")
    asignaciones = cargar_json("asignaciones.json")
    bloques = cargar_json("bloques_horarios.json")

    # Se agrupan todas las colecciones en un solo diccionario de datos.
    return {
        "materias": materias,
        "profesores": profesores,
        "grupos": grupos,
        "salones": salones,
        "asignaciones": asignaciones,
        "bloques": bloques
    }


# Permite usar este módulo como verificación independiente de los archivos de entrada.
if __name__ == "__main__":
    # Ejecutar el módulo directamente muestra un resumen para comprobar la carga.
    datos = cargar_datos()

    print("Datos cargados correctamente.")
    print(f"Materias: {len(datos['materias'])}")
    print(f"Profesores: {len(datos['profesores'])}")
    print(f"Grupos: {len(datos['grupos'])}")
    print(f"Salones: {len(datos['salones'])}")
    print(f"Asignaciones: {len(datos['asignaciones'])}")
    print(f"Bloques horarios: {len(datos['bloques'])}")