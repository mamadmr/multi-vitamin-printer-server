import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from datetime import datetime


# generate the location of the to_print_files folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'to_print_files')

# create the Flask app
app = Flask(__name__)

# set the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/print', methods=['POST'])
def _print():
    now = datetime.now()
    if 'file' not in request.files:
        return "{'message': 'you should send a file'}"
    file = request.files['file']
    filename = str(now.strftime("%d-%m-%Y_%H:%M:%S"))+'@'+ secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    return "{'message': 'file has recieved', file_name="+filename+"}"

@app.route('/check', methods=['POST'])
def _check():
    data = request.json
    return data['filename']

    return "{'message': 'check'}"

if __name__ == "__main__":
    app.run(debug=True)