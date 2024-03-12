from flask import Blueprint, render_template, request, jsonify
from db import articles_collection
from dto.article import ArticleDTO
from bson import ObjectId
from datetime import datetime

now = datetime.now()

# html 파일이 있는 folder path 정의
articles_blueprint = Blueprint("articles_blueprint", __name__, template_folder="../templates/articles")


@articles_blueprint.route("/")
def get_all_articles():
    topic_param = request.args.get("topic", default="all")
    page_param = request.args.get("page", default=1, type=int)

    filter = {"deleted_at": None}

    if topic_param in ["good", "bad"]:
        filter["topic"] = topic_param

    page_size = 6
    skip = (page_param - 1) * page_size
    limit = page_size

    total = articles_collection.count_documents(filter)

    # todo author 를 작성자의 ObjectId 로 설정 후, GET 요청시 lookup 해 오도록 변경
    list_of_articles = list(articles_collection.find(filter).skip(skip).limit(limit))

    # ObjectId 를 문자열로 변환
    for article in list_of_articles:
        article["_id"] = str(article["_id"])

    articles_object = [ArticleDTO.from_dict(article_dict) for article_dict in list_of_articles]

    total_pages = (total // page_size) + (1 if total % page_size else 0)
    start_page = max(1, page_param - 5)
    end_page = min(total_pages, start_page + 9)

    return render_template('article_list.html', articles=articles_object, topic=topic_param,
                           pagination={"total": total, "page": page_param, "size": page_size,
                                       "start_page": start_page, "end_page": end_page})


@articles_blueprint.route("/likes/<string:id>", methods=["POST"])
def like_article(id):
    userId = "abc"  # get author id

    filter = {'_id': ObjectId(id), 'deleted_at': None}

    articles_collection.update_one(filter, {'$addToSet': {'likes': userId}})


@articles_blueprint.route("/likes/<string:id>", methods=["DELETE"])
def dislike_article(id):
    userId = "abc"  # get author id

    filter = {'_id': ObjectId(id), 'deleted_at': None}

    articles_collection.update_one(filter, {'$pull': {'likes': userId}})


@articles_blueprint.route("/", methods=["POST"])
def create_article():
    # 게시물 생성 기능 구현
    article = {'topic': request.form['topic'], 'author': request.form['author'], 'title': request.form['title'],
               'body': request.form['body'],
               'is_blind': request.form['is_blind'], 'created_at': now.strftime('%Y-%m-%d %H:%M:%S'),
               'updated_at': None, 'deleted_at': None, 'comments': [], 'likes': []}

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

    articles_collection.update_one({'_id': ObjectId(id)}, {"$set": article})
    return jsonify({'result': 'success'})


@articles_blueprint.route("/<string:id>")
def get_one_articles(id):
    article = articles_collection.find_one({'_id': ObjectId(id)})
    return render_template('article_detail.html', article=article)


# 65ef8d9cf8506452fbb03c86
# 65f00a141320c7693dbdaf7a
@articles_blueprint.route("/new")
def create_article_page():
    # 게시물 작성 페이지 구현
    # author = request.form['author']
    author = "김철수"
    return render_template('create_article.html', author=author, type="create")


@articles_blueprint.route("/modify/<string:id>")
def modify_article_page(id):
    article = articles_collection.find_one({'_id': ObjectId(id)})

    return render_template('create_article.html', article=article, type="modify", id=id)
