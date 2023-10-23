import os

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister, UserLogin

app = Flask(__name__)

app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

app.config["JWT_SECRET_KEY"] = "robert" # Gen a secret
jwt = JWTManager(app)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/auth")

@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {"description": "Request does not contain an access token", "error": "authorization_required"}
        ),
        401
    )

if __name__ == '__main__':
    from db import db

    db.init_app(app)

    if app.config['DEBUG']:
        #@app.before_first_request
        #def create_tables():
        with app.app_context():
            db.create_all()

    app.run(port=5000)
