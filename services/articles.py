from flask import Blueprint, render_template

# html 파일이 있는 folder path 정의
articles_blueprint = Blueprint("articles_blueprint", __name__, template_folder="../templates/articles")


@articles_blueprint.route("/")
def get_all_articles():
    return render_template('article_list.html')


@articles_blueprint.route("/<string:id>")
def get_one_articles(id):
    return render_template('article_detail.html', id=id)
