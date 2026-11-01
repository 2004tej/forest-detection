import cv2
import firebase_admin
from firebase_admin import credentials, storage, firestore
import time
import datetime
import random

# 🔴 Change this path to your Firebase credentials
cred = credentials.Certificate(r"C:\Users\saidp\OneDrive\Desktop\forest detection\firedetection-7d3c2-firebase-adminsdk-fbsvc-c83b518799.json")
firebase_admin.initialize_app(cred, {"storageBucket": "firedetection-7d3c2.appspot.com"})

db = firestore.client()
bucket = storage.bucket()

# Initialize camera
cap = cv2.VideoCapture(0)  # Change to the correct camera index if needed

def detect_fire(frame):
    """
    Dummy fire detection function. Replace with a real fire detection model.
    """
    return random.choice([True, False])  # Simulating fire detection

def upload_to_firebase(image_path, filename):
    blob = bucket.blob(f"fire_alerts/{filename}")
    blob.upload_from_filename(image_path)
    blob.make_public()
    return blob.public_url

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"fire_image_{timestamp}.jpg"

    # Save the image locally
    cv2.imwrite(image_path, frame)
    print(f"Captured {image_path}")

    # Fire detection
    fire_detected = detect_fire(frame)

    if fire_detected:
        print("🔥 Fire detected! Uploading image...")

        # Upload image to Firebase Storage
        image_url = upload_to_firebase(image_path, image_path)

        # Update Firestore database
        doc_ref = db.collection("fire_alerts").document("current_status")
        doc_ref.set({
            "fire_detected": True,
            "timestamp": timestamp,
            "image_url": image_url
        })

        print(f"🚨 Fire alert sent! Image URL: {image_url}")

    else:
        print("✅ No fire detected.")

    time.sleep(10)  # Capture every 10 seconds (adjust as needed)

cap.release()
cv2.destroyAllWindows()
