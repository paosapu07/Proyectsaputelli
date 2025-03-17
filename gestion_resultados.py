import json
import os
from gestion_reactivos import GestionReactivos
from gestion_experimentos import GestionExperimentos

class GestionResultados:
    def __init__(self):
        """gestiona la evaluación y almacenamiento de resultados de experimentos"""
        self.resultados = []
        self.gestion_experimentos = None 
        self.gestion_reactivos = None 
        self.cargar_datos()
        self.cargar_resultados_json()

    def _try_load_json(self, file_path):
        """intenta cargar un archivo JSON con diferentes codificaciones"""
        encodings = ['utf-8', 'utf-16', 'latin-1']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    return json.load(f)
            except UnicodeDecodeError:
                continue
        """si todas las codificaciones fallan, intentar leer como binario"""
        try:
            with open(file_path, 'rb') as f:
                return json.loads(f.read().decode('utf-8', errors='replace'))
        except Exception as e:
            print(f"error al leer el archivo {file_path}: {str(e)}")
            return None

    def cargar_datos(self):
        """carga los datos de experimentos y reactivos desde archivos json"""
        try:
            datos_experimentos = self._try_load_json(os.path.join("data", "experimentos.json"))
            datos_reactivos = self._try_load_json(os.path.join("data", "reactivos.json"))

            if datos_experimentos is None or datos_reactivos is None:
                raise FileNotFoundError("No se pudo leer uno o más archivos")

            """crear instancias de las clases con los datos cargados"""
            self.gestion_experimentos = GestionExperimentos()
            self.gestion_experimentos.experimentos = datos_experimentos
            self.gestion_reactivos = GestionReactivos()
            self.gestion_reactivos.reactivos = [Reactivo(r["nombre"], r["cantidad"], r["unidad"], r["minimo_sugerido"]) for r in datos_reactivos]

        except FileNotFoundError:
            print("error al cargar los archivos de experimentos o reactivos. Se inicializarán como vacíos")
            self.gestion_experimentos = GestionExperimentos()
            self.gestion_reactivos = GestionReactivos()

    def cargar_resultados_json(self):
        """carga los resultados almacenados en el archivo json"""
        try:
            with open(os.path.join("data", "resultados.json"), "r", encoding="utf-8") as file:
                self.resultados = json.load(file)
        except FileNotFoundError:
            print("archivo de resultados no encontrado. Se creará uno nuevo al guardar")
            self.resultados = []

    def guardar_resultados_json(self):
        """guarda los resultados actuales en un archivo json"""
        with open(os.path.join("data", "resultados.json"), "w", encoding="utf-8") as file:
            json.dump(self.resultados, file, indent=4)

    def evaluar_experimento(self, nombre_experimento):
        """Evalúa un experimento comparando sus resultados con los valores esperados."""
        if self.gestion_experimentos is None or self.gestion_experimentos.experimentos is None:
            print("no hay experimentos cargados")
            return
        
        experimento = next((exp for exp in self.gestion_experimentos.experimentos if exp["nombre"] == nombre_experimento), None)
        
        if not experimento:
            print(f"el experimento '{nombre_experimento}' no existe")
            return

        receta_nombre = experimento.get("receta")
        print(f"evaluando experimento: {nombre_experimento}")  # para debuggear
        print(f"nombre de la receta: {receta_nombre}")

        """cargar recetas desde un archivo JSON"""
        try:
            with open(os.path.join("data", "recetas.json"), "r", encoding="utf-8") as f:
                recetas_data = json.load(f)
        except FileNotFoundError:
            print("archivo de recetas no encontrado")
            return

        print("cargando recetas desde un json...")  # para debuggear

        receta_data = next((r for r in recetas_data if r["nombre"] == receta_nombre), None)
        
        if receta_data is None:
            print(f"no se encontró la receta '{receta_nombre}'.")
            return

        valores_obtenidos = experimento.get("resultado", {})  # para obtener los resultados obtenidos
        print(f"Valores obtenidos: {valores_obtenidos}")  # para debuggear
        valores_esperados = receta_data.get("valores_esperados", {})  # obtiene los valores esperados de la receta

        """comprobacionde cada parametro"""
        evaluacion = {}
        if isinstance(valores_obtenidos, str):
            evaluacion["resultado"] = valores_obtenidos
        else:
            evaluacion = {
                param: valores_obtenidos.get(param, "no registrado") in valores_esperados.get(param, [])
                for param in valores_esperados
            }

        resultado = {
            "experimento": nombre_experimento,
            "evaluacion": evaluacion
        }
        print(f"resultado de evalucion: {resultado}")

        self.resultados.append(resultado)
        self.guardar_resultados_json()