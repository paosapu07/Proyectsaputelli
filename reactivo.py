"""representa un reactivo químico con sus propiedades y funciones asociadas"""
class Reactivo:
    def __init__(self, id, nombre, descripcion, costo, categoria, inventario_disponible, unidad_medida, fecha_caducidad, minimo_sugerido, conversiones_posibles):
        """inicializa un reactivo con su información básica, inventario y conversiones posibles"""
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.costo = costo
        self.categoria = categoria
        self.inventario_disponible = inventario_disponible
        self.unidad_medida = unidad_medida
        self.fecha_caducidad = fecha_caducidad
        self.minimo_sugerido = minimo_sugerido
        self.conversiones_posibles = conversiones_posibles

    def cambiar_unidad(self, nueva_unidad):
        """convierte el inventario a una nueva unidad de medida si es posible"""
        for conversion in self.conversiones_posibles:
            if conversion['unidad'] == nueva_unidad:
                self.unidad_medida = nueva_unidad
                self.inventario_disponible *= conversion['factor']
                break

    def mostrar_reactivo(self):
        """retorna una descripción detallada del reactivo"""
        return f"nombre: {self.nombre}, descripción: {self.descripcion}, inventario disponible: {self.inventario_disponible} {self.unidad_medida}, costo: ${self.costo}, fecha de caducidad: {self.fecha_caducidad}, mínimo sugerido: {self.minimo_sugerido}"

    def verificar_inventario(self):
        """devuelve True si el inventario está por debajo del mínimo sugerido, False en caso contrario"""
        if self.inventario_disponible < self.minimo_sugerido:
            return True
        return False