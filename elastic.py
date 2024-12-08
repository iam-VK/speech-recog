from elasticsearch import Elasticsearch
from mysql_DB import video_To_file_id
from MY_Modules import file_name_extract

client = Elasticsearch(
  "https://localhost:9200/",
  api_key="N2l1TUlwSUJTMWxfTmtUOGlpR1M6cThDOVNGTEJUNXVwZ2VzY2t2OG4tdw==",
  verify_certs=False,
  ssl_show_warn=False
)

def insert_into_elastic(filename, transcription):
    _, filename_without_extension = file_name_extract(filename)
    file_id = video_To_file_id(filename_without_extension)
    doc = {
        "file_name":filename,
        "video_id":file_id, ## TODO change video_id to file_id in elastic db
        "transcription":transcription
    }

    resp = client.index(index="transcription-index", document=doc, id=file_id)
    print("response from elastic: ",resp)
    return resp