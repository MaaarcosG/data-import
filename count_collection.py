import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Ruta a tu archivo de credenciales descargado desde la consola de Firebase
cred = credentials.Certificate("data/database/firebase-config.json")

# Inicializa la app de Firebase con las credenciales
firebase_admin.initialize_app(cred)

# Obtiene una referencia a la colección que deseas contar
db = firestore.client()
collection_ref = db.collection("files")

docs = collection_ref.stream()
document_ids = [doc.id for doc in docs]

# Imprimir los IDs
print("IDs de los documentos en la colección:")
print(document_ids)