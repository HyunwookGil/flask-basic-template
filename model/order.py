from app.db import mongo
from datetime import date, datetime

class ProductOrder(mongo.DynamicEmbeddedDocument):
    product_id = mongo.IntField()
    price = mongo.IntField()


class Order(mongo.Document):
    buyer_id = mongo.IntField()
    order_id = mongo.StringField()
    order_date = mongo.StringField()
    product_orders = mongo.EmbeddedDocumentListField(ProductOrder)
    total_price = mongo.IntField()
    total_quantity = mongo.IntField()


    def issue_order_id(self):
        today = str(date.today().isoformat()).replace('-', '')
        now = str(datetime.now().strftime("%H%M%S"))

        self.order_date = str(date.today().isoformat())
        self.order_id = today + now

    def re_tally(self):
        self.total_price = sum([x.price for x in self.product_orders])
        self.total_quantity = len(self.product_orders)


    @classmethod
    def dict_to_cls(cls, json_dic):
        order = cls(**dict(json_dic))
        return order
