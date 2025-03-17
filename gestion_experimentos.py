import json
import random
import os
from receta import Receta
from gestion_reactivos import GestionReactivos

class GestionExperimentos:
    """gestiona la creación, modificación y ejecución de experimentos químicos"""
    def __init__(self):
        self.experimentos = []
        self.gestion_reactivos = GestionReactivos()
        self.cargar_experimentos_json("experimentos.json")
    
    def menu(self):
        """muestra el menú de opciones para gestionar experimentos"""
        while True:
            print("\ngestión de experimentos")
            print("1. crear experimento")
            print("2. modificar experimento")
            print("3. eliminar experimento")
            print("4. listar experimentos")
            print("5. volver al menú principal")
            
            opcion = input("seleccione una opción: ")
            
            if opcion == "1":
                self.crear_experimento()
            elif opcion == "2":
                nombre = input("nombre del experimento a modificar: ")
                self.modificar_experimento(nombre)
            elif opcion == "3":
                nombre = input("nombre del experimento a eliminar: ")
                self.eliminar_experimento(nombre)
            elif opcion == "4":
                self.listar_experimentos()
            elif opcion == "5":
                break
            else:
                print("Opción no válida. Intente nuevamente.")
    
    def crear_experimento(self):
        """solicita datos y registra un nuevo experimento"""
        nombre = input("nombre del experimento: ")
        receta = input("nombre de la receta base: ")
        responsables = input("personas responsables: ").split(', ')
        fecha = input("fecha del experimento (YYYY-MM-DD): ")
        
        if not self.validar_reactivos(receta):
            print("no se puede realizar el experimento. Reactivos insuficientes o caducados.")
            return
        
        costo = self.calcular_costo_experimento(receta)
        resultado = input("resultado del experimento: ")
        
        experimento = {
            "nombre": nombre,
            "receta": receta,
            "responsables": responsables,
            "fecha": fecha,
            "costo": costo,
            "resultado": resultado
        }
        
        self.experimentos.append(experimento)
        self.guardar_experimentos_json()
        print("experimento registrado exitosamente!")
    
    def validar_reactivos(self, receta_nombre):
        """verifica si hay suficientes reactivos disponibles para un experimento"""
        with open(os.path.join("data", "recetas.json"), "r", encoding="utf-8") as f:
            recetas = json.load(f)
            receta = next((r for r in recetas if r["nombre"] == receta_nombre), None)
        
        if not receta:
            print("receta no encontrada.")
            return False
        
        for reactivo in receta["reactivos"]:
            nombre = reactivo["nombre"]
            cantidad_necesaria = reactivo["cantidad"]
            reactivo_lab = next((r for r in self.gestion_reactivos.reactivos if r.nombre == nombre), None)
            
            if not reactivo_lab or reactivo_lab.cantidad < cantidad_necesaria:
                return False
        
        self.restar_inventario(receta["reactivos"])
        return True
    
    def restar_inventario(self, reactivos):
        """descuenta del inventario los reactivos usados en un experimento"""
        for reactivo in reactivos:
            nombre = reactivo["nombre"]
            cantidad_necesaria = reactivo["cantidad"]
            reactivo_lab = next((r for r in self.gestion_reactivos.reactivos if r.nombre == nombre), None)
            
            if reactivo_lab:
                error = random.uniform(0.001, 0.225) * cantidad_necesaria
                reactivo_lab.cantidad -= (cantidad_necesaria + error)
                print(f"descontado {cantidad_necesaria + error:.2f} de {nombre} (incluyendo error aleatorio de {error:.2f})")
        
        self.gestion_reactivos.guardar_reactivos_json()
    
    def calcular_costo_experimento(self, receta_nombre):
        """calcula el costo total de un experimento según los reactivos requeridos"""
        with open(os.path.join("data", "recetas.json"), "r", encoding="utf-8") as f:
            recetas = json.load(f)
            receta = next((r for r in recetas if r["nombre"] == receta_nombre), None)
        
        if not receta:
            return 0
        
        costo_total = sum(reactivo["costo"] * reactivo["cantidad"] for reactivo in receta["reactivos"])
        return costo_total
    
    def modificar_experimento(self, nombre):
        """modifica el resultado de un experimento existente"""
        experimento = next((e for e in self.experimentos if e["nombre"] == nombre), None)
        if experimento:
            experimento["resultado"] = input(f"Nuevo resultado ({experimento['resultado']}): ") or experimento["resultado"]
            self.guardar_experimentos_json()
            print("experimento modificado correctamente")
        else:
            print("experimento no encontrado")
    
    def eliminar_experimento(self, nombre):
        """elimina un experimento del registro"""
        self.experimentos = [e for e in self.experimentos if e["nombre"] != nombre]
        self.guardar_experimentos_json()
        print("experimento eliminado correctamente")
    
    def listar_experimentos(self):
        """muestra la lista de experimentos registrados"""
        if not self.experimentos:
            print("no hay experimentos registrados.")
        for experimento in self.experimentos:
            print(experimento)
    
    def cargar_experimentos_json(self, file_path="experimentos.json"):
        """carga los experimentos desde un archivo json"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.experimentos = json.load(f)
                # Validar que los datos contengan la estructura esperada
                if not isinstance(self.experimentos, list) or not all("id" in e and "receta_id" in e and "personas_responsables" in e and "fecha" in e and "costo_asociado" in e and "resultado" in e for e in self.experimentos):
                    raise ValueError("El formato de los datos en experimento.json es incorrecto.")
        except FileNotFoundError:
            print("Archivo de experimentos no encontrado. Se creará uno nuevo al guardar.")
    
    def guardar_experimentos_json(self):
        """guarda los experimentos en un archivo json"""
        with open(os.path.join("data", "experimentos.json"), "w", encoding="utf-8") as f:
            json.dump(self.experimentos, f, indent=4)

    def realizar_experimento(self, experimento_id):
        """ejecuta un experimento verificando reactivos y actualizando el inventario"""
        experimento = next((exp for exp in self.experimentos if exp["id"] == experimento_id), None)
        if not experimento:
            print(f"no se encontró un experimento con ID {experimento_id}")
            return

        receta = self.obtener_receta_por_id(experimento["receta_id"])
        if not receta:
            print(f"no se encontró la receta con ID {experimento['receta_id']}")
            return

        for reactivo in receta.reactivos:
            if not self.gestion_reactivos.verificar_disponibilidad(reactivo["nombre"], reactivo["cantidad"]):
                print(f"No hay suficiente {reactivo['nombre']} en inventario o está vencido.")
                return

            # resta del inventario y simula error de pérdida
        for reactivo in receta.reactivos:
            perdida = reactivo["cantidad"] * random.uniform(0.001, 0.225)  # Entre 0.1% y 22.5%
            cantidad_final = reactivo["cantidad"] + perdida
            self.gestion_reactivos.reducir_inventario(reactivo["nombre"], cantidad_final)

            # actualiza el resultado del experimento (pendiente por el momento)
        experimento["resultado"] = "pendiente"
            
        self.guardar_experimentos_json()
        print(f"experimento ID {experimento_id} realizado usando la fecha {experimento['fecha']}.")

    def obtener_receta_por_id(self, receta_id):
        """obtiene una receta a partir de su ID"""
        try:
            with open(os.path.join("data", "recetas.json"), "r", encoding="utf-8") as f:
                recetas = json.load(f)
            for receta in recetas:
                if receta["id"] == receta_id:
                    return Receta(receta["id"], receta["nombre"], receta["objetivo"], receta["reactivos"], receta["procedimiento"])
        except FileNotFoundError:
            print("no se encontró el archivo de recetas")
        return None