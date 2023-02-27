# Flask basic template


### Clone Repo
```bash
git clone ssh://git@0cool.space:8022/si_0216/flask-basic-template.git
```


# Request

### Auth: /auth

[Login]
```html
[POST] /login
```
```json
{
    "id":"admin",
    "passwd":"admin"
}
```

[Register]
```html
[POST] /register
```

```json
{
    "id":"admin",
    "passwd":"admin"
}
```


### Product: /product
[Get all products]
```html
[GET] /all (Need JWT)
```

[Get specific product]
```html
[GET] ?opt=[column]&val=[value] (Need JWT)
- only support 'SEQ', 'NAME'
```

[Get used product]
```html
[GET] /used (Need JWT)
```

[Get products total count by given column]
```html
[GET] /totals_by?col=[column] (Need JWT) (Admin)
- only support 'CATEGORY', 'VENDOR'
```

[Update product]
```html
[PUT] ?opt=[column]&val=[value] (Need JWT) (Admin)
- only support 'SEQ', 'NAME'
```

```json
{
    "name":"MACBOOK_CTO",
    "price":100000,
    "category":1,
    "vendor":1
}
```

[Delete product]
```html
[DELETE] ?opt=[column]&val=[value] (Need JWT) (Admin)
- only support 'SEQ', 'NAME'
```


### Order: /order

[Get Order]
```html
[GET] ?opt=[column]&val=[value] (Need JWT)
- only support 'buyer_id', 'order_id', 'order_date'
```

[Update Order]
```html
[PUT] ?order_id=[value] (Need JWT) (Admin)
- only support 'order_id'
```
```json
{
    "product_orders": [
      {
        "product_id": 1,
        "price": 1000000
      },
      {
        "product_id": 1,
        "price": 1000000
      }
    ],
    "total_price": 2000000,
    "total_quantity": 2
}
```

[Create Order]
```html
[POST] / (Need JWT) (Admin)
```
```json
{
    "buyer_id": 1,
    "order_id": "",
    "order_date": "",
    "product_orders": [
      {
        "product_id": 1,
        "price": 1000000
      },
      {
        "product_id": 1,
        "price": 1000000
      }
    ],
    "total_price": 2000000,
    "total_quantity": 2
}
```

### User: /user (Complex query)

[Get user's total order price by vendor]
```html
[GET] /vendor_total?seq=[value (user seq num)]
```


# Revise code

### DB
[main branch]
- fix app/db.py
  - MySql
  ```python
    def get_mysql():
    if 'mysql' not in g:
        g.mysql = pymysql.connect(
            user='[id]',
            passwd='[passwd]',
            host='[host address]',
            db='[db name]',
            charset='utf8'
        )
    return g.mysql
    ```
  - Oracle
  ```python
    def get_oracle():
    if 'oracle' not in g:
        g.oracle = cx_Oracle.connect('[User]','[Passwd]','[address]:[port]/XE')
    return g.oracle
    ```
  - Mongo
  ```python
  def get_mongo():
    if 'mongo' not in g:
        g.mongo = pymongo.MongoClient(f"mongodb://[id]:[passwd]@0cool.space:27017/?authSource=admin&"
                                      "readPreference=primary&"
                                      "appname=MongoDB%20Compass&ssl=false")
    return g.mongo
     ```
  MongoDB 사용 시, 라우터 정의부에 사용할 collection의 지정이 필요 EX: ```coll = mongo['Order']['order']```

[orm branch]
- fix app/init.py
  ```python
   app.config["SQLALCHEMY_DATABASE_URI"] = "oracle://[user]:[passwd]@[host address]:1521/xe"
      app.config["SQLALCHEMY_BINDS"] = {
          "mysql": "mysql+pymysql://[user]:[passwd]@[host address]:3306/cms"
      }
      app.config["MONGODB_SETTINGS"] = {
          "host": "mongodb://[user]:[passwd]0[host address]:[port]/[DB]?authSource=admin"
      }
  ```