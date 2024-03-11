# https://www.geeksforgeeks.org/templating-with-jinja2-in-flask/

from flask import Flask
from services.users import users_blueprint
from services.articles import articles_blueprint

app = Flask(__name__)

# 사용자 관련 블루프린트 등록
app.register_blueprint(users_blueprint, url_prefix='/users')

# 게시물 관련 블루프린트 등록
app.register_blueprint(articles_blueprint, url_prefix='/articles')


@app.route("/")
def home():
    return "Hello, World!"


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
