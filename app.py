from flask import Flask, send_from_directory
from flask_cors import CORS
from api import api
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# Register blueprint
app.register_blueprint(api)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
