from datetime import datetime
from flask import Blueprint, render_template, request
from db import comments_collection, articles_collection
from dto.comment import CommentDTO
from bson import ObjectId
from flask_jwt_extended import get_jwt_identity, jwt_required

# html 파일이 있는 folder path 정의
comments_blueprint = Blueprint("comments_blueprint", __name__)


@comments_blueprint.route("/")
def create_comment():
    data = request.get_json()
    comment = CommentDTO.from_dict(data)

    comment.created_at = datetime.now()
    # client 에서 작성자 ObjectID author 에 추가하여 보냄

    result = comments_collection.insert_one(comment)

    # article 의 comments 배열에 comment ObjectId 추가
    articles_collection.update_one({'_id': ObjectId(comment.article)}, {'$addToSet': {'comments': result.inserted_id}})


@comments_blueprint.route("/<string:id>", methods=["PATCH"])
@jwt_required()
def update_comment(id):
    userId = get_jwt_identity()['_id']

    data = request.get_json
    comment = CommentDTO.from_dict(data)

    comment.updated_at = datetime.now()

    filter = {'_id': ObjectId(id), 'author': ObjectId(userId)}

    comments_collection.update_one(filter, {"$set": comment})


@comments_blueprint.route("/<string:article_id>/<string:comment_id>", methods=["DELETE"])
@jwt_required()
def remove_comment(article_id, comment_id):
    userId = get_jwt_identity()['_id']

    filter = {'_id': ObjectId(comment_id), 'author': ObjectId(userId)}

    update_result = comments_collection.update_one(filter, {"$set": {"deleted_at": datetime.now()}})

    if update_result.modified_count:
        # article 의 comments 배열에서 comment ObjectId 삭제
        comments_collection.update_one({'_id': ObjectId(article_id)}, {'$pull': {'comments': article_id}})
