import chatbot
from flask import Flask, render_template, request, redirect, session, flash
from werkzeug.security import generate_password_hash
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
collection2 = db['B']
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


@app.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    # POST
    # TODO - Do some authentication
    return redirect("/main")

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)