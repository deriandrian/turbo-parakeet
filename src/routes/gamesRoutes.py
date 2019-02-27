from flask import Flask, request, json, jsonify
from random import randint
import os

from . import router, quizzesFileLocation, gamesFileLocation, questionsFileLocation
from ..utils.file import readFile, writeFile

# bikin game baru
@router.route('/game', methods=["POST"])
def createGame():
    body = request.json

    # dapetin info quiz
    # quizzesFile = open(quizzesFileLocation)
    # quizzesData = json.load(quizzesFile)
    quizzesData = readFile(quizzesFileLocation)

    for quiz in quizzesData["quizzes"]:
        # quiz = json.loads(quiz)

        if quiz["quiz-id"] == int(body["quiz-id"]):
            gameInfo = quiz

    gameInfo["game-pin"] = randint(100000, 999999)
    gameInfo["user-list"] = []
    gameInfo["leaderboard"] = []

    # create skeleton for list of game buat nulis 
    # kalau belum pernah main game sama sekali
    gamesData = {
        "game-list": []
    }

    # simpen data game nya
    if os.path.exists(gamesFileLocation):
        gamesData = readFile(gamesFileLocation)

    gamesData["game-list"].append(gameInfo)

    writeFile(gamesFileLocation, gamesData)

    return jsonify(gameInfo)


@router.route('/game/join', methods=["POST"])
def joinGame():
    body = request.json

    # open game data information
    gamesData = readFile(gamesFileLocation)

    position = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == int(body["game-pin"]):
            if body["username"] not in game["user-list"]:
                game["user-list"].append(body["username"])
                game["leaderboard"].append({
                    "username": body["username"],
                    "score": 0
                })
                gameInfo = game
                position = i
                break
            # TODO: error kalau usernya udah dipake

    gamesData["game-list"][position] = gameInfo

    writeFile(gamesFileLocation, gamesData)

    return jsonify(gameInfo)

@router.route('/game/answer', methods=["POST"])
def submitAnswer():
    isTrue = False
    body = request.json

    # buka file question
    questionsData = readFile(questionsFileLocation)

    for question in questionsData["questions"]:
        # question = json.loads(question)

        if question["quiz-id"] == int(body["quiz-id"]) and question["question-number"] == int(body["question-number"]):
            if question["answer"] == body["answer"]:
                isTrue = True


    # TODO : update skor/Leaderboard
    gamesData = readFile(gamesFileLocation)

    gamePosition = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == body["game-pin"]:
            if isTrue:
                userPosition = 0
                for j in range(len(game["leaderboard"])):
                    userData = game["leaderboard"][j]
                
                    if userData["username"] == body["username"]:
                        userData["score"] += 100
                        print(userData)               

                        userInfo = userData
                        userPosition = j
                        break

                game["leaderboard"][userPosition] = userInfo
                gameInfo = game
                gamePosition = i
                break

    gamesData["game-list"][gamePosition] = gameInfo

    writeFile(gamesFileLocation, gamesData)

    return jsonify(request.json)

@router.route('/game/leaderboard', methods=["POST"])
def getLeaderboard():
    body = request.json

    gamesData = readFile(gamesFileLocation)

    for game in gamesData["game-list"]:
        if game["game-pin"] == body["game-pin"]:
            leaderboard = game["leaderboard"]

    i = 0
    while (i < len(leaderboard)):
        for j in range(len(leaderboard)-i-1):
            if (leaderboard[j]["score"] < leaderboard[j+1]["score"]):      
                leaderboard[j+1], leaderboard[j] = leaderboard[j], leaderboard[j+1]
        i += 1

    return jsonify(leaderboard)