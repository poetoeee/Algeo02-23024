from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import shutil
import os
import json
import zipfile
from audio.main import handle_query_audio, procces_audio_db
from image.integration import handle_query, process_dataset
# import zipfile
# from audio.main import handle_query_audio, procces_audio_db
# from image.integration import handle_query, process_dataset


# App instance
app = Flask(__name__)
CORS(app)

# Path Folder Dataset
BASE_DIR = os.getcwd()
AUDIO_FOLDER = os.path.join(BASE_DIR, "src", "backend", "audio", "database_song")
AUDIO_RES_JSON = os.path.join(BASE_DIR, r"src\backend\audio\result\audio.json")
IMAGE_FOLDER = os.path.join(BASE_DIR, "src", "backend", "image", "database_image")
IMAGE_MAPPER_FILE = os.path.join(BASE_DIR, "src", "backend", "mapper", "audio_image_map.json")
IMAGE_RES_JSON = os.path.join(BASE_DIR, r"src\backend\image\result\image.json")

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

#------------SONG------------#
#upload song query
@app.route("/api/upload_query_song", methods = ["POST"])
def upload_query_song():
    try:

        query_song_folder = os.path.join(r"src\backend\audio", "query")
        
        if os.path.exists(query_song_folder) and os.path.isdir(query_song_folder):
            shutil.rmtree(query_song_folder)
        
        os.makedirs(query_song_folder, exist_ok=True)

        query = request.files.get('file_song')
        
        if not query:
            return jsonify({'error': 'No file uploaded'}), 400
        
        query_dir = os.path.join(r"src\backend\audio\query", query.filename)

        query.save(query_dir)
        return jsonify({"message": "Song querry uploaded successfully"})

    except Exception as e:
        return jsonify({'error' : str(e)}), 500


##search song
@app.route("/api/compare_song", methods = ['POST'])
def compare_song():
    '''
        return json of dictionary[name:kemiripan]
    '''
    try:

        for file in os.listdir(r"src\backend\audio\query"):
            print(file)
            query_dir = os.path.join(r"src\backend\audio\query", file)
            res = handle_query_audio(query_dir) 

            break
        
        #Sort
        # sorted_dict = dict(sorted(res.items(), key=lambda item: item[1]))
        song_res_json_dir = os.path.join(r"src\backend\audio\result")
        res_dir = os.path.join(r"src\backend\audio\result\audio.json")

        if os.path.exists(song_res_json_dir) and os.path.isdir(song_res_json_dir):
            shutil.rmtree(song_res_json_dir)
        os.makedirs(song_res_json_dir)
        
        with open(res_dir, 'w') as f:
            json.dump(res, f)

        return jsonify(res)
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500


##Upload database song
@app.route("/api/upload_song", methods= ["POST"])
def procces_song():
    try:
        temp = os.path.join(r"src\backend\audio\temp")
        extracted = os.path.join(r"src\backend\audio\database_song")
        
        if os.path.exists(extracted) and os.path.isdir(extracted):
            shutil.rmtree(extracted)
            
        os.makedirs(temp, exist_ok=True)
        uploaded_file = request.files.get('file_song_db')

        if not uploaded_file:
            return jsonify({'error': 'No file uploaded'}), 400
        
        zip_path = os.path.join(r"src\backend\audio\temp", uploaded_file.filename)
        uploaded_file.save(zip_path)

        os.makedirs(extracted, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted)

        procces_audio_db(path=extracted)

        return jsonify({"message": "Song database processed successfully"})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

#--------------IMAGE------------#
#Upload query
@app.route("/api/upload_query_image", methods = ["POST"])
def upload_query_image():
    try:
        query_image_folder = os.path.join(r"src\backend\image\query")
        
        if os.path.exists(query_image_folder) and os.path.isdir(query_image_folder):
            shutil.rmtree(query_image_folder)
            
        os.makedirs(query_image_folder, exist_ok=True)

        query = request.files.get('file_image')
        query_dir = os.path.join(r"src\backend\image\query", query.filename)
        
        if not query:
            return jsonify({'error': 'No file uploaded'}), 400
        
        query.save(query_dir)
        
        return jsonify({"message": "Image querry uploaded successfully"})
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

#Search image
@app.route("/api/compare_image", methods = ["POST"])
def compare_image():
    '''
        return json of dictionary[name:kemiripan]
    '''
    try:
        for file in os.listdir(r"src\backend\image\query"):
            print(file)
            query_dir = os.path.join(r"src\backend\image\query", file)
            res = handle_query(query_dir)

            break
        
        image_res_json_dir = os.path.join(r"src\backend\image\result")
        res_dir = os.path.join(r"src\backend\image\result\image.json")

        if os.path.exists(image_res_json_dir) and os.path.isdir(image_res_json_dir):
            shutil.rmtree(image_res_json_dir)

        os.makedirs(image_res_json_dir)
        
        with open(res_dir, 'w') as f:
            json.dump(res, f)
        
        return jsonify(res)
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500


##Upload image database 
@app.route("/api/upload_image", methods= ["POST"])
def procces_image():
    try:
        temp = os.path.join(r"src\backend\image\temp")
        extracted = os.path.join(r"src\backend\image\database_image")

        if os.path.exists(extracted) and os.path.isdir(extracted):
            shutil.rmtree(extracted)

        os.makedirs(temp, exist_ok=True)
        uploaded_file = request.files.get('file_image_db')

        if not uploaded_file:
            return jsonify({'error': 'No file uploaded'}), 400
        
        zip_path = os.path.join(r"src\backend\image\temp", uploaded_file.filename)
        uploaded_file.save(zip_path)
        os.makedirs(extracted, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extracted)
        process_dataset(extracted, "processed_data.npy")
        return jsonify({"message": "Image database processed successfully"})
    
    except Exception as e:
        return jsonify({'errornya' : str(e)}), 500
    
@app.route("/api/play/<filename>", methods=["GET"])
def serve_audio(filename):
    """
    Serves audio files for playback.
    """
    if not os.path.exists(AUDIO_FOLDER):
        return jsonify({"error": "Audio folder not found"}), 404

    if not os.path.exists(os.path.join(AUDIO_FOLDER, filename)):
        return jsonify({"error": f"Audio file {filename} not found"}), 404

    return send_from_directory(AUDIO_FOLDER, filename, mimetype="audio/midi")

#-------------MAPPER-----------
@app.route("/api/upload_mapper", methods= ["POST"])
def upload_mapper():
    try:
        mapper_dir = os.path.join(r"src\backend\mapper")
        
        if os.path.exists(mapper_dir) and os.path.isdir(mapper_dir):
            shutil.rmtree(mapper_dir)
            
        os.makedirs(mapper_dir, exist_ok=True)

        query = request.files.get('file_mapper')
        mapper_dir = os.path.join(r"src\backend\mapper", "audio_image_map.json")
        
        if not query:
            return jsonify({'error': 'No file uploaded'}), 400
        
        query.save(mapper_dir)
        
        return jsonify({"message": "Mapper uploaded successfully"})
    
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    app.run(debug=True, port=8080)


