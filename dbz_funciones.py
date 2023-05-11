import re
import random
import datetime
import json

def traer_datos(path:str)->list:
    """ 
    Brief: recibe un string con el directorio del  archivo .csv, lo convierte en una lista de diccionarios con sus respectivas keys y valores, luego la retorna
    Parameters:
        path -> string con la dirección y nombre del archivo que se transformara en lista
    Return: regresa una lista formada de diccionarios con la información contenida en el archivo
    """
    with open(path,"r", encoding="utf-8") as mi_archivo:
        lista = []
        for line in mi_archivo:
            personaje = {}
            lectura_datos = re.split(r",", line)
            personaje["Id"] = lectura_datos[0]
            personaje["Nombre"] = lectura_datos[1]
            if re.search(r"-H", lectura_datos[2]):                
                razas = lectura_datos[2].split("-")
                personaje["Raza"] = razas
            else:          
                personaje["Raza"] = lectura_datos[2].strip()
            personaje["Poder de pelea"] = lectura_datos[3]
            personaje["Poder de ataque"] = lectura_datos[4]
            habilidades_divididas = re.split(r"\|\$\%", lectura_datos[5])
            for i in range(len(habilidades_divididas)):
                habilidades_divididas[i] = habilidades_divididas[i].strip()
            personaje["Habilidades"] = habilidades_divididas
            lista.append(personaje)

    print("Colección creada con éxito")

    return lista

def mostrar_diccionario(razas:dict,tipo:str):    
    """ 
    Brief: recibe un diccionario y un string con el formato indicado para mostrar su contenido
    Parameters:
        razas -> diccionario que se recorrerá para mostrar sus keys y valores
        tipo -> string que indicará la forma en la que se mostrará el diccionario
    Return: -
    """
    if len(razas) == 0 or not type(razas) == dict or (tipo != "numeros" and tipo != "listas"):
        print("Diccionario vacío o tipo de dato inválido")
        return False
    
    if tipo == "listas":
        for raza in razas:
            print(f"| --- {raza} --- |")
            for personaje in razas[raza]:
                print(f"Nombre: {personaje['Nombre']} - Poder de ataque: {personaje['Poder de ataque']}")
    else:        
        for raza,valores in razas.items():
            print(f"{raza}: {valores}")

def generar_diccionario_razas(lista:list,valores:str)->dict:
    """ 
    Brief: recibe una lista para generar un diccionario y un string para determinar que valores tendrán las keys
    Parameters:
        lista -> lista de personajes para leer y transformar en diccionario
        valores -> string que indicará si las keys tendrás como valor un numero 0 o una lista vacía
    Return: regresa un diccionario conformado por la lista y con los valores indicados
    """
    if len(lista) == 0 or not type(lista) == list or (valores != "ceros" and valores != "listas"):
        print("La lista está vacía o tipo de dato inválido")
        return False
    
    razas_total = []

    for personaje in lista:
        if type(personaje["Raza"]) == list:
            for raza in personaje["Raza"]:
                razas_total.append(raza)
        else:
            razas_total.append(personaje["Raza"])

    razas_unicas = set(razas_total)

    if valores == "ceros":
        razas_unicas = {key: 0 for key in razas_unicas}
    else:
        if valores == "listas":
            razas_unicas = {key: [] for key in razas_unicas}

    return razas_unicas

def cantidad_por_raza(lista:list):
    """ 
    Brief: recibe una lista para generar un diccionario y luego muestra la cantidad de personajes que conforman cada raza
    Parameters:
        lista -> lista de personajes para leer, contar y mostrar las diferentes razas con sus cantidades
    Return: -
    """
    if len(lista) == 0 or not type(lista) == list:
        print("La lista está vacía o tipo de dato inválido")
        return False
    
    razas_unicas = generar_diccionario_razas(lista,"ceros")        

    for personaje in lista:
        if type(personaje["Raza"]) == list:
            for raza in personaje["Raza"]:
                razas_unicas[raza] += 1
        else:
            razas_unicas[personaje["Raza"]] += 1

    mostrar_diccionario(razas_unicas,"numeros")

def personajes_por_raza(lista:list,mostrar:bool=True)->dict:
    """ 
    Brief: recibe una lista para generar un diccionario con keys representando las razas, luego agrega los datos de los personajes que conforman cada una. Recibe opcionalmente un booleano para indicar si se debe mostrar o no por consola
    Parameters:
        lista -> lista para leer y generar un diccionario con las diferentes razas y datos de los personajes que conforman esas razas
        mostrar -> booleano que servirá como parámetro para indicar si se debe o no mostrar la lista
    Return: regresa un diccionario conformado por listas divididas por razas y con información de los personajes que las componen
    """
    if len(lista) == 0 or not type(lista) == list:
        print("La lista está vacía o tipo de dato inválido")
        return False
    
    razas_unicas = generar_diccionario_razas(lista,"listas")

    for personaje in lista:
        personaje_nuevo = {}
        personaje_nuevo["Nombre"] = personaje["Nombre"]
        personaje_nuevo["Poder de ataque"] = personaje["Poder de ataque"]
        personaje_nuevo["Habilidades"] = []
        for habilidad in personaje["Habilidades"]:
            personaje_nuevo["Habilidades"].append(habilidad)

        if type(personaje["Raza"]) == list:
            for raza in personaje["Raza"]:
                razas_unicas[raza].append(personaje_nuevo)
        else:
            razas_unicas[personaje["Raza"]].append(personaje_nuevo)

    if mostrar == True:
        mostrar_diccionario(razas_unicas,"listas")

    return razas_unicas

def personajes_por_habilidad(lista:list,habilidad:str="",mostrar:bool=True)->list:
    """ 
    Brief: recibe una lista para generar otra con diccionarios específicos que representen personajes cuales tengan entre sus habilidades una indicada por el usuario, si no viene especificada en la llamada de la función, pedirá ingresar una cuando sea ejectuada. También recibe un booleano que indicará si se debe o no mostrar el resultado
    Parameters:
        lista -> lista para leer y generar un diccionario con los diferentes personajes que conlleven cierta habilidad especificada por el usuario
        habilidad -> string especificado por el usuario indicando cual habilidad debe buscarse
        mostrar -> booleano que servirá como parámetro para indicar si se debe o no mostrar la lista
    Return: regresa una lista de diccionarios con datos de los personajes que tienen la habilidad buscada
    """
    if len(lista) == 0 or not type(lista) == list:
        print("La lista está vacía o tipo de dato inválido")
        return False
    
    if habilidad == "":
        habilidad = input("Ingrese la habilidad(Ej:Kamehameha, Super Saiyan, Ataque de chocolate): ").strip()
    
    bandera_habilidad = False    
    lista_personajes_habilidad = []

    for personaje in lista:
        for habilidades in personaje["Habilidades"]:
            if habilidades == habilidad:
                bandera_habilidad = True
                nuevo_personaje = {}
                poder_de_ataque = int(personaje["Poder de ataque"])
                poder_de_pelea = int(personaje["Poder de pelea"])
                promedio_poder = (poder_de_ataque + poder_de_pelea) / 2
                nuevo_personaje["Nombre"] = personaje['Nombre']
                nuevo_personaje["Raza"] = personaje["Raza"]
                nuevo_personaje["Promedio de poder"] = promedio_poder
                lista_personajes_habilidad.append(nuevo_personaje)

    if bandera_habilidad == False:
        print(f"No se encontraron personajes con la habilidad: {habilidad}")
        return False
    
    if mostrar == True:
        mostrar_personajes_por_habilidad(lista_personajes_habilidad)
    
    return lista_personajes_habilidad

def mostrar_personajes_por_habilidad(lista:list):
    """ 
    Brief: recibe una lista y la muestra de una manera particular para remarcar los diferentes personajes  que la componen en conjunto con sus datos
    Parameters:
        lista -> lista para leer y mostrar por consola sus diferentes diccionarios de determinada manera
    Return: -
    """
    if len(lista) == 0 or not type(lista) == list:
        print("La lista está vacía o tipo de dato inválido")
        return False
    
    for personaje in lista:
        print("-------------------------------------")
        print(f"Nombre: {personaje['Nombre']}")
        if type(personaje["Raza"]) == list:
            razas = "/".join(personaje['Raza'])
            print(f"Razas: {razas}")
        else:
            print(f"Raza: {personaje['Raza']}")
        print(f"Promedio de poder: {personaje['Promedio de poder']}")
        print("-------------------------------------")

def jugar_batalla(lista:list):
    """ 
    Brief: recibe una lista y muestra el nombre de los personajes que la conforman para que el usuario elija uno, luego se escojerá al azar un contrincante y se procederá a resolver el combate
    Parameters:
        lista -> lista para leer y mostrar por consola los nombres de los personajes que la integran, también se utiliza para generar un enemigo del usuario
    Return: -
    """
    if len(lista) == 0 or not type(lista) == list:
        print("La lista está vacía o tipo de dato inválido")
        return False
    
    bandera_personaje_encontrado = False
    
    for personaje in lista:
        print(personaje["Nombre"])
    
    personaje_jugador = input("Elija su personaje para la batalla: ")

    for personaje in lista:
        if personaje["Nombre"] == personaje_jugador:
            bandera_personaje_encontrado = True
            ataque_personaje_jugador = int(personaje["Poder de ataque"])
            break

    if bandera_personaje_encontrado == False:
        print(f"El personaje '{personaje_jugador}' no fué encontrado")
        return False
    
    enemigo_nombre_ataque = generar_enemigo_pc(lista,personaje_jugador)
    personaje_pc = enemigo_nombre_ataque["Nombre"]
    ataque_personaje_pc = enemigo_nombre_ataque["Poder de ataque"]
    resultado_batalla(personaje_jugador,ataque_personaje_jugador,personaje_pc,ataque_personaje_pc)   

def generar_enemigo_pc(lista:list,pj_jugador:str)->dict:
    """ 
    Brief: recibe una lista para elegir al azar un enemigo que combatirá contra el personaje del jugador, también recibe un string con el nombre que el usuario eligió para evitar que se elija al mismo
    Parameters:
        lista -> lista para recorrer y obtener un enemigo al azar
        pj_jugador -> nombre de personaje que el usuarió ingresó
    Return: regresa un diccionario con el nombre y el poder de ataque del enemigo generado
    """
    indices_personajes = len(lista) - 1
    numero_aleatorio = random.randint(0, indices_personajes)
    personaje_pc = lista[numero_aleatorio]["Nombre"]
    
    while personaje_pc == pj_jugador:
        numero_aleatorio = random.randint(0, indices_personajes)
        personaje_pc = lista[numero_aleatorio]["Nombre"]

    ataque_personaje_pc = int(lista[numero_aleatorio]["Poder de ataque"])
    enemigo_nombre_ataque = {
        "Nombre": personaje_pc,
        "Poder de ataque": ataque_personaje_pc
    }

    return enemigo_nombre_ataque

def resultado_batalla(pj_jugador:str,atq_pj_jugador:int,pj_pc:str,atq_pj_pc:int):
    """ 
    Brief: recibe 2 strings y 2 enteros, representando respectivamente los nombres y poder de ataque del personaje elegido por el usuario y el enemigo generado por el programa. Procesa el resultado del enfrentamiento comparando el poder de ataque de los contrincantes, luego agrega el resultado a un archivo de texto indicando la hora y día que fue dado el combate
    Parameters:
        pj_jugador -> string que representa el nombre del personaje elegido por el usuario
        atq_pj_jugador -> entero que representa el poder de ataque del personaje elegido por el usuario
        pj_pc -> string que representa el nombre del personaje generado por el programa
        atq_pj_pc -> entero que representa el poder de ataque del personaje generado por el programa
    Return: -
    """
    if atq_pj_jugador > atq_pj_pc:
        mensaje_resultado = (f"{pj_jugador} le ganó a {pj_pc}")
    else:
        if atq_pj_jugador < atq_pj_pc:
            mensaje_resultado = (f"{pj_pc} le ganó a {pj_jugador}")
        else:
            mensaje_resultado = (f"La pelea entre {pj_jugador} y {pj_pc} resultó en un empate!")

    print(mensaje_resultado)

    with open("resultados_de_batallas.txt", "a") as file:
        fecha = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        file.write(f"{fecha} - {mensaje_resultado}\n")

def comprobar_raza_habilidad(lista:list,raza_pj:str,habilidad_pj:str)->bool:
    """ 
    Brief: recibe una lista para generar con otras funciones diccionarios y listas de personajes que agrupan información necesaria para la comprobación de datos. A su vez recibe 2 strings indicados por el usuario que representan la raza y la habilidad buscado; en caso de que alguno de los datos no se encuentren registrados, terminará la ejecución indicando el motivo
    Parameters:
        lista -> lista de personajes que se utilizará para las comprobaciones
        raza_pj -> string que se usará para buscar cierta raza en un diccionario de razas
        habilidad_pj -> string que se usará para buscar cierta habilidad en una lista de personajes
    Return: regresa un booleano con el valor True si se superan las comprobaciones o False en caso contrario
    """    
    diccionario_personajes_raza = personajes_por_raza(lista,False)
    if diccionario_personajes_raza == False:
        return False
    
    lista_personajes_habilidad = personajes_por_habilidad(lista,habilidad_pj,False)
    if lista_personajes_habilidad == False:
        print("La habilidad no se encuentra en la lista")
        return False 

    if not raza_pj in diccionario_personajes_raza:
        print("La raza no se encuentra en el diccionario")
        return False
    
    return True

def fomar_datos_json(lista:list,raza_pj:str,habilidad_pj:str)->list:
    """ 
    Brief: recibe una lista y 2 strings para hacer comprobaciones y extraer datos necesarios para generar una lista nueva con información de personajes. Los personajes deben coincidir con la raza y habilidad ingresada por el usuario
    Parameters:
        lista -> lista que se usará para hacer comprobaciones y traer información necesaria 
        raza_pj -> string que indica la raza buscada por el usuario
        habilidad_pj -> string que representa la habilidad buscada por el usuario
    Return: regresa una lista conformada por los datos de los personajes que coinciden con la raza y la habilidad indicada por el usuario
    """
    test = comprobar_raza_habilidad(lista,raza_pj,habilidad_pj)    
    if test == False:
        return False
    
    diccionario_personajes_raza = personajes_por_raza(lista,False)
    lista_personajes_habilidad = personajes_por_habilidad(lista,habilidad_pj,False)    
    lista_datos = []

    for personaje in lista_personajes_habilidad:
        for i in range(len(diccionario_personajes_raza[raza_pj])):
            if diccionario_personajes_raza[raza_pj][i]["Nombre"] == personaje["Nombre"]:
                nombre = diccionario_personajes_raza[raza_pj][i]["Nombre"]
                poder_ataque = diccionario_personajes_raza[raza_pj][i]["Poder de ataque"]
                habilidades = []
                for habilidad in diccionario_personajes_raza[raza_pj][i]["Habilidades"]:
                    if habilidad != habilidad_pj:
                        habilidades.append(habilidad)
                if len(habilidades) == 0 :
                    habilidades = "(sin habilidades extras)"
                else:
                    habilidades = " + ".join(habilidades)
                datos = (f"{nombre} - {poder_ataque} - {habilidades}")
                lista_datos.append(datos)

    if len(lista_datos) == 0:
        print(f"No se encontraron personajes de raza '{raza_pj}' que tengan la habilidad '{habilidad_pj}'")
        return False

    return lista_datos

def guardar_json(lista:list)->str:
    """ 
    Brief: recibe una lista para buscar personajes que contengan una habilidad y raza especificada por el usuario posteriormente. Luego guarda los datos en un archivo .json
    Parameters:
        lista -> lista que se usará para hacer comprobaciones y traer información necesaria        
    Return: regresa un string con el nombre del archivo creado
    """
    raza_pj = input("Ingrese la raza que desea buscar(Ej:Humano, Saiyan): ").strip()
    habilidad_pj = input("Ingrese la habilidad que desea buscar(Ej:Kamehameha, Ataque combinado): ").strip()
    lista_datos = fomar_datos_json(lista,raza_pj,habilidad_pj)
    if lista_datos == False:
        return False
    
    habilidad_pj = re.sub(r" |-","_",habilidad_pj)
    raza_pj = re.sub(r" |-","_",raza_pj)

    with open(f"{raza_pj}_{habilidad_pj}.json","w", encoding="utf-8") as mi_archivo_json:
        json.dump(lista_datos,mi_archivo_json, indent=4, ensure_ascii=False)

    print(f"Datos guardados correctamente como {raza_pj}_{habilidad_pj}.json")
    path = f"{raza_pj}_{habilidad_pj}.json"
    
    return path

def leer_json(path:str):
    """ 
    Brief: recibe un string con el nombre del archivo creado en la funcion guardar_json y lo utiliza para abrirlo y mostrarlo linea a linea por consola
    Parameters:
        path -> string con el nombre del archivo para ser leido
    Return: -
    """
    if path == "" or path == False:
        print("La dirección al archivo está vacía")
        return False

    with open(f"{path}","r", encoding="utf-8") as mi_archivo_json:
        data = json.load(mi_archivo_json)
        for linea in data:
            print(linea)
    
def imprimir_menu():    
    """ 
    Brief: muestra un menú con las diferentes opciones a elegir
    Parameters: -
    Return: -
    """
    print("1 - Importar datos del archivo .csv")
    print("2 - Listar cantidad por raza")
    print("3 - Listar personajes por raza")
    print("4 - Listar personajes por habilidad")
    print("5 - Jugar Batalla")
    print("6 - Guardar Json (ingresando raza y habilidad)")
    print("7 - Leer Json")
    print("8 - Salir del programa")

def dbz_menu_principal():
    """ 
    Brief: imprime un menú, recibe un valor del usuario para dicho menú, puede importar un archivo necesario para las diferentes tareas
    Parameters: -
    Return: -
    """
    lista_personajes = []
    path = ""

    while True:
        imprimir_menu()    
        opcion = input("Ingrese una opción: ")

        match opcion:
            case "1":
                lista_personajes = traer_datos("DBZ.csv")                
            case "2":
                cantidad_por_raza(lista_personajes)
            case "3":
                personajes_por_raza(lista_personajes)
            case "4":
                personajes_por_habilidad(lista_personajes)
            case "5":
                jugar_batalla(lista_personajes)
            case "6":
                path = guardar_json(lista_personajes)
            case "7":
                leer_json(path)
            case "8":
                print("Gracias por usar nuestra aplicación!")
                break  
            case _:
                print("La opción ingresada no es válida")