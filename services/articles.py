from flask import Blueprint, render_template, request, jsonify
from db import articles_collection
from bson.objectid import ObjectId
from dto.article import ArticleDTO
from datetime import datetime

now = datetime.now()

# html 파일이 있는 folder path 정의
articles_blueprint = Blueprint("articles_blueprint", __name__, template_folder="../templates/articles")


@articles_blueprint.route("/")
def get_all_articles():
    topic_param = request.args.get("topic")

    filter = {}

    if topic_param in ["good", "bad"]:
        filter["topic"] = topic_param
    else:
        topic_param = "all"

    list_of_articles = list(articles_collection.find(filter))

    # ObjectId 를 문자열로 변환
    for article in list_of_articles:
        article["_id"] = str(article["_id"])

    articles_object = [ArticleDTO.from_dict(article_dict) for article_dict in list_of_articles]

    return render_template('article_list.html', articles=articles_object, topic=topic_param)


@articles_blueprint.route("/", methods=["POST"])
def create_article():
    # 게시물 생성 기능 구현
    article = {'topic': request.form['topic'], 'author': request.form['author'], 'title': request.form['title'], 'body': request.form['body'], 
               'is_blind': request.form['is_blind'], 'created_at': now.strftime('%Y-%m-%d %H:%M:%S'),'updated_at':None, 'deleted_at':None}

    articles_collection.insert_one(article)
    return jsonify({'result': 'success'})    


@articles_blueprint.route("/<string:id>", methods=["DELETE"])
def remove_article():
    # 게시물 삭제 기능 구현
    return


@articles_blueprint.route("/<string:id>", methods=["PATCH"])
def update_article(id):
    # 게시물 수정 기능 구현
    article = {'topic': request.form['topic'], 'title': request.form['title'], 'body': request.form['body'], 
               'is_blind': request.form['is_blind'], 'updated_at': now.strftime('%Y-%m-%d %H:%M:%S')}

    articles_collection.update_one({'_id':ObjectId(id)}, {"$set": article})
    return jsonify({'result': 'success'}) 


@articles_blueprint.route("/<string:id>")
def get_one_articles(id):
    article = articles_collection.find_one({'_id':ObjectId(id)})
    return render_template('article_detail.html', article=article)

#65ef8d9cf8506452fbb03c86
#65f00a141320c7693dbdaf7a
@articles_blueprint.route("/new")
def create_article_page():
    # 게시물 작성 페이지 구현
    # author = request.form['author']
    author = "김철수"
    return render_template('create_article.html', author=author, type="create")

@articles_blueprint.route("/modify/<string:id>")
def modify_article_page(id):
    article = articles_collection.find_one({'_id':ObjectId(id)})

    return render_template('create_article.html', article=article, type="modify", id=id)
