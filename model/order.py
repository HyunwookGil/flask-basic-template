from pydantic import BaseModel
from typing import List

import json
from datetime import date, datetime

class ProductOrder(BaseModel):
    product_id: int
    price: int


class Order(BaseModel):
    buyer_id: int
    order_id: str
    order_date: str
    product_orders: List[ProductOrder]
    total_price: int
    total_quantity: int

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)

    def issue_order_id(self):
        today = str(date.today().isoformat()).replace('-', '')
        now = str(datetime.now().strftime("%H%M%S"))

        self.order_id = today + now

    def re_tally(self):
        self.total_price = sum([x.price for x in self.product_orders])
        self.total_quantity = len(self.product_orders)


    @classmethod
    def dict_to_cls(cls, json_dic):
        order = cls(**dict(json_dic))
        return order
