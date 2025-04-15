from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
DOWNLOAD_DIR = "/app/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def home():
    return "🎬 Flask Video Server is running!"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    cmd = [
        "yt-dlp",
        "-f", "bestvideo+bestaudio/best",
        url,
        "-o", f"{DOWNLOAD_DIR}/%(title)s.%(ext)s"
    ]

    try:
        subprocess.Popen(cmd)
        return jsonify({"status": "Started"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/list", methods=["GET"])
def list_downloads():
    return jsonify(os.listdir(DOWNLOAD_DIR))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
