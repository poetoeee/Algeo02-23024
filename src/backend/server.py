from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import zipfile
from audio.main import handle_query_audio, procces_audio_db
# from image.integration import handle_query, process_dataset

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

        query = request.files.get('file_song')
        res = handle_query_audio(query.filename)

        if not query:
            return jsonify({'error': 'No file uploaded'}), 400
        return jsonify(res)
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

@app.route("/api/upload_song", methods= ["POST"])
def procces_song():
    try:
       
        uploaded_file = request.files.get('file_song_db')

        if not uploaded_file:
            return jsonify({'error': 'No file uploaded'}), 400
        
        zip_path = os.path.join(r"src\backend\audio\temp", uploaded_file.filename)
        uploaded_file.save(zip_path)

        extracted = os.path.join(r"src\backend\audio\database_song")
        os.makedirs(extracted, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted)

        procces_audio_db(path=extracted)

        return jsonify({"message": "Song database processed successfully"})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# @app.route("/api/compare_image", methods = ["POST"])
# def compare_image():
#     try:
#         query = request.files.get('file_image')
#         res = handle_query(query.filename)

#         if not query:
#             return jsonify({'error': 'No file uploaded'}), 400
        
#         return jsonify(res)
    
#     except Exception as e:
#         return jsonify({'error' : str(e)}), 500


# @app.route("/api/upload_image", methods= ["GET"])
# def procces_image():
#     try:
#         process_dataset("database_image", "processed_data.npy", )
#         return jsonify({"message": "Image database processed successfully"})
#     except Exception as e:
#         return jsonify({'error' : str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True, port=8080)