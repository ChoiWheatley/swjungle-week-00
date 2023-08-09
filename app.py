from dataclasses import asdict
import inspect

from chatbot import ChatBot, create_question, get_ai_response
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash
from werkzeug.exceptions import Unauthorized, NotFound
from jinja2 import Environment, FileSystemLoader, Template
from pymongo import MongoClient
from decouple import config
from decouple import config

app = Flask(__name__)

# 시크릿키 설정
app.secret_key = config('APP_SECRET_KEY')

client = MongoClient('localhost', 27017)
# 시크릿키 설정
app.secret_key = config('APP_SECRET_KEY')

client = MongoClient('localhost', 27017)
db = client['WEEK00_TEAM7']
collection = db['users']
collection2 = db['chats']
collection3 = db['C']

@app.route('/')
def entrypoint():
    if 'username' in session:
        return f'''반갑습니다 {session["username"]}님!<br>
        <a href="/main/{session["username"]}">mainPage</a> 
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
    if userId_receive == "":
        flash("아이디를 입력해주세요.")
    if userPwd_receive == "":
        flash("비밀번호를 입력해주세요.")
        return render_template("login.html")
    
    user = db.users.find_one({'id':userId_receive}, {'pwd':userPwd_receive})
    if user is None:
        flash("존재하지 않는 유저입니다.")
        return render_template("login.html")
    session["username"] = userId_receive
    session.permanent = True
    return redirect(f'/main/{userId_receive}')

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
        if userId_receive == '' or userPwd_receive == '':
            db.users.insert_one()
        else:
            db.users.insert_one(user)
            flash("회원가입에 성공하였습니다!")
            return redirect('/login')
        print(user)
    else:
        return render_template("register.html")

@app.route('/main/<string:username>', methods=["GET", "POST"])
def mainRender(username):
    """
    ## GET
    return main.html

    ## POST

    새로운 채팅을 생성할 때 사용함.

    ### POST request type

    - user_status: ['불안', '초조', '산만'],
    - user_goal: '집중력 향상'
    - user_id: TODO - 현재는 username 이지만, 유니크한 user_id가 와야함.

    ### POST response type

    새로 생성된 채팅 객체(ChatBot)의 dict를 리턴함.
    """
    if username != session["username"]:
        raise Unauthorized("Username is different")

    if request.method == "GET":
        return render_template("main.html")
    # POST
    # 새로운 채팅 세션을 생성할 때 사용함
    body_dict = request.get_json()
    question = create_question(body_dict)
    ai_response = get_ai_response(question)

    body_dict["ai_response"] = ai_response
    body_dict["id"] = 1

    chatbot = ChatBot(**body_dict)

    db["chats"].insert_one(asdict(chatbot))

    return asdict(chatbot)


@app.route("/api/history/<string:username>", methods=["GET"])
def history(username):
    """유저의 히스토리 리스트를 쿼리할 때 사용함."""
    cursor = db["chats"].find({"user_id": username})
    if not cursor:
        raise NotFound("chat not found")
    return [
        {k: v for k, v in cur.items() if k in inspect.signature(ChatBot).parameters}
        for cur in cursor]


@app.route("/api/chat/<int:id>", methods=["GET", "POST"])
def chat(id):
    """
    chat regeneration에 사용될 함수

    ## POST request type:
    - user_status: ["불안", "초조", "산만"]
    - user_goal: "집중력 향상
    - _id: mongodb object id

    ## POST response type:
    수정된 `ChatBot` 객체가 반환됨.
    """
    cursor = db["chats"].find_one({"id", id})
    if not cursor:
        raise NotFound("Chat not found")
    if request.method == "GET":
        return cursor

    # POST

    question = create_question(cursor)
    ai_response = get_ai_response(question)

    chatbot = ChatBot(**cursor)
    chatbot.ai_messages.append(ai_response)
    db["chats"].replace_one({"id": chatbot.id}, asdict(chatbot))

    return asdict(chatbot)


if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)
