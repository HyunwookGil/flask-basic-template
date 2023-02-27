from app.db import sql
from .converter import json_converter


class Product(sql.Model):
    seq = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(100), nullable=False)
    price = sql.Column(sql.Integer, primary_key=True)
    category = sql.Column(sql.Integer, primary_key=True)
    vendor = sql.Column(sql.Integer, primary_key=True)

    @property
    def json(self):
        return json_converter.to_json(self, self.__class__)

    def __getitem__(self, x):
        return getattr(self, x)
