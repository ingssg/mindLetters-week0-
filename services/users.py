from flask import Blueprint, render_template
from db import articles_collection

# html 파일이 있는 folder path 정의
users_blueprint = Blueprint("users_blueprint", __name__, template_folder="../templates/users")


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
    return
