import uuid
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token
from db import users
from schemas import UserSchema

blp = Blueprint("users", __name__, description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        for user in users.values():
            if user["username"] == user_data["username"]:
                abort(409, message="A user with that username already exists.")

        user_id = uuid.uuid4().hex
        user = {
            "id": user_id,
            "username": user_data["username"],
            "password": pbkdf2_sha256.hash(user_data["password"])
        }
        users[user_id] = user
        return {"message": "User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        for user in users.values():
            if user["username"] == user_data["username"] and pbkdf2_sha256.verify(user_data["password"], user["password"]):
                access_token = create_access_token(identity=user["id"])
                return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials.")
