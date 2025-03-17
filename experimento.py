import random

"""clase de experimento, en la que ticen que de un experimento se conoce lo siguiente: 
receta del experimento, personas responsables, fecha, costo asociado y el resultado"""
class Experimento: 
    def __init__(self, id, receta, personas_responsables, fecha, costo_asociado, resultado):
        self.id = id
        self.receta = receta 
        self.personas_responsables = personas_responsables
        self.fecha = fecha
        self.costo_asociado = costo_asociado
        self.resultado = resultado
        self.error_simulado = 0

    def simular_error(self):
        """genera un error aleatorio en el experimento entre 0.1% y 22.5%."""
        self.error_simulado = random.uniform(0.1, 22.5)

    def calcular_costo(self):
        """retorna el costo total del experimento tomando en cuenta el error simulado"""
        return self.costo_asociado + self.error_simulado

    def realizar_experimento(self, gestion_reactivos):
        """ejecuta el experimento, verificando reactivos y aplicando el error"""
        validacion, mensaje = self.receta.verificar_reactivos_disponibles(gestion_reactivos)
        if not validacion:
            return mensaje

        self.simular_error()

        """aqui descuenta los reactivos del inventario"""
        for reactivo in self.receta.reactivos:
            reactivo_en_inventario = next((r for r in gestion_reactivos.reactivos if r.nombre == reactivo['nombre']), None)
            if reactivo_en_inventario:
                reactivo_en_inventario.inventario_disponible -= reactivo['cantidad']
                """ajuste del inventario por error simulado"""
                reactivo_en_inventario.inventario_disponible -= (reactivo['cantidad'] * self.error_simulado / 100)

        """aqui se guardan los resultados"""
        return f"experimento realizado con éxito. Costo: ${self.calcular_costo()}"

    """retorna los detalles del experimento en formato de texto"""
    def mostrar_experimento(self):
        return f"experimento ID: {self.id}, receta: {self.receta.nombre}, fecha: {self.fecha}, costo asociado: ${self.costo_asociado}, resultado: {self.resultado}"
