from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask import session
from pymongo import MongoClient
import requests
from uuid import uuid4
# MongoDB-ga bog'lanish
client = MongoClient('mongodb://localhost:27017/')
db = client['admin']
collection = db['users']
users = collection.find()

app = Flask(__name__)
app.secret_key = "app.secret_key" 








# Registratsiya API (POST /register)
@app.route('/register', methods=['POST'])
def register():
    # POST orqali kelayotgan ma'lumotlar
    username = request.json['name']
    email = request.json['email']
    password = request.json['password']

    user = collection.find_one({'username': username})
    if user:
            return jsonify({"message": "Invalid credentials"}), 401
        
    collection.insert_one({'username': username, 'email':  email, 'password': password})

        # Foydalanuvchilarni MongoDB-dan olish
    user = collection.find()
    return jsonify({"message": "Successful"}), 201




# Login API (POST /login)
@app.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    user = collection.find_one({'email': email, 'password': password})
        
    if user and user['password'] == password:
        session['email'] = email
        return jsonify({"message": "Successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401
    
    

# Foydalanuvchilarni olish API (GET /users)
@app.route('/users', methods=['GET'])
def get_users():
    all_users = users.find()
    users_list = []

    for user in all_users:
        users_list.append({            
            'name': user['name'],
            'email': user['email']
        })

    return jsonify(users_list), 200

# Foydalanuvchini yangilash API (PATCH /users/<id>)
@app.route('/users/<id>', methods=['PATCH'])
def update_user(id):
    # Yangilanishi kerak bo'lgan ma'lumotlar
    name = request.json.get('name')
    email = request.json.get('email')

    # Foydalanuvchini yangilash
    users.update_one({ '$set': {
        'name': name,
        'email': email
    }})
    
    return jsonify({"message": "User updated successfully"}), 200



# Flask ilovasini ishga tushirish
if __name__ == '__main__':
    app.run(debug=True)