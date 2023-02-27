from flask import Flask
from flask_jwt_extended import *

from app.router import landing
from app.router import product
from app.router import order
from app.router import auth
from app.router import user

from . import db

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

    app.register_blueprint(landing.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(product.bp)
    app.register_blueprint(order.bp)
    app.register_blueprint(user.bp)

    JWTManager(app)
    db.init_app(app)

    print("Make flask app!")
    return app
