from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# 🔴 Change this path to your Firebase credentials
cred = credentials.Certificate(r"C:\Users\saidp\OneDrive\Desktop\forest detection\firedetection-7d3c2-firebase-adminsdk-fbsvc-c83b518799.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/fire-status', methods=['GET'])
def get_fire_status():
    doc_ref = db.collection("fire_alerts").document("current_status")
    doc = doc_ref.get()
    if doc.exists:
        return jsonify(doc.to_dict())
    return jsonify({"fire_detected": False, "timestamp": "N/A"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
