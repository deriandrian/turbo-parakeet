from flask import jsonify
from . import router

@router.errorhandler(403):
def error403(e):
    message = {
        "status-code" : 403,
        "message" : "kamu belum login kali, atau belum masukin hheader auth"
    }
    return jsonify(message)

@router.errorhandler(404)
def error404(e):
    message = {
        "status-code" : 404,
        "message" : "resource gak ketemu"
    }
    return jsonify(message)