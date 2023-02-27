from app import create_app
from flask_jwt_extended import *

app = create_app()
jwt = JWTManager(app)