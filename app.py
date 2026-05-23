from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
STORAGE_PATH = 'vault_data'
if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/files', methods=['GET'])
def get_files():
    files = os.listdir(STORAGE_PATH)
    return jsonify({"files": files})

@app.route('/api/delete', methods=['POST'])
def delete():
    data = request.json
    filename = data.get('filename')
    file_path = os.path.join(STORAGE_PATH, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"status": "deleted"})
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    app.run()
