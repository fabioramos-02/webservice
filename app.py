from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('database.db')

@app.route('/')
def home():
    return "Welcome to the Python Web Service with SQLite!"

@app.route('/api/users', methods=['GET'])
def get_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    users = []
    for row in rows:
        users.append({"id": row[0], "name": row[1], "email": row[2]})
    return jsonify(users)

@app.route('/api/users', methods=['POST'])
def add_user():
    try:
        data = request.get_json()
        name = data['name']
        email = data['email']
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (name, email))
        conn.commit()
        conn.close()
        return jsonify({"message": "User added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    from database import init_db
    init_db()
    app.run(debug=True)
    