from bottle import route, run, get, post, request, redirect
from conversions import ai_call
import os

template = """<html>
<head><title>Quiz Inspector</title></head>
<body>
<h1>Upload a file</h1>
<form method="POST" enctype="multipart/form-data" action="/response">
<label>Audience:</label> <input type="text" name="audience" value=""><br>
<label>API Key:</label> <input type="text" name="api_key" value=""><br>
<label> Test PDF: </label><input type="file" name="upload"/><br>
<input type="submit" value="Submit" />
</form>
</body>
</html>"""


def response_template(path, audience, api_key):
    redirect = '/upload'
    return (f"<html> <head><title>Quiz Inspector</title></head><h>"
            f" <pre>{ai_call(pdf_path=path, audience=audience, api_key=api_key)}</pre></h><br/>"
            f"<input type='button' onclick=\"window.location.href='{redirect}'\" value='Back'/>")


@route('/upload')
def startpage():
    return template


@post('/response')
def upload():
    audience = request.POST['audience']
    api_key = request.POST['api_key']
    pdf_file = request.files.get('upload')
    name, ext = os.path.splitext(pdf_file.raw_filename)
    if audience and api_key and pdf_file:
        if ext not in ('.pdf'):
            return "This file extenstion is not supported. Please upload a PDF file."
        else:
            #save_path = os.curdir+'/tempPDFS/'
            #pdf_file.save(save_path)
            #pdf_path = save_path + pdf_file.raw_filename
            return response_template(path=pdf_file.file.read(), audience=audience, api_key=api_key)
    else:
        return "Please fill in all fields to proceed." 
run(host='localhost', port=8080, debug=True)
