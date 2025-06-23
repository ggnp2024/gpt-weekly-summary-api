from flask import Flask, request, send_file
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/generate-summary", methods=["POST"])
def generate_summary():
    data = request.get_json()
    week_range = data.get("weekRange", "Unknown Week")
    email_summary = data.get("emailSummary", "")
    bullets = data.get("bullets", [])

    filename = f"Weekly_Accomplishment_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    file_path = os.path.join("/tmp", filename)

    with open(file_path, "w") as f:
        f.write(f"Weekly Accomplishment Summary – Week of {week_range}\n")
        f.write("Office of Public Trust – IT\n\n")
        f.write("Email Summary:\n")
        f.write(email_summary + "\n\n")
        f.write("Performance Summary Bullets:\n")
        for bullet in bullets:
            f.write(f"• {bullet}\n")

    return send_file(file_path, as_attachment=True, download_name=filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 for local dev
    app.run(host="0.0.0.0", port=port)
