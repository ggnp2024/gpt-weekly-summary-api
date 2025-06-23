from flask import Flask, request, jsonify
from datetime import datetime
import os
import requests

app = Flask(__name__)

@app.route("/generate-summary", methods=["POST"])
def generate_summary():
    data = request.get_json()
    week_range = data.get("weekRange", "Unknown Week")
    email_summary = data.get("emailSummary", "")
    bullets = data.get("bullets", [])

    filename = f"Weekly_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    file_path = os.path.join("/tmp", filename)

    with open(file_path, "w") as f:
        f.write(f"Weekly Accomplishment Summary – Week of {week_range}\n")
        f.write("Office of Public Trust – IT\n\n")
        f.write("Email Summary:\n")
        f.write(email_summary + "\n\n")
        f.write("Performance Summary Bullets:\n")
        for bullet in bullets:
            f.write(f"• {bullet}\n")

    # Upload to file.io
    with open(file_path, "rb") as file_to_upload:
        response = requests.post("https://file.io", files={"file": file_to_upload})

    if response.ok:
        file_url = response.json().get("link")
        return jsonify({"fileUrl": file_url})
    else:
        return jsonify({"error": "Upload failed"}), 500
