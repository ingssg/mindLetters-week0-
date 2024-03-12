from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from db import articles_collection
import jwt
import os
import hashlib

# html 파일이 있는 folder path 정의
users_blueprint = Blueprint("users_blueprint", __name__, template_folder="../templates/users")


# 솔트 생성
def generate_salt():
    return os.urandom(16).hex()

# 비밀번호 암호화(솔팅, 스트레칭)
def hash_password(password, salt):
    hashed_password = password
    for _ in range(1000):
        hashed_password = hashlib.sha256((hashed_password + salt).encode()).hexdigest()
    return hashed_password

@users_blueprint.route("/signin")
def signin():
    return render_template('signin.html')


@users_blueprint.route("/signin", methods=["POST"])
def signin_user():
    # 로그인 기능 구현
    return


@users_blueprint.route("/signup")
def signup():
    return render_template('signup.html')


@users_blueprint.route("/signup", methods=["POST"])
def create_user():
    # 회원 가입 기능 구현
    isSignUp = False
    salt = generate_salt()
    user = {
        'id': request.form['id'],
        'hashed_password': hash_password(request.form['password'], salt),
        'nickname': request.form['nickname'],
    }
    # 회원 가입 로직
    # 빈 인풋 체크
    if not user['id'] or not request.form['password'] or not user['nickname']:
        return render_template('signup.html', error="모든 필드를 입력해주세요.")
    
    # 비밀번호 길이 확인
    if len(request.form['password']) < 8:
        return render_template('signup.html', error="비밀번호는 최소 8자 이상이어야 합니다.")
    
    isSignUp = True
    print(user)
    # DB에 유저 정보 추가
    # articles_collection.insert_one(user)
    
    return render_template('signin.html', isSignUp=isSignUp)
