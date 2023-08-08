from flask import Flask, render_template, request, redirect, session, url_for, flash
from jinja2 import Environment, FileSystemLoader, Template
from pymongo import MongoClient

app = Flask(__name__)

# 시크릿키 설정
app.secret_key = 'f289040f70d7274ed6bf86d3906b17ebee34e83d7053126d0029f447d82f2165'

ID = "hello"
PW = "world"

client = MongoClient('mongodb://localhost:27017/')
db = client['WEEK00_TEAM7']
collection = db['A']
collection2 = db['B']
collection3 = db['C']

@app.route('/')
def loginRender():
    if 'userID' in session:
        return render_template("login.html", userid=session.get("userID"), login=True)
    else:
        return render_template("login.html", login=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global ID,PW
    _id_ = request.args.get("loginId")
    _pwd_ = request.args.get("loginPwd")

    if ID == _id_ and PW == _pwd_:
        session["userID"] = _id_
        return redirect(url_for('loginRender'))
    else:
        return redirect(url_for('loginRender'))

@app.route('/logout', methods=['GET'])
def logout():
    session.pop("userID")
    return redirect(url_for('loginRender'))

@app.route('/register')
def registerRender():
    return render_template("register.html")

@app.route('/main')
def mainRender():
    return render_template("main.html")

if __name__ == '__main__':
    app.run('0.0.0.0', port=4000, debug=True)