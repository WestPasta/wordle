import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials
cred_path = r"C:\Issac Compass\Hackathon\backend\ickathon-firebase-adminsdk-fbsvc-6c2c33ae2f.json"

try:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

    # Initialize Firestore
    db = firestore.client()

    print("Firebase Admin SDK initialized successfully.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {str(e)}")
