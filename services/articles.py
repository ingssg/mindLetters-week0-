from flask import Blueprint, render_template
from db import articles_collection
from dto.article import ArticleDTO

# html 파일이 있는 folder path 정의
articles_blueprint = Blueprint("articles_blueprint", __name__, template_folder="../templates/articles")


@articles_blueprint.route("/")
def get_all_articles():
    # list_of_articles = [
    #     {"topic": "good", "author": "홍길동", "title": "칭찬합니다.", "date": "2024-03-11", "is_blind": False},
    #     {"topic": "bad", "author": "양장피", "title": "싫습니다.", "date": "2024-03-11", "is_blind": True},
    #     {"topic": "bad", "author": "김꺽정", "title": "싫습니다.", "date": "2024-03-10", "is_blind": True},
    #     {"topic": "good", "author": "임꺽정", "title": "칭찬합니다.", "date": "2024-03-09", "is_blind": False}
    # ]

    list_of_articles = list(articles_collection.find())

    # ObjectId 를 문자열로 변환
    for article in list_of_articles:
        article["_id"] = str(article["_id"])

    articles_object = [ArticleDTO.from_dict(article_dict) for article_dict in list_of_articles]

    return render_template('article_list.html', articles=articles_object)


@articles_blueprint.route("/", methods=["POST"])
def create_article():
    # 게시물 생성 기능 구현
    return


@articles_blueprint.route("/", methods=["DELETE"])
def remove_article():
    # 게시물 삭제 기능 구현
    return


@articles_blueprint.route("/<string:id>")
def get_one_articles(id):
    return render_template('article_detail.html', id=id)
