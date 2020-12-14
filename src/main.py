"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from datetime import datetime
from flask_jwt_simple import (
    JWTManager, jwt_required, create_jwt, get_jwt_identity
)

#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Simple extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)

# Provide a method to create access tokens. The create_jwt()
# function is used to actually generate the token
#autheticates the login
@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    usercheck = User.query.filter_by(email=email, password=password).first()
    if usercheck == None:
        return jsonify({"msg": "Bad username or password"}), 401
    
    # Identity can be any data that is json serializable
    ret = {'jwt': create_jwt(identity=email)}
    return jsonify(ret), 200

#creating a new user registration 
@app.route('/user', methods=['POST', 'GET'])
def handle_user():
    """
    Create user and retrieve all users
    """
    # POST request - creates new user
    if request.method == 'POST':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)    
        user1 = User(email=body['email'], password=body['password'], first_name=body['first_name'], last_name=body['last_name'], birth_date=body['birth_date'], created_date=body['created_date'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request - shows all users 
    if request.method == 'GET':
        all_people = User.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404

@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
        get_user = User.query.get(user_id)
        return jsonify(get_user.serialize()), 200

# update user by id
@app.route('/user/<int:user_id>', methods=['PUT'])
def update_info(user_id):
        request_body= request.get_json()
        user_1 = User.query.get(user_id)
        if "email" in request_body:
            user_1.email = request_body["email"]
        if "password" in request_body:
            user_1.password = request_body["password"]
        if "first_name" in request_body:
            user_1.first_name = request_body["first_name"]
        if "last_name" in request_body:
            user_1.last_name = request_body["last_name"]
        if "birth_date" in request_body:
            user_1.birth_date = request_body["birth_date"]
        db.session.commit()
        return jsonify(user_1.serialize()), 200 


# deletes by id
@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_info(user_id):
        request_body= request.get_json()
        print(request_body)
        user_to_delete = User.query.get(user_id)
        if user_to_delete is None:
            raise APIException('User not found', status_code=404)
        else:
            db.session.delete(user_to_delete)
            db.session.commit()
            return jsonify(user_to_delete.serialize()), 204


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
