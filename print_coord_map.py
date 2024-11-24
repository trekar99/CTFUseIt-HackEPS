import folium
import json

# Función para leer las coordenadas desde el archivo de texto
def leer_coordenadas(archivo):
    coordenadas = []
    with open(archivo, 'r') as file:
        for line in file:
            try:
                # Eliminar el prefijo "b'" y el sufijo "'" (del formato bytes)
                decoded_line = line.strip()[2:-1]  # Eliminar b' y el '
                # Parsear la línea como JSON
                data = json.loads(decoded_line)
                # Extraer las coordenadas x (longitud) y y (latitud)
                lat = data['x']  # Latitud
                lon = data['y']  # Longitud
                coordenadas.append((lat, lon))
            except json.JSONDecodeError:
                print(f"Error al decodificar la línea: {line}")
    return coordenadas

# Crear un mapa centrado en una ubicación general (en este caso, las coordenadas 0,0)
mapa = folium.Map(location=[0, 0], zoom_start=2)

# Leer las coordenadas desde el archivo output.txt
coordenadas = leer_coordenadas('output.txt')

# Añadir un punto plano en el mapa para cada coordenada usando CircleMarker y Popup
for lat, lon in coordenadas:
    folium.CircleMarker(
        location=[lat, lon],  # Ubicación del círculo
        radius=3,  # Radio del círculo (tamaño)
        color='blue',  # Color del borde
        fill=True,  # Relleno de color
        fill_color='blue',  # Color de relleno
        fill_opacity=0.7,  # Opacidad del relleno
        popup=folium.Popup(f"Latitud: {lat}, Longitud: {lon}", parse_html=True)  # Mostrar coordenadas
    ).add_to(mapa)

# Guardar el mapa como un archivo HTML
mapa.save('mapa_interactivo_llano.html')

print("Mapa guardado como 'mapa_interactivo_llano.html'")
