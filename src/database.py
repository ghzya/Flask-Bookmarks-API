# from enum import unique
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import backref
from datetime import datetime
import string
import random
import json


db = SQLAlchemy()


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(8), unique=True, nullable=False)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.Text(), nullable=False)
    created_at=db.Column(db.DateTime(), default=datetime.now())
    updated_at=db.Column(db.DateTime(), onupdate=datetime.now())
    bookmarks=db.relationship("Bookmark", backref="user")

    def __repr__(self) -> str:
        return f"User>>> {self.username}"
    
    ### my custom function
    @classmethod
    def get_all(self):
        users_json = []
        users = User.query.all()
        for user in users:
            users_json.append({
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "password": user.password,
                    "created_at": user.created_at,
                    "updated_at": user.updated_at
            })

        return {"users": users_json}
    
    @classmethod
    def get_user(self, identifier: str):
        users = self.get_all()["users"]
        for user in users:
            if identifier in [user["id"], str(user["id"])] or user["email"] == identifier or user["username"] == identifier:

                user_json = {
                    "id": user["id"],
                    "email": user["email"],
                    "username": user["username"],
                    "password": user["password"],
                    "created_at": user["created_at"],
                    "updated_at": user["updated_at"]
                }
                
                return {"user": user_json}
        return {"user": {}}
    
    @classmethod
    def show_all(self) -> None:
        users = self.get_all()["users"]
        for user in users:
            self.show_user(user['id'])

    @classmethod
    def show_user(self, identifier: str) -> None:
        user = self.get_user(identifier)
        self.__show(user)

    @classmethod
    def __show(self, user: dict) -> None:
        user_data = user["user"]
        # import pdb
        # pdb.set_trace()
        if not user_data:
            print(f"Data not found")
            print(f"----")
        else:
            print(f"id: {user_data['id']}")
            print(f"email: {user_data['email']}")
            print(f"username: {user_data['username']}")
            print(f"password: {user_data['password']}")
            print(f"created_at: {user_data['created_at']}")
            print(f"updated_at: {user_data['updated_at']}")
            print(f"----")


    
    ### my custom function


class Bookmark(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    body=db.Column(db.Text(), nullable=True)
    url=db.Column(db.Text(), nullable=False)
    short_url=db.Column(db.String(3), nullable=False)
    visits=db.Column(db.Integer, default=0)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at=db.Column(db.DateTime(), default=datetime.now())
    updated_at=db.Column(db.DateTime(), onupdate=datetime.now())

    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters
        picked_chars = ''.join(random.choices(characters, k=3))

        # filter if it's unique from other short_url
        link = self.query.filter_by(short_url=picked_chars).first()
        if link:
            # generate new characters if it's exist on other short_url
            self.generate_short_characters()
        else:
            return picked_chars

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return f"Bookmarks>>> {self.url}"

