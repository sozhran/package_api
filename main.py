from flask import Flask, request, jsonify
from flask_cors import CORS
from status_parser import status_parser
import logging
from dotenv import load_dotenv

logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return ('', 200)

@app.get('/list')
def list():
    package_data = status_parser(filepath)
    packages = [x['package'] for x in package_data]
    return jsonify(packages)
    
@app.get('/package/<package_name>')
def get_package(package_name):
    package_data = status_parser(filepath)
    package_finder = [d for d in package_data if d['package'] == package_name]
    if package_finder:
        response = jsonify(package_finder)
        return response

if __name__ == "__main__":
    app.run(debug=True)