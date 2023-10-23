from flask_restful import Resource, reqparse
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token

from models.user import UserModel

class UserRegister(Resource):
    """
    This resource allows user to register by sending a
    POST request with their username and password.
    """
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 409
        
        user = UserModel(
            username = data["username"],
            password = pbkdf2_sha256.hash(data["password"])
        )
        user.save_to_db()

        return {"message": "User created successfully."}, 201
    

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field cannot be blank")
    
    def post(self):
        user_data = UserRegister.parser.parse_args()

        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id,)
            return {"access_token": access_token, "refresh_token": refresh_token}
        else:
            return {"message": "Invalid credentials."}, 401