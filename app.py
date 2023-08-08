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

@app.route('/register')
def registerRender():
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
    user_status = json.user_status
    user_goal = json.user_goal
    # TODO - connect to openai
    return {
        "message": f"test response that can be returned from openai. \
            user_status is \'{user_status}\' and user_goal is \'{user_goal}\'"
    }


@app.route('/login')
def login():
    return 

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)