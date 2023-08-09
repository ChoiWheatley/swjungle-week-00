from dataclasses import asdict
import inspect

from bson import ObjectId

from chatbot import ChatBot, create_question, get_ai_response
from flask import Flask, render_template, request, redirect, session, flash
from datetime import timedelta
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import Unauthorized, NotFound
from jinja2 import Environment, FileSystemLoader, Template
from pymongo import MongoClient
from decouple import config

app = Flask(__name__)

# 시크릿키 설정
app.secret_key = config('APP_SECRET_KEY')

client = MongoClient('localhost', 27017)
db = client['WEEK00_TEAM7']
collection = db['users']
collection2 = db['chats']
collection3 = db['C']

@app.route('/')
def entrypoint():
    if '_id' in session:
        return f'''반갑습니다 {session["username"]}님!<br>
        <a href="/main/{session["_id"]}">mainPage</a> 
        <a href="/logout">Logout</a>'''
    else:
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    # POST
    userId_receive = request.form.get('username')
    userPwd_receive = request.form.get('password')
    if userId_receive == "" or userPwd_receive == "":
        flash("빈칸을 모두 입력해주세요!")
        return render_template("login.html")
    
    user = db.users.find_one({'id':userId_receive}, {'pwd':userPwd_receive})
    if user is None:
        flash("존재하지 않는 유저입니다.")
        return render_template("login.html")
    session["username"] = userId_receive
    session['_id'] = str(user['_id'])
    print(session['_id'])
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)
    return redirect(f'/main/{session["_id"]}')

@app.route('/logout', methods=['GET'])
def logout():
    session.pop("username")
    return redirect('/login')

@app.route('/register', methods=["GET", "POST"])
def registerRender():
    if request.method == "POST":
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method="pbkdf2:sha256",
            salt_length=8
        )
        userId_receive = request.form.get('username')
        userPwd_receive = hash_and_salted_password
        
        user = {
            'id': userId_receive,
            'pwd': userPwd_receive
        }
        if userId_receive == '' or request.form.get('password') == '':
            flash("빈칸을 모두 입력해주세요!")
            return render_template("register.html")
        if db.users.find_one({'id':userId_receive}) is not None:
            flash("다른 분이 사용 중인 아이디입니다. 다시 입력해주세요.")
            return render_template("register.html")
        else:
            db.users.insert_one(user)
            flash("회원가입에 성공하였습니다!")
            return redirect('/login')
    else:
        return render_template("register.html")

@app.route('/main/<string:_id>', methods=["GET", "POST"])
def mainRender(_id):
    """
    ## GET
    return main.html

    ## POST

    새로운 채팅을 생성할 때 사용함.

    ### POST request type

    - user_status: ['불안', '초조', '산만'],
    - user_goal: '집중력 향상'

    ### POST response type

    새로 생성된 채팅 객체(ChatBot)의 dict를 리턴함.
    """
    if _id != session["_id"]:
        raise Unauthorized("user id is different")

    if request.method == "GET":
        return render_template("main.html")
    # POST
    # 새로운 채팅 세션을 생성할 때 사용함
    body_dict = request.get_json()
    question = create_question(body_dict)
    ai_response = get_ai_response(question)

    body_dict["ai_response"] = [ai_response]
    body_dict["user_id"] = _id

    result = db["chats"].insert_one(body_dict)
    cursor = db["chats"].find_one(result.inserted_id)

    if cursor:
        return asdict(ChatBot(**cursor))
    raise NotFound("chat not found")


@app.route("/api/history/<string:user_id>", methods=["GET"])
def history(user_id):
    """
    유저의 히스토리 리스트를 쿼리할 때 사용함.

    ### GET response type

    - List[dict(ChatBot)]
    """
    cursor = db["chats"].find({"user_id": user_id})
    if not cursor:
        raise NotFound("chat not found")
    return [asdict(ChatBot(**cur)) for cur in cursor]


@app.route("/api/chat/<string:_id>", methods=["GET", "POST"])
def chat(_id: str):
    """
    chat regeneration에 사용될 함수

    ### POST request type:

    - None

    ### POST response type:

    - 수정된 dict(ChatBot)
    """
    cursor = db["chats"].find_one(ObjectId(_id))
    if not cursor:
        raise NotFound("Chat not found")
    if request.method == "GET":
        return asdict(ChatBot(**cursor))

    # POST

    question = create_question(cursor)
    ai_response = get_ai_response(question)

    db["chats"].update_one({"_id": ObjectId(_id)}, {"$push": {"ai_response": ai_response}})
    cursor = db["chats"].find_one(ObjectId(_id))

    if not cursor:
        raise NotFound("Chat not found")
    return asdict(ChatBot(**cursor))


if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)