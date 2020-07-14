from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_SECRET_KEY"] ="henrique"
# app.secret_key = "henrique"
api = Api(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: #Instead of hard-coding, you should read from a config file or a database
        return {"is_admin": True}
    return {"is_admin": False}

@app.route("/")
def index():
    return(
        """
        <h1>Stores API with Flask &amp; FlaskRESTful</h1>
        <hr>
        <h3>Endpoints:</h3>
        <ul>
        <li>/items</li>
        <li>/item/&lt;name&gt;</li>
        <li>/auth</li>
        <li>/register</li>
        <li>/store/&lt;name&gt;</li>
        <li>/stores</li>
        </ul>
        <hr>
        """
    )

api.add_resource(Item, "/item/<string:name>")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, "/login")
