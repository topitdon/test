from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
# ✅ สำหรับแบบปลอดภัย: ระบุ extension origin โดยตรง
# CORS(app, origins=["chrome-extension://ehjcafcgkaehoaakilgamgamnalgahhl"])
# แบบไม่ปลอดภัยเท่าไหร่ ขี้เกียจเช็ค extension id
CORS(app)
DOWNLOAD_DIR = "/app/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def home():
    return "🎬 Flask Video Server is running!"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    fmt = data.get("format", "mp4")  # default เป็น mp4

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    filename_template = f"{DOWNLOAD_DIR}/%(title)s.%(ext)s"

    if fmt == "mp3":
        cmd = [
            "yt-dlp",
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", "mp3",
            "-o", filename_template,
            url
        ]
    else:
        cmd = [
            "yt-dlp",
            "-f", "bv*+ba/best",
            "--merge-output-format", "mp4",
            "--no-part",
            "-o", filename_template,
            url
        ]

    subprocess.Popen(cmd)
    return jsonify({"status": "download started", "format": fmt})


@app.route("/list", methods=["GET"])
def list_downloads():
    return jsonify(os.listdir(DOWNLOAD_DIR))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
