import os
import glob
from moviepy.editor import VideoFileClip

def prepare_output_dir(output_path:str):
    isExist = os.path.exists(output_path)
    if isExist:
        old_files = glob.glob(output_path+'/*')
        for f in old_files:
            os.remove(f)
    else:
        os.makedirs(output_path)
    
    return output_path

def file_name_extract(file_path):
    file_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(file_name)

    return file_name, file_name_without_extension

def extract_audio(filename):
    _, file_name_without_ext = file_name_extract(filename)
    
    video_clip = VideoFileClip(f"./uploads/{filename}")
    prepare_output_dir('audios')
    audio_path = f"./audios/{file_name_without_ext}.wav"
    video_clip.audio.write_audiofile(audio_path, codec="pcm_s16le")

    video_clip.close()
    return {"file_name": filename,
            "audio_file":audio_path}


# def vidName_from_path(vid_dir_path:str="uploads"):
#     vid_files = glob.glob(vid_dir_path+'/*')
#     return [name.replace(vid_dir_path,"").replace("\\","").replace("/","") for name in vid_files]


# print(file_name_extract("holland_BrEn.mp4"))
# print(vidName_from_path("uploads"))