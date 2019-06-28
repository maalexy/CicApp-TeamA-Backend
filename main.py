import datetime
import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
import bcrypt

### Inits, setups
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.environ.get('CICAPP_BACKEND_JWT_SECRET',os.getrandom(16))
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=4)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
jwt = JWTManager(app)

# TODO: use database
all_passw = dict()
all_email = dict()
blacklist_jwt = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist_jwt

### Endpoints

@app.route('/helloworld')
def hello_world():
    return "HelloWorld"

# Parameters: username, password, email
# Parameters will be given through POST body form
@app.route('/register', methods=['POST'])
def register():
    usern = request.form['username']
    passw = request.form['password']
    email = request.form['email']
    pwhash = bcrypt.hashpw(passw.encode('utf-8'), bcrypt.gensalt())
    # TODO: use database
    global all_passw
    global all_email
    all_passw[usern] = pwhash.digest()
    all_email[usern] = email
    return jsonify(msg='Success'), 200


# Parameters: username, password
# Parameters will be given through POST body form
@app.route('/login', methods=['POST'])
def login():
    usern = request.form['username']
    passw = request.form['password']
    # TODO: use database
    global all_passw
    global all_email
    if usern not in all_passw.keys():
        return jsonify(msg='User not registered'), 401
    if bcrypt.checkpw(passw.encode('utf-8'), all_passw[usern]):
        return jsonify(msg='Bad creditentials'), 401
    token = create_access_token(identity=usern)
    return jsonify(msg='Success', token=token), 200


@app.route('/.dev/jwtecho')
@jwt_required
def jwtecho():
    return jsonify(msg='Success'), 200

# Requires authentication
# TODO: JWT token handling
@app.route('/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist_jwt.add(jti)
    return jsonify(msg='Success'), 200

### Main

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000))

