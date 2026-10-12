from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.store import blp as StoreBlueprint
from resources.product import blp as ProductBlueprint
from resources.user import blp as UserBlueprint

app = Flask(__name__)

app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

app.config["JWT_SECRET_KEY"] = "super-secret-key"
jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({"message": "Request does not contain an access token.", "error": "authorization_required"}), 401

api = Api(app)

api.register_blueprint(StoreBlueprint)
api.register_blueprint(ProductBlueprint)
api.register_blueprint(UserBlueprint)

if __name__ == '__main__':
    app.run(debug=True)
