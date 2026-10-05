class Clase:
    """Representa una clase asignada a un bloque horario y un salón."""

    # __init__ es el inicializador llamado al crear una instancia de Clase.
    def __init__(self, asignacion, bloque_id, salon_id):
        # Conserva las relaciones mediante identificadores, no copias completas
        # de las entidades de los archivos JSON.
        # self identifica el objeto actual; sus atributos quedan disponibles en la instancia.
        self.asignacion_id = asignacion["id"]
        self.materia_id = asignacion["materia_id"]
        self.grupo_id = asignacion["grupo_id"]
        self.profesor_id = asignacion["profesor_id"]
        self.bloque_id = bloque_id
        self.salon_id = salon_id

    # Python usa __repr__ para obtener una representación textual de depuración.
    def __repr__(self):
        # Devuelve una representación compacta útil durante la depuración.
        return (
            # Las f-strings interpolan atributos; los literales adyacentes se concatenan.
            f"Clase("
            f"asignacion={self.asignacion_id}, "
            f"materia={self.materia_id}, "
            f"grupo={self.grupo_id}, "
            f"profesor={self.profesor_id}, "
            f"bloque={self.bloque_id}, "
            f"salon={self.salon_id}"
            f")"
        )