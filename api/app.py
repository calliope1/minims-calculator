# Flask server
# app.py
from flask import Flask, request
import server.server as server

app = Flask(__name__)


@app.route('/compute', methods=['GET'])
def compute_minims():
    return server.return_minims(request)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4999, debug=True)