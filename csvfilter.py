import pandas as pd
import requests

def getDF(path):
  dfs = []
  for chunk in pd.read_csv(path, chunksize=1000, encoding='utf8', engine='python'):
      dfs.append(chunk)
  return pd.concat(dfs)

def hacer_requests(url_base, numeros):
    # Lista para almacenar las respuestas de las solicitudes
    urls = []
    
    # Iterar sobre la lista de números
    for numero in numeros:
        # Construir la URL final concatenando la URL base y el número
        url = f"{url_base}{numero}"
        
        try:
            # Realizar la solicitud GET
            respuesta = requests.get(url)
            
            # Verificar si la solicitud fue exitosa (código de estado 200)
            if respuesta.status_code == 200:
                print(url)
                urls.append(url)  # Almacenar el contenido de la respuesta
        except requests.exceptions.RequestException as e:
            # En caso de error en la solicitud
            print(f"Excepción en la solicitud para {url}: {e}")
    
    return urls

df = getDF('./data.csv')

# Condiciones
# KidsNumers = 2 & CityOfResidence = Bangkok
df = df[(df['KidsNumber'] == 2) & (df['CityOfResidence'] =='กรุงเทพมหานคร')]

# Lista de Ids
id_list = df.index.tolist()

# URL base
url_base = "https://hackaton2024.useitapps.com/"

urls = hacer_requests(url_base, id_list)
# print(urls)