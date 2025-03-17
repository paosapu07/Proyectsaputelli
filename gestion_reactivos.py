import json
from reactivo import Reactivo

"""gestiona el inventario de reactivos, permitiendo agregar, modificar y eliminar reactivos"""
class GestionReactivos:
    def __init__(self):
        self.reactivos = []
        self.ultimo_id = 0
    
    def menu(self):
        """muestra el menú de gestión de reactivos y ejecuta la opción seleccionada"""
        while True:
            print("\ngestión de reactivos")
            print("1. agregar reactivo")
            print("2. modificar reactivo")
            print("3. eliminar reactivo")
            print("4. listar reactivos")
            print("5. cambiar unidad de reactivo")
            print("6. volver al menú principal")
            
            opcion = input("seleccione una opción: ")
            
            if opcion == "1":
                self.solicitar_datos_reactivo()
            elif opcion == "2":
                nombre = input("nombre del reactivo a modificar: ")
                self.modificar_reactivo(nombre)
            elif opcion == "3":
                nombre = input("nombre del reactivo a eliminar: ")
                self.eliminar_reactivo(nombre)
            elif opcion == "4":
                self.listar_reactivos()
            elif opcion == "5":
                nombre = input("nombre del reactivo a cambiar unidad: ")
                nueva_unidad = input("nueva unidad: ")
                self.cambiar_unidad_reactivo(nombre, nueva_unidad)
            elif opcion == "6":
                break
            else:
                print("opción no válida. Intente nuevamente.")
    
    def solicitar_datos_reactivo(self):
        """solicita y registra un nuevo reactivo en el inventario"""
        self.ultimo_id += 1
        nombre = input("nombre: ")
        descripcion = input("descripción: ")
        costo = float(input("costo: "))
        categoria = input("categoría: ")
        inventario_disponible = float(input("inventario disponible: "))
        unidad_medida = input("unidad de medida: ")
        fecha_caducidad = input("fecha de caducidad (YYYY-MM-DD): ")
        minimo_sugerido = float(input("mínimo sugerido: "))
        
        conversiones_posibles = []
        if unidad_medida in ["mL", "L", "uL"]:
            conversiones_posibles = [
                {"unidad": "L", "factor": 0.001},
                {"unidad": "uL", "factor": 1000}
            ]
        elif unidad_medida in ["g", "kg", "mg"]:
            conversiones_posibles = [
                {"unidad": "kg", "factor": 0.001},
                {"unidad": "mg", "factor": 1000}
            ]
        
        reactivo = Reactivo(
            self.ultimo_id, nombre, descripcion, costo, categoria,
            inventario_disponible, unidad_medida, fecha_caducidad,
            minimo_sugerido, conversiones_posibles
        )
        self.reactivos.append(reactivo)
        self.verificar_minimo(reactivo)
        self.guardar_reactivos_json()
        print("Reactivo agregado exitosamente.")
    
    def obtener_minimo_sugerido(self, nombre):
        with open("reactivos.json", "r", encoding="utf-8") as f:
            datos = json.load(f)
            for r in datos:
                if r["nombre"] == nombre:
                    return r["minimo_sugerido"]
        return 0  # valor por defecto si no se encuentra
    
    def modificar_reactivo(self, nombre):
        """modifica los datos de un reactivo existente"""
        reactivo = next((r for r in self.reactivos if r.nombre == nombre), None)
        if reactivo:
            print("Ingrese los nuevos valores, o presione Enter para mantener los actuales:")
            
            nuevo_nombre = input(f"Nuevo nombre ({reactivo.nombre}): ") or reactivo.nombre
            nueva_descripcion = input(f"Nueva descripción ({reactivo.descripcion}): ") or reactivo.descripcion
            nuevo_costo = float(input(f"Nuevo costo ({reactivo.costo}): ") or reactivo.costo)
            nueva_categoria = input(f"Nueva categoría ({reactivo.categoria}): ") or reactivo.categoria
            nuevo_inventario = float(input(f"Nuevo inventario ({reactivo.inventario_disponible}): ") or reactivo.inventario_disponible)
            nueva_unidad = input(f"Nueva unidad ({reactivo.unidad_medida}): ") or reactivo.unidad_medida
            nueva_fecha = input(f"Nueva fecha de caducidad ({reactivo.fecha_caducidad}): ") or reactivo.fecha_caducidad
            nuevo_minimo = float(input(f"Nuevo mínimo sugerido ({reactivo.minimo_sugerido}): ") or reactivo.minimo_sugerido)
            
            reactivo.nombre = nuevo_nombre
            reactivo.descripcion = nueva_descripcion
            reactivo.costo = nuevo_costo
            reactivo.categoria = nueva_categoria
            reactivo.inventario_disponible = nuevo_inventario
            reactivo.unidad_medida = nueva_unidad
            reactivo.fecha_caducidad = nueva_fecha
            reactivo.minimo_sugerido = nuevo_minimo
            
            self.verificar_minimo(reactivo)
            self.guardar_reactivos_json()
            print("Reactivo modificado exitosamente.")
        else:
            print("Error: Reactivo no encontrado.")
    
    def eliminar_reactivo(self, nombre):
        """elimina un reactivo del inventario"""
        self.reactivos = [r for r in self.reactivos if r.nombre != nombre]
        self.guardar_reactivos_json()
        print("reactivo eliminado exitosamente!")
    
    def listar_reactivos(self):
        """lista todos los reactivos registrados"""
        if not self.reactivos:
            print("no hay reactivos registrados")
        for reactivo in self.reactivos:
            print(reactivo.mostrar_reactivo())
    
    def cambiar_unidad_reactivo(self, nombre, nueva_unidad):
        """cambia la unidad de medida de un reactivo si es posible"""
        reactivo = next((r for r in self.reactivos if r.nombre == nombre), None)
        if reactivo:
            reactivo.cambiar_unidad(nueva_unidad)
            self.guardar_reactivos_json()
            print(f"unidad de {nombre} cambiada a {nueva_unidad}.")
        else:
            print("reactivo no encontrado.")
    
    def verificar_minimo(self, reactivo):
        if reactivo.inventario_disponible <= reactivo.minimo_sugerido:
            print(f"¡OJO! el reactivo {reactivo.nombre} ha alcanzado su mínimo sugerido. Es necesario reponerlo")
    
    def cargar_reactivos_json(self, file_path):
        """carga reactivos desde un archivo json"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                datos = json.load(f)
                # Validar que los datos contengan la estructura esperada
                campos_requeridos = ["id", "nombre", "descripcion", "costo", "categoria", 
                                   "inventario_disponible", "unidad_medida", "fecha_caducidad", 
                                   "minimo_sugerido", "conversiones_posibles"]
                
                if not isinstance(datos, list) or not all(all(campo in r for campo in campos_requeridos) for r in datos):
                    raise ValueError("El formato de los datos en reactivos.json es incorrecto.")
                
                self.reactivos = [
                    Reactivo(
                        r["id"], r["nombre"], r["descripcion"], r["costo"], 
                        r["categoria"], r["inventario_disponible"], r["unidad_medida"], 
                        r["fecha_caducidad"], r["minimo_sugerido"], r["conversiones_posibles"]
                    ) for r in datos
                ]
                
                # Actualizar el último ID usado
                if self.reactivos:
                    self.ultimo_id = max(r.id for r in self.reactivos)
                
                print("datos de reactivos cargados correctamente")
        except FileNotFoundError:
            print("archivo de reactivos no encontrado. Se creará uno nuevo al guardar")
    
    def verificar_inventario_bajo(self):
        """lista reactivos con inventario por debajo del mínimo sugerido"""
        print("\nreactivos con inventario bajo:")
        for reactivo in self.reactivos:
            if reactivo.inventario_disponible <= reactivo.minimo_sugerido:
                print(f"{reactivo.nombre} - {reactivo.inventario_disponible} {reactivo.unidad_medida} (mínimo sugerido: {reactivo.minimo_sugerido})")

    def guardar_reactivos_json(self):
        """guarda los reactivos en un archivo json"""
        datos = [
            {
                "id": r.id,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "costo": r.costo,
                "categoria": r.categoria,
                "inventario_disponible": r.inventario_disponible,
                "unidad_medida": r.unidad_medida,
                "fecha_caducidad": r.fecha_caducidad,
                "minimo_sugerido": r.minimo_sugerido,
                "conversiones_posibles": r.conversiones_posibles
            }
            for r in self.reactivos
        ]
        with open("reactivos.json", "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4)