from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

# App instance
app = Flask(__name__)
CORS(app)

# Path Folder Dataset
BASE_DIR = os.getcwd()
AUDIO_FOLDER = os.path.join(BASE_DIR, "src", "backend", "audio", "database_song", "midi_dataset1")
IMAGE_FOLDER = os.path.join(BASE_DIR, "src", "backend", "image", "database_image1")
IMAGE_MAPPER_FILE = os.path.join(BASE_DIR, "src", "audio_image_map.json")

# ---------------------- ROUTES ----------------------

# 1. Route Home
@app.route("/api/home", methods=["GET"])
def return_home():
    return jsonify({
        "pesan": "Gacor 45"
    })

# 2. Route Audio List
@app.route("/api/audios", methods=["GET"])
def get_audios():
    """
    Returns a list of audio files from the audio folder.
    """
    if not os.path.exists(AUDIO_FOLDER):
        return jsonify({"error": "Audio folder not found"}), 404

    audio_files = [
        f for f in os.listdir(AUDIO_FOLDER)
        if f.lower().endswith(('.wav', '.mp3', '.midi', '.mid'))
    ]

    return jsonify({"songs": audio_files})

# 3. Route Images List Based on Mapper
@app.route("/api/images", methods=["GET"])
def get_images():
    """
    Returns a list of mapped images linked to audio files.
    """
    if not os.path.exists(IMAGE_MAPPER_FILE):
        return jsonify({"error": "Image mapper file not found"}), 404

    with open(IMAGE_MAPPER_FILE, "r") as file:
        try:
            mapper = json.load(file)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid mapper JSON file"}), 500

    # Membuat path image yang dapat diakses
    data = [
        {
            "audio_file": entry.get("audio_file"),
            "image_url": f"/api/image/{entry.get('pic_name')}"
        }
        for entry in mapper
    ]

    return jsonify(data)

# 4. Route Serve Image
@app.route("/api/image/<filename>", methods=["GET"])
def serve_image(filename):
    """
    Serves image files from the image folder.
    """
    print("Serving image:", filename)  # Debug: cek nama file yang diminta
    print("Image folder path:", IMAGE_FOLDER)  # Debug: cek path folder image
    
    if not os.path.exists(IMAGE_FOLDER):
        return jsonify({"error": "Image folder not found"}), 404
    
    if not os.path.exists(os.path.join(IMAGE_FOLDER, filename)):
        return jsonify({"error": f"Image {filename} not found"}), 404

    return send_from_directory(IMAGE_FOLDER, filename)

# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    app.run(debug=True, port=8080)
