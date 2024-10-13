from flask import Flask, request
from flask_cors import CORS
from MY_Modules import prepare_output_dir
from MY_Modules import extract_audio
from elastic import insert_into_elastic
from ASR_model import speech_recog

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST','GET'])
def service_status():
    return {
                "/speech-index": {
                    "method": "POST",
                    "parameters": {
                        "form_data": ["dir", "vid_name"],
                        "file_upload": "video file",
                        "mode":"standalone, default chained"
                    }
                }
            }

@app.route("/speech-index", methods=['POST'])
def speech_model():
    # check the metadata for file details and check if the file has been recieved
    if request.method == 'POST':
        file = request.files['file_upload']
        mode = request.form.get('mode',"chained") # other mode:standalone, default mode:chained

        if file:
            prepare_output_dir('uploads')
            filename = file.filename
            file_path = f"uploads/{filename}"
            file.save(file_path)

            ###
            audio_extract_resp = extract_audio(filename)
            print(audio_extract_resp)

            transcript = str(speech_recog(filename))
            print(transcript)

            if mode == "standalone":
                return {"filename":filename,
                        "transcript":transcript}

            elif mode == "db":
                resp = insert_into_elastic(filename, transcript)
                return {"elastic_response": str(resp)}
            
            else:
                return {"Error":"Unrecognized mode"}
            ####

        else:
            return {"Error":"No file Recieved"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5005, use_reloader = True)