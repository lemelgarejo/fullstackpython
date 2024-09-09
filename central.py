# Parte 1: Cargar los datos
def cargar_datos(lineas_archivo):
    generos_peliculas = []
    peliculas_por_genero = []
    info_peliculas = []

    # Diccionario temporal para almacenar películas por género
    dict_peliculas_por_genero = {}

    for linea in lineas_archivo:
        # Separar los elementos de cada línea
        titulo, popularidad, voto_promedio, cantidad_votos, generos = linea.split(",")
        generos_lista = generos.split(";")

        # Crear la tupla para info_peliculas
        pelicula_info = (titulo, float(popularidad), float(voto_promedio), int(cantidad_votos), generos_lista)
        info_peliculas.append(pelicula_info)

        # Añadir géneros a la lista de generos_peliculas sin duplicados
        for genero in generos_lista:
            if genero not in generos_peliculas:
                generos_peliculas.append(genero)

            # Añadir película al diccionario por género
            if genero not in dict_peliculas_por_genero:
                dict_peliculas_por_genero[genero] = []
            dict_peliculas_por_genero[genero].append(titulo)

    # Convertir el diccionario en una lista de tuplas
    peliculas_por_genero = [(genero, peliculas) for genero, peliculas in dict_peliculas_por_genero.items()]

    return generos_peliculas, peliculas_por_genero, info_peliculas



# Parte 2: Completar las consultas
def obtener_puntaje_y_votos(nombre_pelicula):
    lineas_archivo = leer_archivo()
    generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(lineas_archivo)

    for pelicula in info_peliculas:
        if pelicula[0].lower() == nombre_pelicula.lower():
            return pelicula[2], pelicula[3]

    return None, None


def filtrar_y_ordenar(genero_pelicula):
    lineas_archivo = leer_archivo()
    generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(lineas_archivo)

    for genero, peliculas in peliculas_por_genero:
        if genero.lower() == genero_pelicula.lower():
            return sorted(peliculas, reverse=True)

    return []


def obtener_estadisticas(genero_pelicula, criterio):
    lineas_archivo = leer_archivo()
    generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(lineas_archivo)

    valores = []
    for pelicula in info_peliculas:
        if genero_pelicula.lower() in [gen.lower() for gen in pelicula[4]]:
            if criterio == "popularidad":
                valores.append(pelicula[1])
            elif criterio == "voto promedio":
                valores.append(pelicula[2])
            elif criterio == "cantidad votos":
                valores.append(pelicula[3])

    if valores:
        maximo = max(valores)
        minimo = min(valores)
        promedio = sum(valores) / len(valores)
        return [maximo, minimo, promedio]

    return [None, None, None]


# NO ES NECESARIO MODIFICAR DESDE AQUI HACIA ABAJO

def solicitar_accion():
    print("\n¿Qué desea hacer?\n")
    print("[0] Revisar estructuras de datos")
    print("[1] Obtener puntaje y votos de una película")
    print("[2] Filtrar y ordenar películas")
    print("[3] Obtener estadísticas de películas")
    print("[4] Salir")

    eleccion = input("\nIndique su elección (0, 1, 2, 3, 4): ")
    while eleccion not in "01234":
        eleccion = input("\nElección no válida.\nIndique su elección (0, 1, 2, 3, 4): ")
    eleccion = int(eleccion)
    return eleccion


def leer_archivo():
    lineas_peliculas = []
    with open("movies.csv", "r", encoding="utf-8") as datos:
        for linea in datos.readlines()[1:]:
            lineas_peliculas.append(linea.strip())
    return lineas_peliculas


def revisar_estructuras(generos_peliculas, peliculas_por_genero, info_peliculas):
    print("\nGéneros de películas:")
    for genero in generos_peliculas:
        print(f"    - {genero}")

    print("\nTítulos de películas por genero:")
    for genero in peliculas_por_genero:
        print(f"    genero: {genero[0]}")
        for titulo in genero[1]:
            print(f"        - {titulo}")

    print("\nInformación de cada película:")
    for pelicula in info_peliculas:
        print(f"    Nombre: {pelicula[0]}")
        print(f"        - Popularidad: {pelicula[1]}")
        print(f"        - Puntaje Promedio: {pelicula[2]}")
        print(f"        - Votos: {pelicula[3]}")
        print(f"        - Géneros: {pelicula[4]}")


def solicitar_nombre():
    nombre = input("\nIngrese el nombre de la película: ")
    return nombre


def solicitar_genero():
    genero = input("\nIndique el género de película: ")
    return genero


def solicitar_genero_y_criterio():
    genero = input("\nIndique el género de película: ")
    criterio = input(
        "\nIndique el criterio (popularidad, voto promedio, cantidad votos): "
    )
    return genero, criterio


def main():
    lineas_archivo = leer_archivo()
    datos_cargados = True
    try:
        generos_peliculas, peliculas_por_genero, info_peliculas = cargar_datos(
            lineas_archivo
        )
    except TypeError as error:
        if "cannot unpack non-iterable NoneType object" in repr(error):
            print(
                "\nTodavía no puedes ejecutar el programa ya que no has cargado los datos\n"
            )
            datos_cargados = False
    if datos_cargados:
        salir = False
        print("\n********** ¡Bienvenid@! **********")
        while not salir:
            accion = solicitar_accion()

            if accion == 0:
                revisar_estructuras(
                    generos_peliculas, peliculas_por_genero, info_peliculas
                )

            elif accion == 1:
                nombre_pelicula = solicitar_nombre()
                ptje, votos = obtener_puntaje_y_votos(nombre_pelicula)
                print(f"\nObteniendo puntaje promedio y votos de {nombre_pelicula}")
                print(f"    - Puntaje promedio: {ptje}")
                print(f"    - Votos: {votos}")

            elif accion == 2:
                genero = solicitar_genero()
                nombres_peliculas = filtrar_y_ordenar(genero)
                print(f"\nNombres de películas del género {genero} ordenados:")
                for nombre in nombres_peliculas:
                    print(f"    - {nombre}")

            elif accion == 3:
                genero, criterio = solicitar_genero_y_criterio()
                estadisticas = obtener_estadisticas(genero, criterio)
                print(f"\nEstadísticas de {criterio} de películas del género {genero}:")
                print(f"    - Máximo: {estadisticas[0]}")
                print(f"    - Mínimo: {estadisticas[1]}")
                print(f"    - Promedio: {estadisticas[2]}")

            else:
                salir = True
        print("\n********** ¡Adiós! **********\n")


if __name__ == "__main__":
    main()
