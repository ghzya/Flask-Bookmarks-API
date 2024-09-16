from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.constants.http_status_code import *
from src.database import db, Bookmark

import validators
from flasgger import swag_from

bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")


# @bookmarks.get("/")
# def get_all():
#     return {"bookmarks": []}


# get bookmarks or post a bookmark
@bookmarks.route("/", methods=['POST', 'GET'])
# @jwt_required()
def handle_bookmarks():
    # current_user = get_jwt_identity()
    current_user = 1 # debug in browser, no authorization

    if request.method == 'POST':
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')

        if not validators.url(url):
            # return jsonify({"error": "Enter valid url"})
            return jsonify({
                "error": "URL not valid"
            }), HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                "error": "URL already exists"
            }), HTTP_409_CONFLICT
        
        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            "id": bookmark.id,
            "url": bookmark.url,
            "short_url": bookmark.short_url,
            "visits": bookmark.visits,
            "body": bookmark.body,
            "created_at": bookmark.created_at,
            "updated_at": bookmark.updated_at
        }), HTTP_201_CREATED

    else:
        # pagination
        page = request.args.get("page", default=1, type=int)
        per_page = request.args.get("per_page", default=5, type=int)

        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)

        data = []

        for bookmark in bookmarks.items:
            data.append({
                "id": bookmark.id,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visits": bookmark.visits,
                "body": bookmark.body,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at
            })

        meta = {
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            "total_count": bookmarks.total,
            "prev_page": bookmarks.prev_num,
            "next_page": bookmarks.next_num,
            "has_prev": bookmarks.has_prev,
            "has_next": bookmarks.has_next
        }

        return jsonify({
            "data": data,
            "meta": meta
        }), HTTP_200_OK


# get one bookmark
@bookmarks.get("/<int:id>")
# @jwt_required()
def get_bookmark(id):
    # current_user = get_jwt_identity()
    current_user = 1 # debug in browser, no authorization

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "message": "Item not found" 
        }), HTTP_404_NOT_FOUND
    
    return jsonify({
        "id": bookmark.id,
        "url": bookmark.url,
        "short_url": bookmark.short_url,
        "visits": bookmark.visits,
        "body": bookmark.body,
        "created_at": bookmark.created_at,
        "updated_at": bookmark.updated_at
    }), HTTP_200_OK


# Edit bookmark
@bookmarks.put("/<int:id>")
@bookmarks.patch("/<int:id>")
# @jwt_required()
def edit_bookmark(id):
    # current_user = get_jwt_identity()
    current_user = 1 # debug in browser, no authorization

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "message": "Item not found"
        }), HTTP_404_NOT_FOUND
    
    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')

    if not validators.url(url):
        # return jsonify({"error": "Enter valid url"})
        return jsonify({
            "error": "URL not valid"
        }), HTTP_400_BAD_REQUEST
    
    bookmark.url = url
    bookmark.body = body

    db.session.commit()

    return jsonify({
        "id": bookmark.id,
        "url": bookmark.url,
        "short_url": bookmark.short_url,
        "visits": bookmark.visits,
        "body": bookmark.body,
        "created_at": bookmark.created_at,
        "updated_at": bookmark.updated_at
    }), HTTP_200_OK


# Edit bookmark
@bookmarks.delete("/<int:id>")
# @jwt_required()
def delete_bookmark(id):
    # current_user = get_jwt_identity()
    current_user = 1 # debug in browser, no authorization

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({
            "message": "Item not found"
        }), HTTP_404_NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT

@bookmarks.get("/stats")
@swag_from("./docs/bookmarks/stats.yaml")
# @jwt_required()
def get_stats():
    # current_user = get_jwt_identity()
    current_user = 1

    data = []

    items = Bookmark.query.filter_by(user_id=current_user).all()

    for item in items:
        new_link = {
            "id": item.id,
            "url": item.url,
            "short_url": item.short_url,
            "visits": item.visits,
        }

        data.append(new_link)

    return jsonify({
        "data": data
    }), HTTP_200_OK