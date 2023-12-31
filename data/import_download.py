import pymongo
import os
import requests

class DataDownloader:
    def __init__(self, api_key, base_id, table_name, url, db):
        self.base_id = base_id
        self.table_name = table_name
        self.api_key = api_key
        self.url = url

        # Configurar la conexión a MongoDB
        self.client = pymongo.MongoClient(db)
        self.db = self.client['db']

    def is_pdf_file(self, file_url):
        response = requests.head(file_url)
        content_type = response.headers.get('content-type', '')
        return content_type.lower() == 'application/pdf'

    def is_file_size_within_limit(self, file_url, max_size_bytes=2 * 1024 * 1024):
        response = requests.head(file_url)
        file_size = int(response.headers.get('content-length', 0))
        return file_size <= max_size_bytes

    def save_attachment_to_mongodb(self, attachment):
        file_url = attachment.get('url', '')
        file_name = attachment.get('filename', '')

        # Verificar si el archivo adjunto ya ha sido procesado previamente
        if not self.db['documents'].find_one({'url': file_url}):
            response = requests.get(file_url)
            if response.status_code == 200:
                # Guardar el contenido del archivo en MongoDB
                file_data = {
                    'url': file_url,
                    'name': file_name,
                    'data': response.content
                }
                self.db['files'].insert_one(file_data)
                print(f'Archivo guardado en MongoDB: {file_name}')
            else:
                print(f'Error al guardar el archivo: {file_name}')
        else:
            print(f'Archivo previamente procesado, se omite: {file_name}')

    def download_files_from_airtable(self):
        # Configurar la URL de la API de Airtable
        api_url = '%s/%s/%s' % (self.url, self.base_id, self.table_name)

        # Encabezados de autenticación
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }

        # Realizar la solicitud GET para obtener los datos de la tabla
        while api_url:
            try:
                response = requests.get(api_url, headers=headers)

                if response.status_code == 200:
                    # Convertir la respuesta JSON a un diccionario de Python
                    data = response.json()
                    records = data.get('records', [])

                    # Descargar los archivos adjuntos PDF dentro del límite de tamaño y guardarlos en MongoDB
                    for record in records:
                        fields = record.get('fields', {})
                        attachments = fields.get('CV', [])
                        if attachments:
                            for attachment in attachments:
                                # Utilizar el método get con valor predeterminado para evitar errores por campos faltantes
                                file_url = attachment.get('url', '')
                                file_name = attachment.get('filename', '')
                                if self.is_pdf_file(file_url) and self.is_file_size_within_limit(file_url):
                                    try:
                                        self.save_attachment_to_mongodb(attachment)
                                    except Exception as e:
                                        print(f'Error al guardar el archivo en MongoDB: {e}')
                                else:
                                    print(f'Archivo omitido: {file_name}, no es un PDF o excede el tamaño máximo permitido.')
                        else:
                            print(f'Registro sin archivos adjuntos: {record.get("id")}')
                else:
                    print(f'Error al obtener los datos de Airtable. Código de estado: {response.status_code}')
                    break
            except requests.exceptions.RequestException as e:
                print(f'Error en la solicitud a la API: {e}')
                break
            except Exception as e:
                print(f'Error desconocido: {e}')
                break
