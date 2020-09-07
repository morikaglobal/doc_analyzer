# TRANSLATION DOCUMENT ANALYZER

Document analyzer for Translation projects using <strong>Python</strong>, <strong>matecat API</strong> and <strong>Google Cloud Storage</strong> to automate and analyze the document files uploaded by the user on the web application and get analyzed data on the documents using REST API, built with <strong>Flask</strong> and deployed on <strong>Google App Engine</strong> 

## About the Project

On the landing page of the web application, the user can upload the documents for document analysis, file upload and drag and drop function handled by <strong>Dropzone</strong>, then the uploaded documents are stored in <strong>Google Cloud Storage</strong>, at the same time, the documents uploaded and the language pairs set by the user (the languages pair the document will be translated from/to) will be sent as POST request to <strong>matecat API</strong>

The results page will display the analyzed data returned from <strong>matecat API</strong> 
