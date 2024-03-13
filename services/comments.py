from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from db import comments_collection, articles_collection
from dto.comment import CommentDTO
from bson import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required

# html 파일이 있는 folder path 정의
comments_blueprint = Blueprint("comments_blueprint", __name__)


@comments_blueprint.route("/<string:article_id>")
@jwt_required()
def find_comments_by_article(article_id):
    pipeline = [
        {
            "$match": {
                "deleted_at": None,
                "article": ObjectId(article_id)
            }
        }, {
            "$sort": {"_id": -1}
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
                "body": 1,
                "is_blind": 1,
                "author.nickname": 1,
                "author._id": 1,
                "created_at": 1,

            }
        }
    ]

    list_of_comments = list(comments_collection.aggregate(pipeline))

    for comment in list_of_comments:
        print(comment)
        comment["_id"] = str(comment["_id"])
        comment["author"]["_id"] = str(comment["author"]['_id'])

    return jsonify({'result': 'success', 'comments': list_of_comments})


@comments_blueprint.route("/<string:article_id>", methods=["POST"])
@jwt_required()
def create_comment(article_id):
    userId = get_jwt_identity()['_id']
    comment = request.get_json()

    comment["created_at"] = datetime.now()
    comment["author"] = ObjectId(userId)
    comment["article"] = ObjectId(article_id)

    result = comments_collection.insert_one(comment)

    # article 의 comments 배열에 comment ObjectId 추가
    articles_collection.update_one({'_id': comment["article"]},
                                   {'$addToSet': {'comments': result.inserted_id}})
    return jsonify({'result': 'success'})


@comments_blueprint.route("/<string:id>", methods=["PATCH"])
@jwt_required()
def update_comment(id):
    userId = get_jwt_identity()['_id']

    data = request.get_json()
    comment = CommentDTO.from_dict(data)

    comment.updated_at = datetime.now()

    filter = {'_id': ObjectId(id), 'author': ObjectId(userId)}

    comments_collection.update_one(filter, {"$set": comment})


@comments_blueprint.route("/<string:article_id>/<string:comment_id>", methods=["DELETE"])
@jwt_required()
def remove_comment(article_id, comment_id):
    print("-------------", article_id, comment_id)
    userId = get_jwt_identity()['_id']

    filter = {'deleted_at': None, '_id': ObjectId(comment_id), 'author': ObjectId(userId)}

    update_result = comments_collection.update_one(filter, {"$set": {"deleted_at": datetime.now()}})

    if update_result.modified_count:
        # article 의 comments 배열에서 comment ObjectId 삭제
        articles_collection.update_one({'_id': ObjectId(article_id)}, {'$pull': {'comments': ObjectId(comment_id)}})

    return jsonify({'result': 'success'})
