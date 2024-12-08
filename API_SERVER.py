import os
from flask import Flask, request
from flask_cors import CORS
from MY_Modules import prepare_output_dir, extract_audio
from elastic import insert_into_elastic
from ASR_model import speech_recog
from mysql_DB import check_index_state, set_index_state

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST','GET'])
def service_status():
    return {
                "/speech-index": {
                    "method": "POST",
                    "parameters": {
                        "file_upload": "video file",
                        "mode":"optional parameter, can be 'standalone' or 'db  ' (default: 'db')"
                    }
                }
            }

@app.route("/speech-index", methods=['POST'])
def speech_model():
    # TODO check the metadata for file details and check if the file has been recieved
    if request.method == 'POST':
        file = request.files['file_upload']
        mode = request.form.get('mode',"db") # other mode:standalone, default mode:db

        if file:
            prepare_output_dir('uploads')
            filename = file.filename
            filename_without_extension = os.path.splitext(filename)[0]
            file_path = f"uploads/{filename}"
            file.save(file_path)

            ###
            if (mode == "db") and (check_index_state(filename_without_extension) in ["speech", "vsn-sph"]):
                return {"status":"AlreadyIndexed",
                        "service_name":"speech_recog",
                        "video_file":filename}

            audio_extract_resp = extract_audio(filename)
            print(audio_extract_resp)

            transcript = speech_recog(filename)
            print(transcript)

            if mode == "standalone":
                return {"filename":filename,
                        "transcript":transcript}

            if mode == "db":
                resp = insert_into_elastic(filename_without_extension, transcript)

                index_state = 'speech' if check_index_state(filename_without_extension) == "None" else "vsn-sph"
                set_index_state(filename_without_extension, index_state)
                
                return {"elastic_response": str(resp)}
            
            else:
                return {"Error":"Unrecognized mode"}
            ####

        else:
            return {"Error":"No file Recieved"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, use_reloader = True)