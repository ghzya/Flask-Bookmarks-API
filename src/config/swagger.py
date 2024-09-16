template = {
  "swagger": "2.0",
  "info": {
    "title": "Bookmarks API",
    "description": "API for bookmarks",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "me@me.com",
      "url": "www.me.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
#   "host": "bookmarks-api.zip",  # overrides localhost:500
  "basePath": "/api/v1",  # base bash for blueprint registration
  "schemes": [
    "http",
    "https"
  ],
  "securityDefinitions": {
      "Bearer": {
          "type": "apiKey",
          "name": "Authorization",
          "in": "header",
          "description": "JWT Authorization header using Bearer scheme. Example: \"Authorization: Bearer {token}\""
      }
  },
  "operationId": "getmyData"
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,   # all in
            "mode_filter": lambda tag: True,    # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}

# swagger = Swagger(app, template=template)
