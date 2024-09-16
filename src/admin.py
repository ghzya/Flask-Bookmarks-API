from flask import Blueprint, request, jsonify
from src.constants.http_status_code import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database import db, User


admin = Blueprint("admin", __name__, url_prefix="/api/v1/admin")

@admin.get("/")
@jwt_required()
def index():
    user_id = get_jwt_identity()
    
    if user_id == User.query.filter_by(username="EvilCrow").first().id:
        return {"msg": "This is admin page"}, HTTP_200_OK
    
    return jsonify({"msg": "You are unauthorized"}), HTTP_401_UNAUTHORIZED

@admin.get("/users")
@jwt_required()
def users():
    user_id = get_jwt_identity()

    if user_id == User.query.filter_by(username="EvilCrow").first().id:
        registered_user = User.get_all()
        return jsonify(registered_user), HTTP_200_OK
    return jsonify({"msg": "You are unauthorized"}), HTTP_401_UNAUTHORIZED





