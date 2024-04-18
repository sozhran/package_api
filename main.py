from flask import Flask, request, jsonify
from flask_cors import CORS
from parser import parser
logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return ('', 200)

@app.get('/list')
def list():
    package_data = parser()
    packages = [x['Package'] for x in package_data]
    return jsonify(packages)
    
@app.get('/package/<package_name>')
def get_package(package_name):
    package_data = parser()
    package_finder = [d for d in package_data if d['Package'] == package_name]
    if package_finder:
        response = jsonify(package_finder)
        return response

if __name__ == "__main__":
    app.run(debug=True)