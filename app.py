# https://www.geeksforgeeks.org/templating-with-jinja2-in-flask/
import os

from flask import Flask, redirect, url_for
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
    return redirect(url_for('users_blueprint.signin'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
