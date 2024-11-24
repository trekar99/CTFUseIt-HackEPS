import easyocr
import time

def getSonets():
    with open('shakespeare_sonnets_dataset.txt', 'r') as f:
        data = f.read().lower()

    # Split sonets from file
    sonets = list(filter(lambda x : x != '', data.split('\n\n')))
    sonets = [sonet.replace('\n', ' ') for sonet in sonets]

    return sonets

def ocrImages(path):

    # Crear un reader
    reader = easyocr.Reader(['en'])  # 'en' para inglés, puedes agregar más idiomas
    
    # Leer la imagen
    result = reader.readtext(path)

    # Imprimir el texto
    for (bbox, text, prob) in result:
        print(text)

inicio = time.time()
(ocrImages('./shakespeare sonnets-01.png'))

# Marca el tiempo después de ejecutar la función
fin = time.time()

# Calcula el tiempo transcurrido
tiempo_total = fin - inicio

print(f"El tiempo de ejecución de la función fue: {tiempo_total} segundos")