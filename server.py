import os
from flask import Flask, request
from werkzeug.utils import secure_filename
from datetime import datetime
import jwt
from tools import *
from functools import wraps

# debuge mode
debug = True

# generate the location of the to_print_files folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'to_print_files')

# create the Flask app
app = Flask(__name__)

# set the upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# set the secret key
app.config['SECRET_KEY'] = 'your-secret-key'

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorator():
        token = None
        # ensure the jwt-token is passed with the headers
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token: # throw error if no token provided
            return "{'message': 'A valid token is missing!'}"
        try:
           # decode the token to obtain user public_id
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if data['public_id'] == None:
                raise Exception()
            
        except:
            return "{'message': 'Invalid token!'}"
         # Return the user information attached to the token
        return f()
    return decorator

# Login method responsible for generating authentication tokens
@app.route('/login', methods=['POST'])
def login():
    '''
        this function is used to login the user and generate a token for him
        the function returns a json object with the token
    '''

    # check if the request has the dict part
    try:
        auth = request.form.to_dict()
    except:
        return "{'message': 'there is no json object in the request'}"

    # check if the request has the username and password
    if 'username' not in auth or 'password' not in auth:
        return "{'message': 'there is no username or password'}"
    
    # check if the username and password are correct
    resp, public_id = check_username_password(auth['username'], auth['password'])
    if not resp:
        return "{'message': 'username or password is wrong'}"

    # generate the token
    token = jwt.encode({'public_id':  public_id}, app.config['SECRET_KEY'], 'HS256')

    return  "{'token': " + str(token) + "}"

# Print method responsible for recieving files from the client
@app.route('/print', methods=['POST'])
@token_required
def _print():
    '''
    this function is used to recieve the file from the client and save it in the to_print_files folder
    this file will be printed by the printer
    the function returns a json object with the message and the file name
    '''

    # use the datetime to generate a unique name for the file
    now = datetime.now()

    # debug 
    if debug == True:
        pass
        print(request.files['file'].filename[-4:])

    # check if the request has the file part
    if 'file' not in request.files:
        return "{'message': 'you should send a file'}"
    
    # save the file in the to_print_files folder
    file = request.files['file']

    # check if the file is a pdf
    if len(file.filename) < 4 or file.filename[-4:] != '.pdf':
        return "{'message': 'the file should be a pdf'}"
    

    # generate the file name
    filename = str(now.strftime("%d-%m-%Y_%H:%M:%S"))+'@'+ secure_filename(file.filename)
    # save the file in the UPLOAD_FOLDER
    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))

    return "{'message': 'file has recieved', file_name="+filename+"}"

# Check method responsible for checking the number of files that are waiting to be printed
@app.route('/check', methods=['GET'])
@token_required
def _check():  
    # return the number of files in the to_print_files folder
    return "{'number_of_files': "+str(len(os.listdir(UPLOAD_FOLDER)))+"}"

if __name__ == "__main__":
    app.run(debug=debug, port=54321)