from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import pymysql
import json

from user import Login, UserAdd, User


app = Flask(__name__)
api = Api(app)


class Modis_download(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","ysman","123456","modis")
        self.cursor = self.db.cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("pagenumber",  type=int, default=1)
        self.get_args.add_argument("pageSize",  type=int, default=20)
        self.args = self.get_args.parse_args()

    def total_page(self, offset):
        sql = '''select count(*) from modis'''
        self.cursor.execute(sql)
        number = self.cursor.fetchone()
        return number[0]

    def get(self, pagenumber=0, pagesize=0):
        if not pagenumber or not  pagesize:
            pagenumber = self.args["pagenumber"]
            pagesize = self.args["pageSize"]

        total_page = self.total_page(pagesize)

        start_page = (pagenumber-1) * pagesize
        try:
            sql = '''select * from modis'''
            self.cursor.execute(sql)
            res = list(self.cursor.fetchall())
            ll = []
            for one in res:
                obj = {}
                obj["filename"] = one[0]
                obj["filepath"] = one[1]+ "/" + one[0]
                obj["create_time"] = str(one[2])
                ll.append(obj)
            data = {}
            data["data"] = ll
            data["count"] = len(ll)
            return data 
        except:
            print(1)
            return {}
