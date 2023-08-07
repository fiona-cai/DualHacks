import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("private_data/dualhacks-b5721-firebase-adminsdk-8ml42-4a14b77ebb.json")

firestore_app = firebase_admin.initialize_app(cred)
