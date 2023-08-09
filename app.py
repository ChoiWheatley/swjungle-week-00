import chatbot
from flask import Flask, render_template, request, redirect, session, flash
from datetime import timedelta
from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from decouple import config

app = Flask(__name__)

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
    print(request.headers["content-Type"])
    json = request.get_json()
    completion = chatbot.create_completion(json)
    return {"message": completion.choices[0].message.content}

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)