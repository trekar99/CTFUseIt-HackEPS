import boto3
import base64

# Crear un cliente de Kinesis
kinesis_client = boto3.client('kinesis', region_name='us-west-2')  # Asegúrate de especificar tu región

# Definir el Stream y el ShardId
stream_name = 'info-stream'  # Cambia esto por tu nombre de stream
shard_id = 'shardId-000000000000'  # Cambia esto por tu Shard ID

def obtener_shard_iterator():
    # Obtén un nuevo ShardIterator a partir del primer registro disponible
    response = kinesis_client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType='LATEST'  # 'LATEST' obtiene los últimos registros. Puedes usar 'TRIM_HORIZON' para obtener desde el principio
    )
    return response['ShardIterator']

def obtener_registros(shard_iterator, max_iteraciones=1000):
    iteracion = 0  # Contador de iteraciones

    while shard_iterator and iteracion < max_iteraciones:
        try:
            # Obtener los registros de Kinesis
            response = kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=100  # Ajusta este valor si deseas obtener más o menos registros
            )

            # Abrir el archivo para escribir los datos descodificados
            with open('output.txt', 'a') as file:
                # Recorrer los registros y procesar cada uno
                for record in response['Records']:
                    # Decodificar los datos en base64
                    decoded_data = str(record['Data'])

                    # Escribir los datos descodificados en el archivo
                    file.write(decoded_data + '\n')  # Cada registro en una nueva línea

            # Obtener el siguiente ShardIterator para continuar la lectura
            shard_iterator = response.get('NextShardIterator')
            iteracion += 1  # Incrementar el contador de iteraciones

            # Mensaje informativo
            if shard_iterator:
                print(f"Iteración {iteracion}: Continuando con el siguiente Shard Iterator.")
            else:
                print("No hay más registros para procesar.")
                break

        except kinesis_client.exceptions.ExpiredIteratorException:
            print(f"Iterador caducado, obteniendo uno nuevo. Iteración: {iteracion}")
            shard_iterator = obtener_shard_iterator()  # Obtener un nuevo ShardIterator

        if iteracion >= max_iteraciones:
            print(f"Se alcanzó el límite de {max_iteraciones} iteraciones.")
            break

# Llamar a la función con el shard iterator proporcionado
shard_iterator = obtener_shard_iterator()  # Obtener el primer ShardIterator
obtener_registros(shard_iterator)
