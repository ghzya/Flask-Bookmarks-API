from flask import Blueprint, request, jsonify, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity

from src.constants.http_status_code import *
from src.database import db, User

import validators
from flasgger import swag_from


auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/register")
@swag_from("./docs/auth/register.yaml")
def register():
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    # Validate user input
    if len(password) < 6:
        return jsonify({
            "error": "Password is too short"
        }), HTTP_400_BAD_REQUEST
    
    if len(username) < 6:
        return jsonify({
            "error": "Username is too short"
        }), HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or ' ' in username:
        return jsonify({
            "error": "Username should be alphanumeric, also no spaces"
        }), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({
            "error": "Email is not valid"
        }), HTTP_400_BAD_REQUEST
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({
            "error": "Email is taken"
        }), HTTP_409_CONFLICT

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({
            "error": "Username is taken"
        }), HTTP_409_CONFLICT

    # Hash user's password
    pwd_hash = generate_password_hash(password)
    
    # Add user into db
    user = User(username = username, password = pwd_hash, email = email)
    db.session.add(user)
    db.session.commit()

    # how to query
    # db.Query().filter_by(id=1)
    # db.get_or_404(User, id)
    # User.query.filter_by(id=1)

    return jsonify({
        "message": "User created",
        "user": {
            "username": username,
            "email": email
        }
    }), HTTP_201_CREATED


@auth.post("/login")
@swag_from("./docs/auth/login.yaml")
def login():
    email = request.json.get("email", '') 
    password = request.json.get("password", '') 

    # email = request.get_json()["email"]
    # password = request.get_json()["password"]

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                "user": {
                    "refresh": refresh,
                    "access": access,
                    "username": user.username,
                    "email": user.email
                }
            }), HTTP_200_OK

    return jsonify({"error": "wrong credentials"}), HTTP_401_UNAUTHORIZED

@auth.get("/me")
@jwt_required()
def me():
    ## debug to check the user id from jwt access token
    # import pdb
    # pdb.set_trace()

    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return jsonify({
        "username": user.username,
        "email": user.email
    }), HTTP_200_OK

@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_users_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        "access": access
    }), HTTP_200_OK

@auth.get("/<int:id>/delete")
@jwt_required()
def delete(id):
    user_id = get_jwt_identity()
    if user_id == User.query.filter_by(username="EvilCrow").first().id:

        deleted_user = User.query.filter_by(id=id).first()
        if deleted_user:
            db.session.delete(deleted_user)
            db.session.commit()
            return redirect("http://127.0.0.1:5000/api/v1/admin/users", HTTP_302_FOUND)
    
        return jsonify({"msg": "User not found"})
    
    return jsonify({"msg": "You are unauthorized"}), HTTP_401_UNAUTHORIZED
