# https://www.geeksforgeeks.org/templating-with-jinja2-in-flask/
import os

from flask import Flask, redirect, url_for, render_template
from services.users import users_blueprint
from services.articles import articles_blueprint
from services.comments import comments_blueprint
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

# 사용자 관련 블루프린트 등록
app.register_blueprint(users_blueprint, url_prefix='/users')

# 게시물 관련 블루프린트 등록
app.register_blueprint(articles_blueprint, url_prefix='/articles')

# 댓글 관련 블루프린트 등록
app.register_blueprint(comments_blueprint, url_prefix='/comments')


@app.route("/")
def home():
    return "Hello, World!"


# 토큰이 만료된 경우
@jwt.expired_token_loader
def handleWithExpiredToken(jwt_header, jwt_payload):
    return render_template('signin.html', isExpired=True)

# 토큰이 없던 경우
@jwt.unauthorized_loader
def handleWithNoToken(reason):
    return render_template('signin.html', hasNoToken=True)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
