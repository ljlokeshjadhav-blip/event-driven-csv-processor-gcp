import json
import io
import base64
import pandas as pd
from flask import Flask, request
from google.cloud import storage, firestore

app = Flask(__name__)

storage_client = storage.Client()
firestore_client = firestore.Client()

@app.route("/", methods=["POST"])
def process_file():
    envelope = request.get_json()
    message = envelope["message"]
    data = json.loads(base64.b64decode(message["data"]).decode())

    bucket_name = data["bucket"]
    file_name = data["name"]

    if not file_name.endswith(".csv"):
        return "Only CSV allowed", 400

    doc = firestore_client.collection("processed_files").document(file_name)
    if doc.get().exists:
        return "Already processed", 200

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)
    csv_bytes = blob.download_as_bytes()

    df = pd.read_csv(io.BytesIO(csv_bytes))

    result = {
        "file_name": file_name,
        "row_count": len(df),
        "null_counts": df.isnull().sum().to_dict()
    }

    report_name = file_name.replace("raw-data/", "reports/").replace(".csv", ".json")
    bucket.blob(report_name).upload_from_string(
        json.dumps(result, indent=2),
        content_type="application/json"
    )

    doc.set({"status": "done"})

    return "Processed", 200
