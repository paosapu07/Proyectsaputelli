import json
import matplotlib.pyplot as plt

"""gestiona la generación y visualización de estadísticas del sapulaboratorio"""
class GestionEstadisticas:
    def __init__(self, gestion_experimentos):
        self.gestion_experimentos = gestion_experimentos
        self.experimentos = []
        self.reactivos = []
        self.resultados = []
        self.cargar_datos_json()

    def cargar_resultados_json(self):
        """carga los datos de resultados desde el archivo json"""
        try:
            with open("resultados.json", "r", encoding="utf-8") as f:
                resultados = json.load(f)
                if not isinstance(resultados, list) or not all("experimento" in r and "resultado" in r for r in resultados):
                    raise ValueError("el formato de los datos en resultados.json es incorrecto.")
                return resultados
        except FileNotFoundError:
            print("archivo de resultados no encontrado.")
            return []

    def cargar_datos_json(self):
        """carga experimentos, reactivos y resultados desde archivos json"""
        try:
            self.resultados = self.cargar_resultados_json()  # cargar y valida los resultados

            with open("experimentos.json", "r", encoding="utf-8") as f:
                self.experimentos = json.load(f)
                """validar que los datos contengan la estructura esperada"""
                if not isinstance(self.experimentos, list) or not all("id" in e and "receta_id" in e and "personas_responsables" in e for e in self.experimentos):
                    raise ValueError("el formato de los datos en experimentos.json es incorrecto")

            with open("reactivos.json", "r", encoding="utf-8") as f:
                self.reactivos = json.load(f)
                """valida que los datos contengan la estructura esperada"""
                if not isinstance(self.reactivos, list) or not all("nombre" in r and "inventario_disponible" in r for r in self.reactivos):
                    raise ValueError("el formato de los datos en reactivos.json es incorrecto")

            print("datos de experimentos y reactivos cargados correctamente")

        except FileNotFoundError as e:
            print(f"error al cargar los archivos: {e}")

    def investigador_mas_activo(self):
        """devuelve el nombre del investigador con más experimentos realizados"""
        investigadores = {}
        for exp in self.gestion_experimentos.experimentos:
            for investigador in exp["personas_responsables"]:
                investigadores[investigador] = investigadores.get(investigador, 0) + 1
        if investigadores:
            return max(investigadores, key=investigadores.get)
        return "no hay datos suficientes"

    def experimento_mas_menos_frecuente(self):
        """devuelve los experimentos más y menos realizados"""
        frecuencia = {}
        for exp in self.gestion_experimentos.experimentos:
            receta_id = exp["receta_id"]
            frecuencia[receta_id] = frecuencia.get(receta_id, 0) + 1
        if frecuencia:
            max_exp = max(frecuencia, key=frecuencia.get)
            min_exp = min(frecuencia, key=frecuencia.get)
            return max_exp, min_exp
        return "no hay datos suficientes", "no hay datos suficientes"

    def obtener_nombre_receta(self, receta_id):
        """obtiene el nombre de una receta dado su ID"""
        try:
            with open("recetas.json", "r", encoding="utf-8") as f:
                recetas = json.load(f)
                receta = next((r for r in recetas if r["id"] == receta_id), None)
                return receta["nombre"] if receta else f"receta {receta_id}"
        except (FileNotFoundError, json.JSONDecodeError):
            return f"receta {receta_id}"

    def obtener_nombre_reactivo(self, reactivo_id):
        """obtiene el nombre de un reactivo dado su ID"""
        reactivo = next((r for r in self.reactivos if r["id"] == reactivo_id), None)
        return reactivo["nombre"] if reactivo else f"reactivo {reactivo_id}"

    def reactivos_mas_usados(self):
        """devuelve una lista de los reactivos más utilizados en experimentos"""
        uso_reactivos = {}
        try:
            with open("recetas.json", "r", encoding="utf-8") as f:
                recetas = json.load(f)
                for exp in self.gestion_experimentos.experimentos:
                    receta = next((r for r in recetas if r["id"] == exp["receta_id"]), None)
                    if receta and "reactivos_utilizados" in receta:
                        for reactivo in receta["reactivos_utilizados"]:
                            if "reactivo_id" in reactivo:
                                nombre_reactivo = self.obtener_nombre_reactivo(reactivo["reactivo_id"])
                                uso_reactivos[nombre_reactivo] = uso_reactivos.get(nombre_reactivo, 0) + 1
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"error al procesar recetas: {e}")
            return []

        """ordenar por frecuencia de uso y obtener los 5 más usados"""
        reactivos_ordenados = sorted(uso_reactivos.items(), key=lambda x: x[1], reverse=True)[:5]
        return [f"{nombre} ({usos} usos)" for nombre, usos in reactivos_ordenados]

    def mostrar_estadisticas(self):
        """muestra estadísticas generales del laboratorio en consola"""
        print("\nestadísticas del laboratorio")
        print(f"investigador más activo: {self.investigador_mas_activo()}")
        max_exp, min_exp = self.experimento_mas_menos_frecuente()
        print(f"experimento más realizado: {self.obtener_nombre_receta(max_exp)} (ID: {max_exp})")
        print(f"experimento menos realizado: {self.obtener_nombre_receta(min_exp)} (ID: {min_exp})")
        print("reactivos más usados:")
        for reactivo in self.reactivos_mas_usados():
            print(f"  - {reactivo}")

    def graficar_estadisticas(self):
        """genera gráficos de los experimentos más y menos frecuentes"""
        exp_max, min_exp = self.experimento_mas_menos_frecuente()
        nombres = [self.obtener_nombre_receta(exp_max), self.obtener_nombre_receta(min_exp)]
        plt.figure(figsize=(10, 6))
        plt.bar(nombres, [1, 0])
        plt.title("experimentos más y menos frecuentes")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
