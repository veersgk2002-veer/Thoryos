from flask import Flask, render_template, request, jsonify, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'super_secret_key_change_me' # Change this for security
STORAGE_PATH = 'vault_data'

if not os.path.exists(STORAGE_PATH):
    os.makedirs(STORAGE_PATH)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/auth', methods=['POST'])
def auth():
    if request.json.get('password') == 'YOUR_MASTER_KEY':
        session['logged_in'] = True
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 401

@app.route('/api/files', methods=['GET'])
def get_files():
    if not session.get('logged_in'): return jsonify({"status": "unauthorized"}), 401
    return jsonify({"files": os.listdir(STORAGE_PATH)})

@app.route('/api/upload', methods=['POST'])
def upload():
    if not session.get('logged_in'): return jsonify({"status": "unauthorized"}), 401
    file = request.files['file']
    if file:
        file.save(os.path.join(STORAGE_PATH, secure_filename(file.filename)))
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 400

@app.route('/api/delete', methods=['POST'])
def delete():
    if not session.get('logged_in'): return jsonify({"status": "unauthorized"}), 401
    filename = request.json.get('filename')
    path = os.path.join(STORAGE_PATH, filename)
    if os.path.exists(path):
        os.remove(path)
        return jsonify({"status": "success"})
    return jsonify({"status": "error"}), 404

if __name__ == '__main__':
    app.run()
