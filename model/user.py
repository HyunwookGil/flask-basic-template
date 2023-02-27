from app.db import sql
from .converter import json_converter

class User(sql.Model):
    __tablename__ = "User"
    __bind_key__ = "mysql"

    seq = sql.Column(sql.Integer, primary_key=True)
    id = sql.Column(sql.String(100), nullable=False)
    passwd = sql.Column(sql.String(100), nullable=False)

    @property
    def json(self):
        return json_converter.to_json(self, self.__class__)
