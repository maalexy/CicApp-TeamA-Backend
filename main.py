import os
from flask import Flask, request
from hashlib import sha256
app = Flask(__name__)

@app.route('/helloworld')
def hello_world():
    app.logger.info('HELLO LOG')
    return "HelloWorld"

# TODO: use database
all_passw = {}
all_email = {}

# Parameters: username, password, email
# Parameters will be given through POST body form
@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.info(request.form)
    app.logger.info('HERE I AM')
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
    if all_passw[usern] == pwhash.digest():
        # TODO: JWT token handling
        return 'OKITOKI', 200
    else:
        return 'NOPE', 401

# Requires authentication
# TODO: JWT token handling
@app.route('/logout', methods=['POST'])
def logout():
    # get JWT token from auth, and disable it...
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))