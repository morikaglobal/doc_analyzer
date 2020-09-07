from flask import Flask, render_template, request
from flask_dropzone import Dropzone

import os
import requests
import pprint
# import io
# import base64
import json
import time

from google.cloud import storage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='gcskey.json'
client = storage.Client()
# https://console.cloud.google.com/storage/browser/[bucket-id]/
bucket = client.get_bucket('translationdocs')

app = Flask(__name__)

app.config.update(
    # UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    # Flask-Dropzone config:
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024, #upload file max size is 16MB
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=3,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='handle_upload',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
)

dropzone = Dropzone(app)

source_language = ["English", "Spanish", "Japanese", "Korean", "German"]
target_language = ["English", "Spanish", "Japanese", "Korean", "German"]
language_value = ["en-US", "es-ES", "ja-JP", "ko-KR", "de-DE"]

uploadedfile_list = []
files_data_topost = []

@app.route('/')
def index():
    return render_template('index4.html', 
    data = zip(source_language, language_value),
    data2 = zip(target_language, language_value))

@app.route('/upload', methods=['POST'])
def handle_upload():

    for key, f in request.files.items():
        if key.startswith('file'):
            print("there is a file or files submitted")
            print("name of the files is: ")
            print(f.filename)

            # uploading submitted files to GCS
            blob = bucket.blob(f.filename)
            blob.upload_from_file(f)
            print(f) #filestorage

            uploadedfile_list.append(f.filename)

            # get file data from GCS to make POST request to matecat API later on
            blob_get_file = bucket.get_blob(f.filename)
            filedata = blob_get_file.download_as_string()  
            # print(filedata)  - file contents

            global files_data
            files_data = {
                    'file': (f.filename, #name of the uploading file  
                    filedata,
                    'application/octet-stream')
                    # open(os.path.join(app.config['UPLOADED_PATH'], f.filename ), 'rb')
            }
            print("files_data")
            files_data_topost.append(files_data)
            # print(files_data) example below
            # {'file': ('testfile.txt', b'TestingTestingTesting\r\nLorem ipsum', 'application/octet-stream')}        
        

    print("files uploaded are: ")
    print(uploadedfile_list)  

    print("FILES_DATA to be posted for API reqeust")
    # print(files_data_topost)

    # check files saved in GCS
    for f in bucket.list_blobs():
        print(f)
    return '', 204            

@app.route('/form', methods=['POST'])
def handle_form():
    print("HANDLINE THE DATA for API REQUEST")

    data_array = []
    
    sourcelanguage_selected = request.form.get('sourcelanguage')
    sourcelanguage_text_index = language_value.index(sourcelanguage_selected)
    print(sourcelanguage_text_index) #index
    sourcelanguage_text = source_language[sourcelanguage_text_index]
    print(sourcelanguage_text) # ex Spanish
  
    targetlanguage_selected = request.form.get("targetlanguage")
    targetlanguage_text_index = language_value.index(targetlanguage_selected)
    print(targetlanguage_text_index) #index
    targetlanguage_text = target_language[targetlanguage_text_index]
    print(targetlanguage_text) # ex Spanish

    print("languages:")
    print(sourcelanguage_selected)
    print(targetlanguage_selected)

    print("file data to post for the API request")
    # print(files_data) -comment out as large data

    project_data = {
            "project_name": "NEWDOCUMENT",
            "source_lang": sourcelanguage_selected,
            "target_lang": targetlanguage_selected
    }
    
    for (name, data) in zip (uploadedfile_list, files_data_topost):

        display_data = {}

        name_of_the_file = name
        # {'file': ('testfile.txt', b'TestingTestingTesting\r\nLorem ipsum', 'application/octet-stream')}  example
        r_post = requests.post('https://www.matecat.com/api/v1/new',
        data = project_data,
        files = data
        )

        print(name_of_the_file)
        display_data["documentname"] = name_of_the_file

        print(r_post.status_code)
        pprint.pprint(r_post.json())
        created_info = r_post.json()
        print(type(created_info))  #dict
        

        id = created_info['id_project']
        pass_code = created_info['project_pass']

        print(id)
        print(pass_code)

        get_data = {
            "id_project": id,
            "project_pass": pass_code
        }

        # need sleep to wait for the analyzed data to be ready at metacat side
        time.sleep(15)
        # GET request to metacat to get the analyzed data for the document uploaded
        r_get = requests.get('https://www.matecat.com/api/status',
            params = get_data)

        print(r_get.status_code)
        # pprint.pprint(r_get.json())
        statistics = r_get.json()
        print(type(statistics)) #dict

        maindata = statistics['data']
        print(type(maindata)) #dict
        print(maindata)

        total_word_count = maindata['summary']['TOTAL_RAW_WC']
        if type(total_word_count) == str:
            total_word_count = int(total_word_count)   
        total_word = round(total_word_count)
        print(total_word)
        # print(round(total_word_count))

        industry_weighted_count = maindata['summary']['TOTAL_STANDARD_WC']
        if type(industry_weighted_count) == str:
            industry_weighted_count = int(industry_weighted_count)
        industry_weighted = round(industry_weighted_count)
        print(industry_weighted)
        # print(round(industry_weighted))

        weighted_words_count = maindata['summary']['TOTAL_PAYABLE']
        if type(weighted_words_count) == str:
            industry_weighted_count = int(weighted_words_count)
        weighted_words = round(weighted_words_count)
        print(weighted_words)
        # print(round(weighted_words))

        percentage = weighted_words / total_word
        print(percentage)
        discount_percentage = round((1 - percentage) * 100)
        print(discount_percentage)

        display_data["totalwordcount"] = total_word
        display_data["industryweighted"] = industry_weighted
        display_data["weightedwords"] = weighted_words
        display_data["discountpercentage"] = discount_percentage
        
        data_array.append(display_data)
    
    print(data_array)
    
    return render_template('result.html', data_array=data_array, sourcelanguage_text=sourcelanguage_text,targetlanguage_text=targetlanguage_text)

if __name__ == '__main__':
    app.run(debug=True)