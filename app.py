from flask import Flask, render_template, request
from flask_dropzone import Dropzone

import os
import requests
import pprint
import io
import base64
import json
import time

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    #uncomment below when deploying on heroku
    # UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    
    # Flask-Dropzone config:
    # DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=5,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='handle_form',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
    DROPZONE_REDIRECT_VIEW='handle_form',
)

dropzone = Dropzone(app)

source_language = ["English", "Spanish", "Japanese", "Korean", "German"]
target_language = ["English", "Spanish", "Japanese", "Korean", "German"]
language_value = ["en-US", "es-ES", "ja-JP", "ko-KR", "de-DE"]

@app.route('/')
def index():
    return render_template('index2.html', 
    data = zip(source_language, language_value),
    data2 = zip(target_language, language_value))


@app.route('/upload', methods=['POST'])
def handle_upload():
    for key, f in request.files.items():
        if key.startswith('file'):
            f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return '', 204


@app.route('/form', methods=['POST'])
def handle_form():

    if request.method == 'POST':

        try:
            title = request.form.get('title')
            description = request.form.get('description')

            time.sleep(5)
            sourcelanguage_selected = request.form.get('sourcelanguage')
            print("languages:")
            print(sourcelanguage_selected)
            targetlanguage_selected = request.form.get("targetlanguage")
            print(targetlanguage_selected)

            uploadedfile_list = []
            files_data = []
            
            for key, f in request.files.items():
                if key.startswith('file'):
                    # f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                    # print(f)  #filestorage
                    print("name of the files are: ")
                    print(f.filename)
                    file_contents = (os.path.join(app.config['UPLOADED_PATH'], f.filename ))
                    file_path = open(file_contents)
                    print(file_path)
                    uploadedfile_list.append(f.filename)
                    print("files uploaded are: ")
                    print(uploadedfile_list)  #list working

                    destination = os.path.join(app.config['UPLOADED_PATH']), f.filename
                    print('destination is:')
                    print(destination)
                    # ('C:\\Users\\masao\\Desktop\\Projects\\doc_analyzer\\uploads', 'fillable_example.pdf')

                    global file_to_post
                    file_to_post = (os.path.join(app.config['UPLOADED_PATH'], f.filename))
                    print('file_to_post is:')
                    print(file_to_post)
                    return file_to_post
                    #C:\Users\masao\Desktop\Projects\doc_analyzer\uploads\fillable_example.pdf

            return 'file uploaded and form submit<br>title: %s<br> description: %s<br> file_to_post: %s<br>targetlanguage_selected: %s' % (title, description,file_to_post, targetlanguage_selected)

        except requests.RequestException as e:
            print(e)




    


if __name__ == '__main__':
    app.run(debug=True)