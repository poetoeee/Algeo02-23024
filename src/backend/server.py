from flask import Flask, jsonify
from flask_cors import CORS
from audio.main import handle_query_audio, procces_audio_db
from image.integration import handle_query, process_dataset

#app instance
app = Flask(__name__)
CORS(app)

@app.route("/api/home", methods = ['GET'])
def return_home():
    return jsonify({
        "pesan" : "Gacor 45"
    })


@app.route("/api/compare_song", methods = ['POST'])
def compare_song():
    try:
        res = handle_query_audio()
        return jsonify(res)
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

@app.route("/api/upload_song", methods = ['POST'])
def procces_song():
    try:
        procces_audio_db()
        return 1
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

@app.route("api/compare_image", methods = ["POST"])
def compare_song():
    try:
        res = handle_query("image_query.jpg")
        return jsonify(res)
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

@app.route("api/upload_image", methods = [])
def procces_image():
    try:
        process_dataset("database_image", "", )
        return 1
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
if __name__ == "__main__":
    app.run(debug=True, port=8080)