from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from jinja2 import Environment, FileSystemLoader, Template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['WEEK00_TEAM7']
collection = db['A']
collection2 = db['B']
collection3 = db['C']

SECRET_KEY = 'SWJUNGLE'

import jwt
import datetime
import hashlib

@app.route('/')
def loginRender():
    # 현재 이용자의 컴퓨터에 저장된 cookie에서 mytok en을 가져온다.
    token_receive = request.cookies.get('mytoken')
    print(token_receive)
    try:
        # 암호화 되어있는 token의 값을 우리가 사용할 수 있도록 디코딩 (암호화 풀기)
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', id=user_info["id"])
    # 만약 해당 token의 로그인 시간이 만료되었다면, 아래와 같은 코드 실행
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    # 만약 해당 token이 올바르게 디코딩되지 않는다면, 아래와 같은 코드 실행
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))
    
@app.route('/login')
def login():
    msg = request.args.get("msg")
    return render_template('login.html', msg=msg)

@app.route('/register')
def registerRender():
    return render_template('register.html')

# 회원가입 API
# id, pwd, pwd2 받아서, mongoDB에 저장합니다.
# 저장하기 전에, pw를 sha256 방법(=단방향 암호화. 풀어볼 수 없음)으로 암호화해서 저장합니다.
@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pwd_receive = request.form['pwd_give']
    pwd2_receive = request.form['pwd2_give']

    pwd_hash = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    db.user.insert_one({'id': id_receive, 'pwd':pwd_hash, 'pwd2':pwd2_receive})

    return jsonify({'result':'success'})

# 로그인 API
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급합니다.
@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pwd_receive = request.form['pwd_give']
    pwd2_receive = request.form['pwd2_give']

    # 회원가입 때와 같은 방법으로 pwd 암호화
    pwd_hash = hashlib.sha256(pwd_receive.encode('utf-8')).hexdigest()

    # id, 암호화된 pwd를 가지고 해당 유저를 찾음
    result = db.user.find_one({'id': id_receive, 'pwd':pwd_hash})

    # 찾으면 jwt 토큰을 만들어 발급
    # jwt 토큰에는 payload와 시크릿키가 필요하다.
    # 시크릿키가 있어야 토큰을 디코딩해서 payload 값을 볼 수 있음
    # 아래에선 id 와 exp를 담았습니다. 즉, jwt 토큰을 풀면 유저id 값을 알 수 있음
    # exp에는 만료시간을 넣어줌, 만료시간이 지나면 시크릿키로 토큰을 풀 때 만료되었다고 에러가 난다.
    if result is not None:
        payload = {
            'id' : id_receive,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        # token을 준다
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg':'아이디/비밀번호가 일치하지 않습니다.'})

# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API입니다.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
# (그렇지 않으면 남의 장바구니라든가, 정보를 누구나 볼 수 있겠죠?)
@app.route('/api/id', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    # try / catch 문?
    # try 아래를 실행했다가, 에러가 있으면 except 구분으로 가란 얘기입니다.

    try:
        # token을 시크릿키로 디코딩합니다.
        # 보실 수 있도록 payload를 print 해두었습니다. 우리가 로그인 시 넣은 그 payload와 같은 것이 나옵니다.
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        # payload 안에 id가 들어있습니다. 이 id로 유저정보를 찾습니다.
        # 여기에선 그 예로 닉네임을 보내주겠습니다.
        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'id': userinfo['id']})
    except jwt.ExpiredSignatureError:
        # 위를 실행했는데 만료시간이 지났으면 에러가 납니다.
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)