import pymysql
import pymongo
import importlib
cx_Oracle = importlib.import_module('cx_Oracle')

from flask import g


def get_mysql():
    if 'mysql' not in g:
        g.mysql = pymysql.connect(
            user='root',
            passwd='0cool-0070',
            host='0cool.space',
            db='cms',
            charset='utf8'
        )
    return g.mysql

def get_oracle():
    if 'oracle' not in g:
        g.oracle = cx_Oracle.connect('SYSTEM','0cool-0070','0cool.space:1521/XE')
    return g.oracle


def get_mongo():
    if 'mongo' not in g:
        g.mongo = pymongo.MongoClient(f"mongodb://admin:0cool-0070@0cool.space:27017/?authSource=admin&"
                                      "readPreference=primary&"
                                      "appname=MongoDB%20Compass&ssl=false")
    return g.mongo


def close_mysql(e=None):
    print("Close MySql, (TearDown)")
    db = g.pop('mysql', None)
    if db is not None:
        db.close()


def close_oracle(e=None):
    print("Close Oracle, (TearDown)")
    db = g.pop('oracle', None)
    if db is not None:
        db.close()


def close_mongo(e=None):
    print("Close Mongo, (TearDown)")
    mongo = g.pop('mongo', None)
    if mongo is not None:
        mongo.close()


def init_app(app):
    app.teardown_appcontext(close_mysql)
    app.teardown_appcontext(close_oracle)
    app.teardown_appcontext(close_mongo)
