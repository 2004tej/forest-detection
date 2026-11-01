import firebase_admin
from firebase_admin import credentials, firestore
import cv2
import numpy as np
import time
import requests
from twilio.rest import Client

# Initialize Firebase
cred = credentials.Certificate("firedetection-7d3c2-firebase-adminsdk-fbsvc-c83b518799.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Twilio Credentials (Replace with your details)
TWILIO_ACCOUNT_SID = "ACb83a3897cf959bd487914a0fe53c449c"
TWILIO_AUTH_TOKEN = "2b8e0c725e864600982d897f819359e6"
TWILIO_PHONE_NUMBER = "+16154373592"  # Your Twilio number
YOUR_PHONE_NUMBER = "+91 8309128227"  # Your mobile number

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Google Geolocation API (Replace with your API key)
GOOGLE_API_KEY = "AIzaSyBpBj6RFMjZD5huKTu2ecPbe-7sPz_3EWo"

# Function to get latitude and longitude
def get_location():
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"
    response = requests.post(url, json={"considerIp": "true"}).json()
    
    if "location" in response:
        lat, lon = response["location"]["lat"], response["location"]["lng"]
        print(f"📍 Location Detected: {lat}, {lon}")
        return lat, lon
    else:
        print("⚠️ Failed to get location")
        return None, None

# Function to send SMS alert with Google Maps link
def send_sms_alert(lat, lon):
    google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
    message = f"🔥 Fire Detected at Location: {lat}, {lon}\n📍 Google Maps: {google_maps_link}"
    
    sms = client.messages.create(
        body=message,
        from_=TWILIO_PHONE_NUMBER,
        to=YOUR_PHONE_NUMBER
    )
    print(f"📲 SMS Sent: {sms.sid}")

# Fire detection simulation (Replace with real model)
def detect_fire():
    fire_detected = np.random.choice([True, False], p=[0.1, 0.9])  # Simulate fire detection
    return fire_detected

# Function to send fire alert with location
def send_fire_alert(status):
    latitude, longitude = get_location()  # Get real-time location
    if latitude and longitude:
        doc_ref = db.collection("fire_alerts").document("current_status")
        doc_ref.set({
            "fire_detected": bool(status),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "latitude": latitude,
            "longitude": longitude
        })
        print(f"🔥 Fire Alert Sent: {status} at ({latitude}, {longitude})")
        
        # Send SMS if fire is detected
        if status:
            send_sms_alert(latitude, longitude)

# Main loop for fire detection
while True:
    fire = detect_fire()
    send_fire_alert(fire)
    time.sleep(10)  # Check every 10 seconds
