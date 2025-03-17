import json
from gestion_reactivos import GestionReactivos
from gestion_experimentos import GestionExperimentos
from gestion_resultados import GestionResultados
from gestion_estadisticas import GestionEstadisticas


"""función PRINCIPAL que gestiona el menú del sistema del laboratorio"""
def main():
    """se inicializan las gestiones"""
    gestion_reactivos = GestionReactivos()
    gestion_experimentos = GestionExperimentos()
    gestion_resultados = GestionResultados()
    gestion_estadisticas = GestionEstadisticas(gestion_experimentos)
    
    """se cargan los datos de los archivos json"""
    while True:
        try:
            gestion_reactivos.cargar_reactivos_json("reactivos.json")
            gestion_experimentos.cargar_experimentos_json("experimentos.json")
            gestion_estadisticas.cargar_datos_json()  # aqui te seguras de que los datos se estan cargando correctamente
            break  # se sale del bucle si la carga es exitosa
        except FileNotFoundError as e:
            print(f"Error: {e}. Asegúrate de que los archivos JSON existan y estén correctamente formateados.")
            respuesta = input("¿Deseas intentar cargar los archivos nuevamente? (s/n): ")
            if respuesta.lower() != 's':
                return
    
    """menú principal"""
    while True:
        print("\nbienvenido al sapulaboratorio, elige la opcion de lo que quieras gestionar: ")
        print("1. gestión de reactivos")
        print("2. gestión de experimentos")
        print("3. gestión de resultados")
        print("4. gestión de estadísticas")
        print("5. salir")
        
        opcion = input("seleccione una opción: ")
        
        if opcion == "1":
            print("\n*gestión de reactivos*")
            gestion_reactivos.menu()
        elif opcion == "2":
            print("\n*gestión de experimentos*")
            gestion_experimentos.menu()
        elif opcion == "3":
            print("\n*gestión de resultados*")
            nombre_experimento = input("ingrese el nombre del experimento que desea evaluar: ")
            gestion_resultados.evaluar_experimento(nombre_experimento)
        elif opcion == "4":
            print("\n*gestión de estadísticas*")
            gestion_estadisticas.mostrar_estadisticas()
            gestion_estadisticas.graficar_estadisticas()
        elif opcion == "5":
            print("saliendo del sistema...")
            break
        else:
            print("opción no válida. Intente nuevamente.")

main()