import os
from flask import Flask, request
from hashlib import sha256
app = Flask(__name__)

@app.route('/helloworld')
def hello_world():
    return "HelloWorld"

# TODO: use database
all_passw = {}
all_email = {}

# Parameters: username, password, email
# Parameters will be given through POST body form
@app.route('/register', methods=['POST'])
def register():
    usern = request.form['username']
    passw = request.form['password']
    email = request.form['email']
    pwhash = sha256()
    pwhash.update(bytes(passw, 'utf-8'))
    # TODO: use database
    global all_passw
    global all_email
    all_passw[usern] = pwhash.digest()
    all_email[usern] = pwhash.digest()
    return ''


# Parameters: username, password
# Parameters will be given through POST body form
@app.route('/login', methods=['POST'])
def login():
    usern = request.form['username']
    passw = request.form['password']
    pwhash = sha256()
    pwhash.update(bytes(passw, 'utf-8'))
    # TODO: use database
    global all_passw
    global all_email
    if usern not in all_passw.keys():
        return 'User not registered', 401
    if all_passw[usern] != pwhash.digest():
        return 'Bad creditentials', 401
    # TODO: JWT token handling
    return 'OKITOKI', 200

# Requires authentication
# TODO: JWT token handling
@app.route('/logout', methods=['POST'])
def logout():
    if True: # test token authenticity
        # get JWT token from auth, and disable it...
        return '', 200
    else:
        return 'Bad token', 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))