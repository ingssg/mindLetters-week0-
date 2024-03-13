from flask import Blueprint, render_template, request, jsonify
from db import articles_collection
from dto.article import ArticleDTO
from bson import ObjectId
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required

now = datetime.now()

# html 파일이 있는 folder path 정의
articles_blueprint = Blueprint("articles_blueprint", __name__, template_folder="../templates/articles")


@articles_blueprint.route("/")
@jwt_required()
def get_all_articles():
    userId = get_jwt_identity()['_id']

    topic_param = request.args.get("topic", default="all")
    page_param = request.args.get("page", default=1, type=int)

    filter = {
        "deleted_at": None,
    }

    if topic_param in ["good", "bad"]:
        filter["topic"] = topic_param

    page_size = 6
    skip = (page_param - 1) * page_size
    limit = page_size

    total = articles_collection.count_documents(filter)

    pipeline = [
        {
            "$match": filter
        }, {
            "$sort": {"_id": -1}
        }, {
            "$skip": skip
        }, {
            "$limit": limit
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "author",
                "foreignField": "_id",
                "as": "author"
            }
        }, {
            "$unwind": "$author"
        }, {
            "$project": {
                "topic": 1,
                "title": 1,
                "created_at": 1,
                "likes": 1,
                "comments": 1,
                "is_blind": 1,
                "author.nickname": 1,
                "author._id": 1,
            }
        }
    ]

    list_of_articles = list(articles_collection.aggregate(pipeline))

    # ObjectId 를 문자열로 변환
    for article in list_of_articles:
        article["_id"] = str(article["_id"])
        article["author"]["_id"] = str(article["author"]["_id"])

    articles_object = [ArticleDTO.from_dict(article_dict) for article_dict in list_of_articles]

    total_pages = (total // page_size) + (1 if total % page_size else 0)
    start_page = max(1, page_param - 5)
    end_page = min(total_pages, start_page + 9)

    return render_template('article_list.html', articles=articles_object, topic=topic_param,
                           pagination={"total": total, "page": page_param, "size": page_size,
                                       "start_page": start_page, "end_page": end_page}, userId=userId)


@articles_blueprint.route("/likes/<string:id>", methods=["POST"])
@jwt_required()
def like_article(id):
    userId = get_jwt_identity()['_id']

    filter = {'_id': ObjectId(id), 'deleted_at': None}

    articles_collection.update_one(filter, {'$addToSet': {'likes': userId}})

    return jsonify({'result': 'success'})


@articles_blueprint.route("/likes/<string:id>", methods=["DELETE"])
@jwt_required()
def dislike_article(id):
    userId = get_jwt_identity()['_id']

    filter = {'_id': ObjectId(id), 'deleted_at': None}

    articles_collection.update_one(filter, {'$pull': {'likes': userId}})
    return jsonify({'result': 'success'})


@articles_blueprint.route("/", methods=["POST"])
@jwt_required()
def create_article():
    # 게시물 생성 기능 구현
    userId = get_jwt_identity()['_id']

    article = {'topic': request.form['topic'], 'author': ObjectId(userId), 'title': request.form['title'],
               'body': request.form['body'],
               'is_blind': request.form['is_blind'] == "true", 'created_at': now.strftime('%Y-%m-%d %H:%M:%S'),
               'updated_at': None, 'deleted_at': None, 'comments': [], 'likes': []}

    articles_collection.insert_one(article)

    return jsonify({'result': 'success'})


@articles_blueprint.route("/<string:article_id>", methods=["DELETE"])
@jwt_required()
def remove_article(article_id):
    userId = get_jwt_identity()['_id']

    filter = {"deleted_at": None, "author": ObjectId(userId), '_id': ObjectId(article_id)}

    articles_collection.update_one(filter, {"$set": {"deleted_at": datetime.now()}})

    return jsonify({'result': 'success'})


@articles_blueprint.route("/<string:id>", methods=["PATCH"])
@jwt_required()
def update_article(id):
    # 게시물 수정 기능 구현
    article = {'topic': request.form['topic'], 'title': request.form['title'], 'body': request.form['body'],
               'is_blind': request.form['is_blind'] == "true", 'updated_at': now.strftime('%Y-%m-%d %H:%M:%S')}

    articles_collection.update_one({'_id': ObjectId(id)}, {"$set": article})
    return jsonify({'result': 'success'})


@articles_blueprint.route("/<string:id>")
@jwt_required()
def get_one_articles(id):
    userId = get_jwt_identity()['_id']

    pipeline = [
        {
            "$match": {
                "deleted_at": None,
                "_id": ObjectId(id)
            }
        }, {
            "$lookup": {
                "from": "users",
                "localField": "author",
                "foreignField": "_id",
                "as": "author"
            }
        }, {
            "$unwind": "$author"
        }, {
            "$project": {
                "topic": 1,
                "title": 1,
                "created_at": 1,
                "likes": 1,
                "comments": 1,
                "is_blind": 1,
                "body": 1,
                "author.nickname": 1,
                "author._id": 1,
            }
        }
    ]

    article = list(articles_collection.aggregate(pipeline))[0]

    return render_template('article_detail.html', article=article, userId=userId)


@articles_blueprint.route("/new")
@jwt_required()
def create_article_page():
    # 게시물 작성 페이지 구현
    userId = get_jwt_identity()['_id']
    return render_template('create_article.html', author=userId, type="create")


@articles_blueprint.route("/modify/<string:id>")
def modify_article_page(id):
    article = articles_collection.find_one({'_id': ObjectId(id)})

    return render_template('create_article.html', article=article, type="modify", id=id)
