from flask import request, json, jsonify, g
import os

from . import router, quizzesFileLocation, questionsFileLocation
from ..utils.file import readFile, writeFile
from ..utils.authorization import verifyLogin

# bikin kuis baru
@router.route('/quizzes', methods=['POST'])
@verifyLogin
def createQuiz():
    body = request.json
    print("usernamenya adalah", g.username)

    quizData = {
        "total-quiz-available": 0,
        "quizzes": []
    }    

    if os.path.exists(quizzesFileLocation) and os.path.getsize(quizzesFileLocation) > 0:
        quizData = readFile(quizzesFileLocation)

    quizData["total-quiz-available"] += 1
    quizData["quizzes"].append(body)

    writeFile(quizzesFileLocation, quizData)

    return jsonify(quizData)

# meminta data kuis dan soalnya
@router.route('/quizzes/<quizId>')
def getQuiz(quizId):
    # nyari quiznya
    quizzesData = readFile(quizzesFileLocation)

    quizFound = False
    for quiz in quizzesData["quizzes"]:
        if quiz["quiz-id"] == int(quizId):
            quizData = quiz
            quizFound = True
            break

    if not quizFound:
        return jsonify("quiz-id " + str(quizId) + " tidak ditemukan")
    # nyari soalnya
    questionData = readFile(questionsFileLocation)

    for question in questionData["questions"]:
        if question["quiz-id"] == int(quizId):
            quizData["question-list"].append(question)

    return jsonify(quizData)

# delete quis sama ubah informasi tentang kuisnya
@router.route('/quizzes/<quizId>', methods=["PUT", "DELETE"])
def updateDeleteQuiz(quizId):
    if request.method == "DELETE":
        return deleteQuiz(quizId)
    elif request.method == "PUT":
        return updateQuiz(quizId)

# fungsi hapus quiz berdasarkan quiz-id
def deleteQuiz(quizId):
    quizData = readFile(quizzesFileLocation)

    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]

        if quiz["quiz-id"] == int(quizId): # nyari indeks quiz yg akan dihapus
            del quizData["quizzes"][i] # hapus quiz
            quizData["total-quiz-available"] -= 1 # kurangi total quiz
            # message = "Berhasil menghapus quiz id " + quizId
            break
        # else:
        #     message = "Gagal menghapus. Tidak ada quiz-id " + quizId

    # save ke file
    writeFile(quizzesFileLocation, quizData)

    # nyari question sesuai quiz-id lalu hapus 
    questionData = readFile(questionsFileLocation)

    # message2 = ""
    # looping ini sisa 1 question dg quiz-id sama, belum bisa semua hapus dalam 1 for(karena out of range)
    for i in range(len(questionData["questions"])):
        if i < len(questionData["questions"]):
            question = questionData["questions"][i]

            if question["quiz-id"] == int(quizId):
                del questionData["questions"][i]
                # message2 = " dan menghapus semua questionnya "

    # looping untuk hapus 1 question sisa
    for j in range(i-2,len(questionData["questions"])):
        question = questionData["questions"][j]

        if question["quiz-id"] == int(quizId):
            del questionData["questions"][j]
            # message2 = " dan menghapus semua questionnya "
            break

    writeFile(questionsFileLocation, questionData)

    return jsonify(quizData)

# fungsi ubah quiz berdasarkan quiz-id
def updateQuiz(quizId):
    body = request.json
    
    quizData = readFile(quizzesFileLocation)

    # pake spread
    # quizData = {
    #     **json.loads(quizData["quizzes"]),
    #     **body
    # }

    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]

        if quiz["quiz-id"] == int(quizId): # nyari indeks quiz yg akan didelete
            quiz["quiz-id"] = body["quiz-id"] # hapus line ini kalau quiz-id ga bisa diubah
            quiz["quiz-name"] = body["quiz-name"]
            quiz["quiz-category"] = body["quiz-category"]
            
            quizData["quizzes"][i] = quiz
            # message = "Berhasil mengubah quiz id " + quizId
            break
        # else:
        #     message = "Gagal mengubah. Tidak ada quiz-id " + quizId

    writeFile(quizzesFileLocation, quizData)

    return jsonify(quizData)