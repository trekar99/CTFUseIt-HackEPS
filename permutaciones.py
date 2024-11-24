import itertools
import requests
import threading

# Definimos las letras
# HRESADIEOBETR
letras = ['H', 'R', 'E', 'S', 'A', 'D', 'I', 'E', 'O', 'B', 'E', 'T', 'R']

def eliminar_caracteres(string, char_list):
    # Filtramos los caracteres de char_list que no están en la string
    try:
        for i in string:
            char_list.remove(i)
        return char_list
    except Exception as e:
        print("Nombre no apto")
        return []

# URL base
url_base = "https://hackaton2024.useitapps.com/"

# Función que realiza una solicitud HTTP para cada permutación
def realizar_solicitud(name, perm):
    name = name.capitalize()
    permStr = (''.join(perm)).capitalize()
    url = url_base + name + "-" + permStr 
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Request a {url} -> Status: {response.status_code}")
    except Exception as e:
        print(f"Error en la solicitud a {url}: {e}")

# Generamos todas las permutaciones de las letras
name = input('Introduce un nombre: ')

letras = eliminar_caracteres(name.upper(), letras)
if len(letras) != 0:
    permutaciones = itertools.permutations(letras)

    # Creamos una lista de threads para manejar las solicitudes en paralelo
    threads = []

    # Iteramos sobre las permutaciones y creamos un thread para cada solicitud
    for perm in permutaciones:
        thread = threading.Thread(target=realizar_solicitud, args=(name, perm,))
        threads.append(thread)
        thread.start()

    # Esperamos a que todos los threads terminen
    for thread in threads:
        thread.join()
