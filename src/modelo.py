class Clase:
    def __init__(self, asignacion, bloque_id, salon_id):
        self.asignacion_id = asignacion["id"]
        self.materia_id = asignacion["materia_id"]
        self.grupo_id = asignacion["grupo_id"]
        self.profesor_id = asignacion["profesor_id"]
        self.bloque_id = bloque_id
        self.salon_id = salon_id

    def __repr__(self):
        return (
            f"Clase("
            f"asignacion={self.asignacion_id}, "
            f"materia={self.materia_id}, "
            f"grupo={self.grupo_id}, "
            f"profesor={self.profesor_id}, "
            f"bloque={self.bloque_id}, "
            f"salon={self.salon_id}"
            f")"
        )