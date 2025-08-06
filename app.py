from flask import Flask, request, jsonify
import json

app = Flask(__name__)

# Load the JSON file
with open('data.json') as f:
    data = json.load(f)

@app.route('/query', methods=['POST'])
def query():
    req = request.json
    category = req.get('category', '').lower()
    response = {}

    # Search the JSON for matching crime category
    for record in data:
        if record['CRIME CATEGORY'].lower() == category:
            response = record
            break

    if response:
        return jsonify({"status": "success", "data": response})
    else:
        return jsonify({"status": "error", "message": "Crime category not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
