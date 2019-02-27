from flask import Flask, request, json, jsonify
import os

from . import router, usersFileLocation

from ..utils.crypt import encrypt, decrypt
from ..utils.file import readFile, writeFile
from ..utils.authorization import generateToken



# Register user
@router.route('/users', methods=['POST'])
def register():
    print(os.getenv("API_KEY"))
    body = request.json

    body["password"] = encrypt(body["password"])

    userData = {
        "userList": []
    }

    if os.path.exists(usersFileLocation):
        userData = readFile(usersFileLocation)

    userData["userList"].append(body)

    writeFile(usersFileLocation, userData)

    return jsonify(userData)


# Login user
@router.route('/users/login', methods=["POST"])
def login():
    body = request.json

    userData = readFile(usersFileLocation)

    status = False
    # cari user yang udah register 
    for i in range(len(userData["userList"])):
        registeredUser = userData["userList"][i]
        if registeredUser["username"] == body["username"]:
            if decrypt(registeredUser["password"]) == body["password"]:
                status = True
                body["token"] = generateToken(body["username"])
                break
            else:
                status = False

    return jsonify(body)
