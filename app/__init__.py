from flask import Flask
from flask_jwt_extended import *

from app.router import landing
from app.router import product
from app.router import order
from app.router import auth
from app.router import user

from .db import *

def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="0cool-0070",
    )

    app.config.update(
        JWT_SECRET_KEY="0cool.space"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "oracle://SYSTEM:0cool-0070@0cool.space:1521/xe"
    app.config["SQLALCHEMY_BINDS"] = {
        "mysql": "mysql+pymysql://root:0cool-0070@0cool.space:3306/cms"
    }
    app.config["MONGODB_SETTINGS"] = {
        "host": "mongodb://admin:0cool-0070@0cool.space:27017/Order?authSource=admin"
    }

    # put app down sql-alchemy
    sql.init_app(app)
    # put app down mongoengine
    mongo.init_app(app)
    # put app down dbms object
    init_app(app)

    app.register_blueprint(landing.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(user.bp)

    JWTManager(app)

    print("Make flask app!")
    return app
