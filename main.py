import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from status_parser import status_parser
from dotenv import load_dotenv

load_dotenv()

filepath = os.getenv('FILEPATH', './status')

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return ('', 200)

@app.get('/list')
def list():
    package_data = status_parser(filepath)
    packages = [x['package'] for x in package_data]
    if packages:
        response = jsonify(packages)
        return response
    
@app.get('/package/<package_name>')
def get_package(package_name):
    package_data = status_parser(filepath)
    package_finder = [d for d in package_data if d['package'] == package_name]
    if package_finder:
        response = jsonify(package_finder)
        return response

if __name__ == "__main__":
    app.run(debug=True)