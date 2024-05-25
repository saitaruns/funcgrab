import firebase_admin
import pyrebase
from firebase_admin import credentials

if not firebase_admin._apps:
    cred = credentials.Certificate("./serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

config = {
    "apiKey": "AIzaSyDjEJtT1TJjz4G5BFogiLUxxr0uC-hpAg8",
    "authDomain": "fastapiauth-fed6e.firebaseapp.com",
    "projectId": "fastapiauth-fed6e",
    "storageBucket": "fastapiauth-fed6e.appspot.com",
    "messagingSenderId": "1059164332666",
    "appId": "1:1059164332666:web:e6421803dd3d2eb40b91c3",
    "measurementId": "G-5DTMFSHK9P",
    "databaseURL": ""
}

fireb = pyrebase.initialize_app(config)
auth = fireb.auth()

print("Firebase initialized.")