from flask import Flask, request, json, jsonify
import os

from . import router, questionsFileLocation, getQuiz
from ..utils.file import readFile, writeFile

# bikin soal untuk kuis yang udah ada
@router.route('/question', methods=['POST'])
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

    for question in quizData["question-list"]:
        if question["question-number"] == int(questionNumber):
            return jsonify(question)


@router.route('/quizzes/<quizId>/question/<questionNumber>', methods=["PUT", "DELETE"])
def updateDeleteQuestion(quizId, questionNumber):
    if request.method == "DELETE":
        return deleteQuestion(quizId, questionNumber)
    elif request.method == "PUT":
        return updateQuestion(quizId, questionNumber)

def deleteQuestion(quizId, questionNumber):
    
    questionData = readFile(questionsFileLocation)

    for i in range(len(questionData["questions"])):
        if questionData["questions"][i]["question-number"] == int(questionNumber):
            if questionData["questions"][i]["quiz-id"] == int(quizId):
                del questionData["questions"][i]
    
            break
            
    writeFile(questionsFileLocation, questionData)
    
    return jsonify(questionData)

def updateQuestion(quizId, questionNumber):
    body = request.json

    questionData = readFile(questionsFileLocation)

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

    writeFile(questionsFileLocation, questionData)

    return jsonify(questionData)