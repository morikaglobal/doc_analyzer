import os

from flask import Flask, render_template, request
from flask_dropzone import Dropzone
import werkzeug
from werkzeug.utils import secure_filename

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
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    
    
    # Flask-Dropzone config:
    # DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=10,
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

filename = None

@app.route('/')
def index():
    return render_template('index2.html', 
    data = zip(source_language, language_value),
    data2 = zip(target_language, language_value))






#result page
@app.route('/form', methods=['POST'])
def handle_form():

    # try:
    if request.method == 'POST':

        try:
            title2 = request.files.getlist("file")
            title = request.form.get('title')
            print(title)
            # description = request.form.get('description')

            
            time.sleep(5)



            sourcelanguage_selected = request.form.get('sourcelanguage')
            print(sourcelanguage_selected)
            targetlanguage_selected = request.form.get("targetlanguage")
            print(targetlanguage_selected)

            time.sleep(20)
            files_uploaded = request.files
            # print(files_uploaded)  #no value
            files_uploaded_test = request.form
            print(files_uploaded_test)
            testing = request.files.items()
            print("testing")
            print(testing)

            # for file in request.files.getlist("file"):
            #     print(file)
            #     filename = file.filename
            #     destination = '/'.join([os.path.join(app.config['UPLOADED_PATH'], filename])
            #     file.save(destination)

            #     testing = (open(destination), 'rb')
            #     print(testing)





            uploadedfile_list = []
            files_data = []
            for key, f in request.files.items():
                if key.startswith('file'):
                    f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
                    print(f)  #filestorage
                    print("name of the files are: ")
                    print(f.filename)
                    file_contents = (os.path.join(app.config['UPLOADED_PATH'], f.filename ))
                    file_path = open(file_contents)
                    print(file_path)
                    uploadedfile_list.append(f.filename)
                    print("filename filename:")
                    print(uploadedfile_list)  #list working

                    destination = os.path.join(app.config['UPLOADED_PATH']), f.filename
                    print('destination is:')
                    print(destination)
                    # ('C:\\Users\\masao\\Desktop\\Projects\\doc_analyzer\\uploads', 'fillable_example.pdf')


                    TESTing = (os.path.join(app.config['UPLOADED_PATH'], f.filename))
                    print('TESTing is:')
                    print(TESTing)
                    #C:\Users\masao\Desktop\Projects\doc_analyzer\uploads\fillable_example.pdf
                    

                    
                    files_data = {
                        'file1': (f.filename, #name of the uploading file
                        open(TESTing, 'rb'),
                        # open(os.path.join(app.config['UPLOADED_PATH'], f.filename ), 'rb'),


                        # open(f.filename, 'rb'), #file path
                        'application/octet-stream')
                        
                    # ('file2', ('noneditable_example.pdf', #name of the uploading file
                    #         open('noneditable_example.pdf', 'rb'), #file data
                    #         'application/octet-stream'))
                    }
                    # print(open(file_path, 'rb'))
                    print("print files_data")
                    print(files_data)
                    # [('file1', ('fillable_example.pdf', <_io.BufferedReader name='C:\\Users\\masao\\Desktop\\Projects\\doc_analyzer\\uploads\\fillable_example.pdf'>, 'application/octet-stream'))]


            print("printing the list")        
            print(uploadedfile_list)
            # print(uploadedfile_list[0])
                    
            # with open(os.path.join(app.config['UPLOADED_PATH'], 'Excel.xlsx' )) as f:
            #     print(f)

            # <_io.TextIOWrapper name='C:\\Users\\masao\\Desktop\\Projects\\doc_analyzer\\uploads\\Excel.xlsx' mode='r' encoding='cp932'>
            

            project_data = {
                    "project_name": "NEWDOCUMENT",
                    "source_lang": sourcelanguage_selected,
                    "target_lang": targetlanguage_selected
                }

            print(project_data)

            print("uploadedfile_list is: ")
            print(uploadedfile_list)  #list
            
            print("this is the file name")
        
            
            time.sleep(20)
            print("WAITED")
            # print(os.path.join(app.config['UPLOADED_PATH'].exists(uploadedfile_list))
            
            
            
            # files_data = [
            #     ('file1', ('testfile.txt', #name of the uploading file
            #     open('testfile.txt', 'rb'), #file data
            #     'application/octet-stream')),
            # # ('file2', ('noneditable_example.pdf', #name of the uploading file
            # #         open('noneditable_example.pdf', 'rb'), #file data
            # #         'application/octet-stream'))
            # ]
            print("files_data posting")
            # [('file1', ('testfile.txt', <_io.BufferedReader name='testfile.txt'>, 'application/octet-stream'))]
            
            # this is what is getting posted and TESTING NOW
            # [('file1', ('Excel.xlsx', <_io.BufferedReader name='Excel.xlsx'>, 'application/octet-stream'))]


            

            time.sleep(20)

            r_post = requests.post('https://www.matecat.com/api/v1/new',
                data = project_data,
                files = files_data
            )

            print("request posted")

            # time.sleep(10)
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


            time.sleep(10)

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
            print(round(total_word_count))
            industry_weighted = maindata['summary']['TOTAL_STANDARD_WC']
            print(round(industry_weighted))
            weighted_words = maindata['summary']['TOTAL_PAYABLE']
            print(round(weighted_words))
            percentage = weighted_words / total_word_count
            print(percentage)
            discount_percentage = round((1 - percentage) * 100)
            print(discount_percentage)


            return 'file uploaded successfully ' + str(total_word_count) + "  " + str(discount_percentage)



        # files = {
        #         'file': (f.filename, #name of the uploading file
        #                 open(f.filename, 'rb'), #file data
        #                 'application/octet-stream')  #file type
        #     }

        
        
        # for i in files_uploaded:
        #     file = request.files.get(i)
        #     print(i)
        #     print(file.filename)


        # f = request.files['file']
        # print(f)
        # print(type(f))  #filestorage
        # f.save(secure_filename(f.filename))
        # print(f.filename)  #prints filename
        # print("type is:")
        # print(type(f.filename)) #string

        # return 'file uploaded and form submit<br>title: %s<br> description: %s' % (title, description)
        

        except requests.RequestException as e:
            print(e)



# from flask import Flask, render_template, request
# from flask_dropzone import Dropzone
# # from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
# import werkzeug
# from werkzeug.utils import secure_filename

# # import requests
# # import pprint
# # import io
# # import base64
# # # import pycurl
# # import json
# # import time

# app = Flask(__name__)
# dropzone = Dropzone(app)

# # # setting the maximum size of the file to upload at 15MB
# app.config['MAX_CONTENT_LENGTH'] = 15 * 1024 * 1024
# # # app.config['DROPZONE_REDIRECT_VIEW'] = 'result'
# app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
# # app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
# # app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
# app.config['DROPZONE_REDIRECT_VIEW'] = 'result'

# @app.route('/')
# def index2():
#     return render_template('index2.html')

# @app.route('/result', methods=['POST'])
# def handle_form():
#     return 'RESULT PAGE'



# @app.route('/')
# def upload_file():
#    return render_template('index2.html')

# #this worked
# @app.route('/result', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         file_obj = request.files
#         for f in file_obj:
#             file = request.files.get(f)
#             print (file.filename)
#         return "uploading..."
#     return render_template('result.html')



# @app.route('/result')
# def result():
#     return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)