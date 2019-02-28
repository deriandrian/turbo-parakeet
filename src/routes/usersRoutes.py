from flask import Flask, request, json, jsonify
import os

from . import router, usersFileLocation

from ..utils.crypt import encrypt, decrypt
from ..utils.file import readFile, writeFile
from ..utils.authorization import generateToken



# Register user
@router.route('/users', methods=['POST'])
def register():
    isUsernameOrEmailUsed = False
    body = request.json

    response = {
        "error" : True
    }


    userData = {
        "total-user-registered": 0,
        "userList" : []
    }

    try:
        userData = readFile(usersFileLocation)
    except:
        print("file tidak ada")
    else:
        for data in userData["userList"]:
            if data["username"] == body["username"] or data["email"] == body["email"]:
                isUsernameOrEmailUsed = True
    
    if not isUsernameOrEmailUsed:
        userData["total-user-registered"] += 1
        body["password"] = encrypt(body["password"])
        userData["userList"].append(body)
        
        response["data"] = body
        writeFile(usersFileLocation, userData)
    else:
        del body["password"]
        response["message"] = "username or email is used"

    return jsonify(response)


# Login user
@router.route('/users/login', methods=["POST"])
def login():
    body = request.json

    userData = readFile(usersFileLocation)

    status = False
    # cari user yang udah register 
    for user in userData["userList"]:
        if user["username"] == body["username"]:
            if decrypt(user["password"]) == body["password"]:
                status = True
                body["token"] = generateToken(body["username"])
                break
    body["status"] = status
    if status:
        body["message"] = "Good Work"
    else:
        body["message"] = "username atau password salah"

    return jsonify(body)
