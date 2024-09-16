from flask import Flask, jsonify, redirect, url_for, send_from_directory
import os
from flask_jwt_extended import JWTManager

from src.constants.http_status_code import *
from src.database import db, Bookmark
from src.auth import auth
from src.bookmarks import bookmarks
from src.admin import admin

from flasgger import Swagger, swag_from
from src.config.swagger import template, swagger_config


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Initialize configuration
    if test_config is None:
        app.config.from_mapping(
            # SECRET_KEY="dev",
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY"),

            SWAGGER={
                "title": "Bookmark API",
                "uiversion": 3
            }
        )
    else:
        app.config.from_mapping(test_config)

    # Initialize database
    db.app = app
    db.init_app(app)

    # Initialize JWT manager
    JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    app.register_blueprint(admin)

    Swagger(app, config=swagger_config, template=template)

    @app.get("/api/v1/<short_url>")
    @swag_from('./docs/short_url.yaml')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits = bookmark.visits + 1 
            db.session.commit()

            return redirect(location=bookmark.url, code=302)
        
        # return jsonify({
        #     "message": "Item not found"
        # }), 404


    # default page
    # @app.get("/")
    # def index():
    #     return "Hello World!"

    @app.get("/hello")
    def say_hello():
        return jsonify({"message": "Hello World"})
    

    # return favicon
    @app.route('/favicon.ico')
    def favicon():
        # method 1 (not recommended because it also return the path)
        # return redirect(url_for('static', filename='favicon.ico'), code=302)
        # method 2
        # return send_from_directory(
        #     os.path.join((app.root_path), 'static'),
        #     "favicon.ico", mimetype="image/vnd.microsof.icon"
        # )
        # method 3
        return send_from_directory(
            'static',
            'favicon.ico',
            mimetype='image/vnd.microsoft.icon'
        )
        # return jsonify({
        #     "error": "favicon not found"
        # }), HTTP_404_NOT_FOUND
    

    # error handling
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({
            "error": "Not found"
        }), HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({
            "error": "Something went wrong, we are working on it"
        }), HTTP_500_INTERNAL_SERVER_ERROR

## error handling checkpoint

    return app


