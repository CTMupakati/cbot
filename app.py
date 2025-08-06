from flask import Flask, request, jsonify
from flask_cors import CORS  # ← ADD THIS LINE
import json

app = Flask(__name__)
CORS(app)  # ← ADD THIS LINE TO ENABLE CORS FOR ALL ROUTES

# Load your JSON data
with open('data.json') as f:
    data = json.load(f)

@app.route('/query', methods=['POST'])
def query():
    req = request.json
    category = req.get('category', '').lower()
    response = {}

    for record in data:
        if record['CRIME CATEGORY'].lower() == category:
            response = record
            break

    if response:
        return jsonify({"status": "success", "data": response})
    else:
        return jsonify({"status": "error", "message": "Category not found"}), 404

if __name__ == '__main__':
    app.run()
