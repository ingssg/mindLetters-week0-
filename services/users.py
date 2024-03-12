from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from db import articles_collection, users_collection
from datetime import datetime
import jwt
import os
import hashlib

# html 파일이 있는 folder path 정의
users_blueprint = Blueprint("users_blueprint", __name__, template_folder="../templates/users")


# 솔트 생성
def generate_salt():
    return os.urandom(16).hex()

# 비밀번호 솔팅, 키 스트레칭
def hash_password(password, salt):
    hashed_password = password
    for _ in range(1328): # 반복 횟수 1000~10000 사이 값 (서버 과부하 방지 및 보안 고려)
        hashed_password = hashlib.sha256((hashed_password + salt).encode()).hexdigest()
    return hashed_password

@users_blueprint.route("/signin")
def signin():
    return render_template('signin.html')


@users_blueprint.route("/signin", methods=["POST"])
def signin_user():
    # 로그인 기능 구현
    user = {
    'id': request.form.get('id', ''),
    'password': request.form.get('password', ''),
    }

    print(user['id'] + '====' + user['password'])

    # 빈 인풋 체크
    if not user['id'] or not user['password']:
        return render_template('signin.html', error="모든 필드를 입력해주세요.")

    user_info = users_collection.find_one({"id": user['id']})
    salt = user_info['salt']

    print(user['password'] + '====' + user_info['hashed_password'])
    if(hash_password(user['password'], salt) != user_info['hashed_password']):
        return render_template('signin.html', error="로그인 정보가 올바르지 않습니다.")

    return render_template('articles/article_list.html')

@users_blueprint.route("/signup")
def signup():
    return render_template('signup.html')


@users_blueprint.route("/signup", methods=["POST"])
def create_user():
    # 회원 가입 기능 구현
    isSignUp = False
    salt = generate_salt()

    user = {
    'id': request.form.get('id', ''),
    'hashed_password': '',
    'nickname': request.form.get('nickname', ''),
    'salt': salt,
    'createdAt': datetime.now(),
    }

    # 회원 가입 로직
    # 빈 인풋 체크
    if not user['id'] or not request.form.get('password', '') or not request.form.get('password-confirm', '') or not user['nickname']:
        return render_template('signup.html', error="모든 필드를 입력해주세요.")
    
    # 비밀번호 길이 확인
    if len(user['password']) < 8:
        return render_template('signup.html', error="비밀번호는 최소 8자 이상이어야 합니다.")
    
    # 비밀번호 & 비밀번호 확인 일치 여부 확인
    if request.form['password'] != request.form['password-confirm']:
        return render_template('signup.html', error="비밀번호와 비밀번호 확인이 일치하지 않습니다.")

    user['hashed_password'] = hash_password(request.form['password'], salt)


    isSignUp = True
    print(user)
    # DB에 유저 정보 추가
    users_collection.insert_one(user)
    
    return render_template('signin.html', isSignUp=isSignUp)
