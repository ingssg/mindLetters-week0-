from datetime import datetime
from flask import Blueprint, render_template, request, jsonify
from db import comments_collection, articles_collection
from dto.comment import CommentDTO
from bson import ObjectId

# html 파일이 있는 folder path 정의
comments_blueprint = Blueprint("comments_blueprint", __name__)


@comments_blueprint.route("/", methods=["POST"])
def create_comment():
    
    comment = request.get_json()

    comment["created_at"] = datetime.now()
    # client 에서 작성자 ObjectID author 에 추가하여 보냄

    result = comments_collection.insert_one(comment)

    # article 의 comments 배열에 comment ObjectId 추가
    articles_collection.update_one({'_id': ObjectId(comment["article"])}, {'$addToSet': {'comments': result.inserted_id}})
    return jsonify({'result': 'success'})


@comments_blueprint.route("/<string:id>", methods=["PATCH"])
def update_comment(id):
    userId = "abc"  # get author id

    data = request.get_json()
    comment = CommentDTO.from_dict(data)

    comment.updated_at = datetime.now()

    filter = {'_id': ObjectId(id), 'author': ObjectId(userId)}

    comments_collection.update_one(filter, {"$set": comment})


@comments_blueprint.route("/<string:article_id>/<string:comment_id>", methods=["DELETE"])
def remove_comment(article_id, comment_id):
    userId = "abc"  # get author id

    filter = {'_id': ObjectId(comment_id), 'author': ObjectId(userId)}

    update_result = comments_collection.update_one(filter, {"$set": {"deleted_at": datetime.now()}})

    if update_result.modified_count:
        # article 의 comments 배열에서 comment ObjectId 삭제
        comments_collection.update_one({'_id': article_id}, {'$pull': {'comments': article_id}})
