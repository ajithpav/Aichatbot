from flask import Flask, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import hashlib  # for password hashing

app = Flask(__name__)

MONGO_URL = "mongodb+srv://ajith63073:zBtqgjXMPwU27XHA@vectordb.udkncxz.mongodb.net/"
MONGO_DBNAME = "sample_mflix"
COLLECTION = "users"  # Change to the correct collection name

app.config["MONGO_URI"] = MONGO_URL
mongo = PyMongo(app)

@app.route('/login', methods=['POST'])
@app.route('/logng',methods=['Post'])
def login():
    user_data = request.get_json()
    user_email = user_data.get('email')
    user_password = hashlib.sha256(user_data.get('password').encode()).hexdigest()  # Hash the password

    # Check if the user exists in the database
    user = mongo.db[COLLECTION].find_one({'email': user_email, 'password': user_password})

    if user:
        # If the user exists, store the user information in the session
        session['user_id'] = str(user['_id'])
        return {'message': 'Login successful'}, 200
    else:
        return {'message': 'Invalid email or password'}, 401

# Define a function to insert a new user
def insert_user(user_data):
    user_data['password'] = hashlib.sha256(user_data['password'].encode()).hexdigest()  # Hash the password
    user_id = mongo.db[COLLECTION].insert_one(user_data).inserted_id
    return str(user_id)

# Define a function to get a user by id
def get_user_by_id(user_id):
    user = mongo.db[COLLECTION].find_one({'_id': ObjectId(user_id)})
    return user

# Define a function to update a user
def update_user(user_id, user_data):
    mongo.db[COLLECTION].update_one({'_id': ObjectId(user_id)}, {'$set': user_data})

# Define a function to delete a user
def delete_user(user_id):
    mongo.db[COLLECTION].delete_one({'_id': ObjectId(user_id)})

if __name__ == '__main__':
    app.run(debug=True)
