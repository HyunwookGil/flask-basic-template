from flask_jwt_extended import *

is_admin = lambda: False if get_jwt_identity() != "admin" else True
