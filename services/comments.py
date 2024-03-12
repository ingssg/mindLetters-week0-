from datetime import datetime
from flask import Blueprint, render_template, request
from db import comments_collection
from dto.comment import CommentDTO
from bson import ObjectId

# html 파일이 있는 folder path 정의
comments_blueprint = Blueprint("comments_blueprint", __name__)


@comments_blueprint.route("/")
def create_comment():
    data = request.get_json()
    comment = CommentDTO.from_dict(data)

    comment.created_at = datetime.now
    # 작성자 ObjectID author 에 추가
    # article 의 comments 배열에 comment ObjectId 추가

    comments_collection.insert_one(comment)


@comments_blueprint.route("/<string:id>", method=["PATCH"])
def update_comment(id):
    data = request.get_json
    comment = CommentDTO.from_dict(data)

    comment.updated_at = datetime.now()

    # filter 에 작성자가 현재 로그인한 사람인지도 추가해야 함
    filter = {'_id': ObjectId(id)}

    comments_collection.update_one(filter, {"$set": comment})


@comments_blueprint.route("/<string:id>", method=["DELETE"])
def remove_comment(id):
    # filter 에 작성자가 현재 로그인한 사람인지도 추가해야 함
    filter = {'_id': ObjectId(id)}

    comments_collection.update_one(filter, {"$set": {"deleted_at": datetime.now()}})
