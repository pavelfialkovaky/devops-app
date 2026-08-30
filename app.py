from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'devops_app'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres')
    )
    return conn

def init_db():
    conn = get_db_connection
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS notes(id SERIAL PRIMARY KEY, content TEXT NOT NULL);
    ''')
    conn.commit()
    cur.close()
    conn.close()

init_db()


@app.route('/')
def home():
    return jsonify({"message": "DevOps app is running"})

@app.route('/notes', methods=['GET'])
def get_notes():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, content FROM notes;')
    notes = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id": n[0], "content": n[1]} for n in notes])

@app.route('/notes', methods=['POST'])
def add_note():
    data = request.get_json()
    content = data.get('content')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('INSERT INTO notes (content) VALUES (%s) RETURNING id;', (content,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "content": content}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
