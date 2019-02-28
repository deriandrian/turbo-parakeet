from flask import Flask, request, json, jsonify, abort
import os

from . import router, questionsFileLocation, getQuiz
from ..utils.file import readFile, writeFile
from ..utils.authorization import verifyLogin

# bikin soal untuk kuis yang udah ada
@router.route('/question', methods=['POST'])
@verifyLogin
def createQuestion():
    body = request.json

    questionData = {
        "questions": []
    }

    if os.path.exists(questionsFileLocation):
        questionData = readFile(questionsFileLocation)
    
    questionData["questions"].append(body)

    writeFile(questionsFileLocation, questionData)

    return jsonify(questionData)


# minta data sebuah soal untuk kuis tertentu
@router.route('/quizzes/<quizId>/questions/<questionNumber>')
def getThatQuestion(quizId, questionNumber):
    quizData = getQuiz(int(quizId)).json

    try:
        for question in quizData["data"]["question-list"]:
            if question["question-number"] == int(questionNumber):
                return jsonify(question)
        raise Exception("Soal Gaadeu")
    except ValueError:
        abort(404)
    except TypeError:
        abort(403)
    except Exception:
        abort(404)

@router.route('/quizzes/<quizId>/questions/<questionNumber>', methods=["PUT", "DELETE"])
def updateDeleteQuestion(quizId, questionNumber):
    if request.method == "DELETE":
        return deleteQuestion(quizId, questionNumber)
    elif request.method == "PUT":
        return updateQuestion(quizId, questionNumber)

def deleteQuestion(quizId, questionNumber):
    
    questionData = readFile(questionsFileLocation)

    questionToBeDeleted = getThatQuestion(int(quizId), int(questionNumber)).json # ambil dari fungsi getThatQuestion

    for i in range(len(questionData["questions"])):
        if questionData["questions"][i] == questionToBeDeleted:
            del questionData["questions"][i]
    
            break
            
    writeFile(questionsFileLocation, questionData)
    
    return jsonify(questionData)

def updateQuestion(quizId, questionNumber):
    body = request.json

    questionData = readFile(questionsFileLocation)

    questionToBeUpdated = getThatQuestion(int(quizId), int(questionNumber)).json # ambil dari fungsi getThatQuestion

    for i in range(len(questionData["questions"])):
        if questionData["questions"][i] == questionToBeUpdated:
                questionData["questions"][i]["question-number"] = body["question-number"]
                questionData["questions"][i]["question"] = body["question"]
                questionData["questions"][i]["answer"] = body["answer"]
                questionData["questions"][i]["option-list"]["A"] = body["option-list"]["A"]
                questionData["questions"][i]["option-list"]["B"] = body["option-list"]["B"]
                questionData["questions"][i]["option-list"]["C"] = body["option-list"]["C"]
                questionData["questions"][i]["option-list"]["D"] = body["option-list"]["D"]
                break

    writeFile(questionsFileLocation, questionData)

    return jsonify(questionData)