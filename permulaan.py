# from flask import Flask, request
# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Bismillahirrahmaanirrahiim"

# @app.route('/deri')
# def deri():
#     return "Gaskenn Mamang"

# @app.route('/summation/<firstNum>/<secondNum>')
# def summation(firstNum, secondNum):
#     firstNum = int(firstNum)
#     secondNum = int(secondNum)

#     result = firstNum + secondNum
#     return str(result)

# @app.route('/summation')
# def summation2():
#     firstNum = request.args.get('firstNum')
#     secondNum = request.args.get('secondNum')

#     numb1 = int(firstNum)
#     numb2 = int(secondNum)

#     result = numb1 + numb2
#     return str(result)

from flask import Flask, request, json, jsonify
from random import randint
import requests
import os
app = Flask(__name__)


# bikin kuis baru
@app.route('/quiz', methods=['POST'])
def createQuiz():
    body = json.dumps(request.json)

    quizData = {
        "totalQuizAvailable": 0,
        "quizzes": []
    }

    if os.path.exists('./quizzes-file.json'):
        quizzesFile = open('./quizzes-file.json', 'r')
        quizData = json.load(quizzesFile)
    else:
        quizzesFile = open('./quizzes-file.json', 'x')

    quizData["totalQuizAvailable"] += 1
    quizData["quizzes"].append(body)

    quizzesFile = open('./quizzes-file.json', 'w')
    quizzesFile.write(str(json.dumps(quizData)))

    return str(quizData)

# bikin soal untuk kuis yang udah ada
@app.route('/question', methods=['POST'])
def createQuestion():
    body = json.dumps(request.json) #untuk merubah dari ('') menjadi ("")

    questionData = {
        "questions": []
    }

    if os.path.exists('./question-file.json'):
        questionFile = open('./question-file.json', 'r')
        print("File ada")
        questionData = json.load(questionFile)
    else:
        questionFile = open('./question-file.json', 'x')
        print("file ga ada") 

    questionFile = open('./question-file.json', 'w')
    questionData["questions"].append(body)
    questionFile.write(str(json.dumps(questionData)))

    return str(questionData)

# meminta data kuis dan soalnya
@app.route('/quizzes/<quizId>') #kalau gaada methodnya itu defaulnya ["GET"]
def getQuiz(quizId):
    # nyari quiznya
    quizzesFile = open('./quizzes-file.json')
    quizzesData = json.load(quizzesFile) #kalo load itu dari file

    for quiz in quizzesData["quizzes"]:
        quiz = json.loads(quiz) #sedangkan loads itu dari string
        if quiz["quiz-id"] == int(quizId):
            quizData = quiz
            break

    # nyari soalnya
    questionsFile = open('./question-file.json')
    questionsData = json.load(questionsFile)

    for question in questionsData["questions"]:
        question = json.loads(question)
        if question["quiz-id"] == int(quizId):
            quizData["question-list"].append(question)

    return jsonify(quizData)

# minta data sebuah soal untuk kuis tertentu
@app.route('/quizzes/<quizId>/questions/<questionNumber>')
def getThatQuestion(quizId, questionNumber):
    quizData = getQuiz(int(quizId)).json

    for question in quizData["question-list"]:
        if question["question-number"] == int(questionNumber):
            return jsonify(question)


# bikin game baru
@app.route('/game', methods=["POST"])
def createGame():
    body = request.json

    # dapetin info quiz
    quizzesFile = open('./quizzes-file.json')
    quizzesData = json.load(quizzesFile)

    for quiz in quizzesData["quizzes"]:
        quiz = json.loads(quiz)

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
    if os.path.exists('./games-file.json'):
        gamesFile = open('./games-file.json', 'r')
        gamesData = json.load(gamesFile)
    else:
        gamesFile = open('./games-file.json', 'x')

    with open('./games-file.json', 'w') as gamesFile:
        gamesData["game-list"].append(gameInfo)
        gamesFile.write(str(json.dumps(gamesData)))

    return jsonify(gameInfo)


@app.route('/game/join', methods=["POST"])
def joinGame():
    body = request.json

    # open game data information
    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)

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

    with open('./games-file.json', 'w') as gamesFile:
        gamesData["game-list"][position] = gameInfo
        gamesFile.write(str(json.dumps(gamesData)))

    return jsonify(request.json)


# ```
# 1. harus ada soalnya
# 2. ada pilihan jawabannya
# 3. identitas soalnya jelas
# 4. yang jawabnya juga tau siapa
# 5. si jawabannya
# 6. pin game nya
# ```

@app.route('/game/answer', methods=["POST"])
def submitAnswer():
    isTrue = False
    body = request.json

    # buka file question
    questionsFile = open('./question-file.json')
    questionsData = json.load(questionsFile)

    for question in questionsData["questions"]:
        question = json.loads(question)

        if question["quiz-id"] == int(body["quiz-id"]) and question["question-number"] == int(body["question-number"]):
            if question["answer"] == body["answer"]:
                isTrue = True


    # TODO : update skor/Leaderboard
    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)

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

    with open('./games-file.json', 'w') as gamesFile:
        gamesData["game-list"][gamePosition] = gameInfo
        gamesFile.write(str(json.dumps(gamesData)))
  

    return jsonify(request.json)

@app.route('/game/leaderboard', methods=["POST"])
def getLeaderboard():
    body = request.json
 
    gamesFile = open('./games-file.json')
    gamesData = json.load(gamesFile)

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

@app.route('/register', methods=["POST"])
def register():
    body = request.json

    if body["todo"] == "encrypt":
        body["password"] = encrypt(body["password"])
    elif body["todo"] == "decrypt":
        body["password"] = decrypt(body["password"])


    userData = {
        "listUser" : []
    }

    if os.path.exists('./users-file.json'):
        userFile = open('./users-file.json', 'r')
        userData = json.load(userFile)
        
        result = ''
        position = -1
        for i in range(len(userData["listUser"])):
            user = userData["listUser"][i]
            if user["username"] == body["username"]:
                print("username sudah ada")
                result = "maaf kakak namanya sudah ada yang make"
                position = i
                break
            if user["email"] == body["email"]:
                print("email sudah ada")
                result = "maaf kakak emailnya sudah ada yang make"
                position = i 
                break
        if position == -1:
            userFile = open('./users-file.json', 'w')      
            userData["listUser"].append(body)
            userFile.write(str(json.dumps(userData)))
            result = jsonify(userData)
        else:
            result = result
    
    else:
        userFile = open('./users-file.json', 'x')     
        userFile = open('./users-file.json', 'w')      
        userData["listUser"].append(body)
        userFile.write(str(json.dumps(userData)))
        result = jsonify(userData)

    return result

@app.route('/login', methods=["POST"])
def login():
    body = request.json

    if body["todo"] == "encrypt":
        body["password"] = encrypt(body["password"])
    elif body["todo"] == "decrypt":
        body["password"] = decrypt(body["password"])  

    # buka file question
    userFile = open('./users-file.json')
    userData = json.load(userFile)

    result = ''
    position = -1
    for i in range(len(userData["listUser"])):
        user = userData["listUser"][i]
        if user["username"] == body["username"]:
            position = i
            if user["password"] == body["password"]:
                print("anda sudah masuk")
                result = "welcome back"
                break
            else :
                result = "yang bener dong nulis passwordnya"
    if position == -1:
        result = "berani-beraninya kamu belum registrasi tapi mau masuk!"

    return result

defaultCaesarMove = 2
def encrypt(string):
    caesarMove = defaultCaesarMove
    alphabet = 'abcdefghijkhlmnopqrstuvwxyz'
    number = '0123456789'
    initial = alphabet+number
    listInitial = list(initial)
    allMove = len(listInitial)
  
    listString = list(string)     
    for i in range(len(listString)) :
        tobe = listInitial.index(listString[i])
        en = (tobe + caesarMove) % allMove
        listString[i] = listInitial[en]
    
    return ''.join(listString)

def decrypt(string):
    caesarMove = defaultCaesarMove
    alphabet = 'abcdefghijkhlmnopqrstuvwxyz'
    number = '0123456789'
    initial = alphabet+number
    listInitial = list(initial)
    allMove = len(listInitial)
    
    listString = list(string)  
    for i in range(len(listString)) :
        tobe = listInitial.index(listString[i])
        en = (tobe - caesarMove) % allMove
        listString[i] = listInitial[en]
        
    return ''.join(listString)

#update dan delete quiz
@app.route('/quizzes/<quizId>', methods=["DELETE"])
def deleteQuiz(quizId):
    
    # nyari quiznya
    quizzesFile = open('./quizzes-file.json')
    quizzesData = json.load(quizzesFile) 

    for i in range(len(quizzesData["quizzes"])):
        if quizzesData["quizzes"][i]["quiz-id"] == int(quizId):
            quizzesData["quizzes"].pop(i)
            quizzesData["total-quiz-available"] -= 1
            break


    with open('./quizzes-file.json', 'w') as quizzesFile:
        quizzesFile.write(str(json.dumps(quizzesData)))

    return jsonify(quizzesData)

@app.route('/quizzes/<quizId>', methods=["PUT"])
def upadateQuiz(quizId):
    body = request.json
    
    quizzesFile = open('./quizzes-file.json')
    quizzesData = json.load(quizzesFile) 

    for i in range(len(quizzesData["quizzes"])):
        if quizzesData["quizzes"][i]["quiz-id"] == int(quizId):
            quizzesData["quizzes"][i]["quiz-category"] = body["quiz-category"]
            quizzesData["quizzes"][i]["quiz-name"] = body["quiz-name"]
            break

    with open('./quizzes-file.json', 'w') as quizzesFile:
        quizzesFile.write(str(json.dumps(quizzesData)))

    return jsonify(quizzesData)

@app.route('/quizzes/<quizId>/question/<questionNumber>', methods=["DELETE"])
def deleteThatQuestion(quizId, questionNumber):
    
    # nyari quiznya
    questionFile = open('./question-file.json')
    questionData = json.load(questionFile) 

    for i in range(len(questionData["questions"])):
        if questionData["questions"][i]["question-number"] == int(questionNumber):
            if questionData["questions"][i]["quiz-id"] == int(quizId):
                del questionData["questions"][i]
    
            break


    with open('./question-file.json', 'w') as questionFile:
        questionFile.write(str(json.dumps(questionData)))

    return jsonify(questionData)

@app.route('/quizzes/<quizId>/question2/<questionNumber>', methods=["PUT"])
def updateThatQuestion(quizId, questionNumber):
    body = request.json

    # nyari quiznya
    questionFile = open('./question-file.json')
    questionData = json.load(questionFile) 

    for i in range(len(questionData["questions"])):
        if questionData["questions"][i]["question-number"] == int(questionNumber):
            if questionData["questions"][i]["quiz-id"] == int(quizId):
                questionData["questions"][i]["question-number"] = body["question-number"]
                questionData["questions"][i]["question"] = body["question"]
                questionData["questions"][i]["answer"] = body["answer"]
                questionData["questions"][i]["option-list"]["A"] = body["option-list"]["A"]
                questionData["questions"][i]["option-list"]["B"] = body["option-list"]["B"]
                questionData["questions"][i]["option-list"]["C"] = body["option-list"]["C"]
                questionData["questions"][i]["option-list"]["D"] = body["option-list"]["D"]
                
            break


    with open('./question-file.json', 'w') as questionFile:
        questionFile.write(str(json.dumps(questionData)))

    return jsonify(questionData)



if __name__ == "__main__":
    app.run(debug=True, port=14045)