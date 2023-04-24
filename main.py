from bottle import route, run, post, request, redirect, static_file, template
from conversions import ai_call
import os


def response_template(path, audience, api_key, flags):
    redirect = '/'
    return (f"<html> <head><title>Quiz Inspector</title></head>"
            f" <pre>{ai_call(pdf_path=path, audience=audience, api_key=api_key, flags=flags)}</pre></h><br/>"
            f"<input type='button' onclick=\"window.location.href='{redirect}'\" value='Back'/>")

@route('/')
def startpage():
    return template('upload.html', root='.', checkbox1=True, checkbox2 = True, checkbox3=True, checkbox4=True, checkbox5=True)


@post('/response')
def upload():
    flags = []
    audience = request.POST['audience']
    api_key = request.POST['api_key']
    pdf_file = request.files.get('upload')
    checkbox1 = request.forms.get("checkbox1")
    checkbox2 = request.forms.get("checkbox2")
    checkbox3 = request.forms.get("checkbox3")
    checkbox4 = request.forms.get("checkbox4")
    checkbox5 = request.forms.get("checkbox5")
    flags.append(checkbox1)
    flags.append(checkbox2)
    flags.append(checkbox3)
    flags.append(checkbox4)
    flags.append(checkbox5)
    name, ext = os.path.splitext(pdf_file.raw_filename)
    if audience and api_key and pdf_file:
        if ext not in ('.pdf'):
            return "This file extenstion is not supported. Please upload a PDF file."
        else:
            return response_template(path=pdf_file.file.read(), audience=audience, api_key=api_key, flags=flags)
    else:
        return "Please fill in all fields to proceed."


run(host='localhost', port=8080, debug=True, reloader=True)
