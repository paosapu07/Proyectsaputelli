"""representa una receta química con su objetivo, reactivos y procedimiento"""
class Receta:
    def __init__(self, id, nombre, objetivo, reactivos, procedimiento, valores_esperados):
        """inicializa una receta con su nombre, objetivo, reactivos y valores esperados"""
        self.id = id
        self.nombre = nombre
        self.objetivo = objetivo
        self.reactivos = reactivos   #esto es una lista de reactivos requeridos y sus cantidades
        self.procedimiento = procedimiento
        self.valores_esperados = valores_esperados  # de los experimentos

    def mostrar_receta(self):
        """retorna una descripción detallada de la receta"""
        reactivos_info = "\n".join([f"{r['nombre']} - {r['cantidad']} {r['unidad']}" for r in self.reactivos])
        return f"receta: {self.nombre}\nobjetivo: {self.objetivo}\nreactivos:\n{reactivos_info}\nprocedimiento: {self.procedimiento}\nvalores esperados: {self.valores_esperados}"

    def verificar_reactivos_disponibles(self, gestion_reactivos):
        """comprueba si los reactivos requeridos están disponibles en inventario"""
        for reactivo in self.reactivos:
            reactivo_en_inventario = next((r for r in gestion_reactivos.reactivos if r.nombre == reactivo['nombre']), None)
            if reactivo_en_inventario:
                if reactivo_en_inventario.inventario_disponible < reactivo['cantidad']:
                    return False, f"falta el reactivo {reactivo['nombre']} en la cantidad necesaria"
            else:
                return False, f"el reactivo {reactivo['nombre']} no está disponible en inventario"
        return True, "todos los reactivos están disponibles."
