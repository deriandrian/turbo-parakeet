from flask import Flask, request, json, jsonify,abort
import jwt
from src.routes import router

app = Flask(__name__)
app.register_blueprint(router)

@app.route('/encode')
def jwtEncode():
    encoded = jwt.encode({"data": "makers"}, "kucing-merah", algorithm="HS256")
    return encoded

@app.route('/decode', methods=["POST"])
def jwtDecode():
    decoded = jwt.decode(request.json["token"], "kucing-merah", algorithms=["HS256"])
    return str(decoded)

@app.route('/ngetesaborsi')
def ngetesaborsi():
    abort(404)

@app.errorhandler(404)
def errorhandler404(e):
    return "error 404 JOW"