from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Load JSON data using absolute path (works from any folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(BASE_DIR, 'data.json')) as f:
    data = json.load(f)

# API 1: Get all data
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(data)

# API 2: Get student by ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    student = [s for s in data if s['id'] == id]
    return jsonify(student)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True, use_reloader=False)
