import chatbot
from flask import Flask, render_template, request, redirect
from jinja2 import Environment, FileSystemLoader, Template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['WEEK00_TEAM7']
collection = db['A']
collection2 = db['B']
collection3 = db['C']

@app.route('/')
def loginRender():
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def registerRender():
    #GET
    if request.method == "POST":
        return render_template("login.html")
    else :
        return render_template("register.html")

@app.route('/main', methods=["GET", "POST"])
def mainRender():
    """
    [GET]
    return main.html

    [POST]
    request_type = application/json
    request_scheme = {
        'user_status': ['불안', '초조', '산만'],
        'user_goal': '집중력 향상'
    }
    response_type = application/json
    response_scheme = {
        'message': '적어도 3 문단 이상의 긴 문자열'
    }
    """
    if request.method == "GET":
        return render_template("main.html")
    # POST
    json = request.get_json()
    completion = chatbot.create_completion(json)

    return {"message": completion.choices[0].message.content}


@app.route('/regist' , methods=['POST'])
def login():
    return 'hello'

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)