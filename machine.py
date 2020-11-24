from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import pymysql
import json
import MySQLdb

from user import Login, UserAdd, User


app = Flask(__name__)
api = Api(app)


class Updatemachine(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor =self.db. cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("data",  type=str)
        self.get_args.add_argument("year",  type=int)
        self.args = self.get_args.parse_args()

    def get(self):
        sdata = json.loads(self.args["data"])
        year = self.args["year"]

        obj = Getmachine()
        data  = obj.get()

        sql = '''update machineroom set zichanbiaoqian='%s', pinpai='%s', xinghao='%s', xuliehao='%s', shebeileixing='%s', shujuzhongxinweizhi='%s', jifangweizhi='%s',  jiguiweizhi='%s',gaodu='%s', shebeizhuangtai='%s', edinggonglv='%s', yongdiandengji='%s', guanliip='%s', yewuip='%s', beizhu='%s' where id =%d ''' % (sdata["zichanbiaoqian"], sdata["pinpai"], sdata["xinghao"],sdata["xuliehao"], sdata["shebeileixing"], sdata["shujuzhongxinweizhi"], sdata["jifangweizhi"], sdata["jiguiweizhi"], sdata["gaodu"],sdata["shebeizhuangtai"],sdata["edinggonglv"],sdata["yongdiandengji"], sdata["guanliip"],sdata["yewuip"],sdata["beizhu"], int(sdata["id"]))
        self.cursor.execute(sql)
        self.db.commit()
        return {"data": data, "message": "成功"}


class Delemachine(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor =self.db. cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("taskid",  type=int)
        self.get_args.add_argument("year",  type=int)
        self.args = self.get_args.parse_args()

    def get(self):
        taskid = self.args["taskid"]
        year = self.args["year"]

        obj = Getmachine()
        data  = obj.get(year)
        print(taskid)
        if not taskid:
            return {"data": data["data"], "message": "请规范操作"}

        sql = '''update machineroom set status=0 where id = %d ''' % taskid 
        print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        return {"data": data, "message": "删除成功"}


class Addmachine(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor =self.db. cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("data",  type=str)
        self.get_args.add_argument("year",  type=int)
        self.args = self.get_args.parse_args()

    def get(self):
        sdata = json.loads(self.args["data"])
        year = self.args["year"]
        userid = request.cookies.get('userid')

        obj = Getmachine()
        print(sdata)
        data  = obj.get(year)
        if not sdata[0]["zichanbiaoqian"]:
            return {"data": data["data"], "message": "您还没有输入数据"}

        for one in sdata:
            sql = '''insert into machineroom (zichanbiaoqian, pinpai, xinghao, xuliehao, shebeileixing, shujuzhongxinweizhi, jifangweizhi, jiguiweizhi, gaodu, shebeizhuangtai, edinggonglv, yongdiandengji, guanliip, yewuip, beizhu, status) values ('%s', '%s', '%s','%s', '%s','%s', '%s', '%s', '%s','%s', '%s','%s', '%s','%s', '%s', %d)''' % (one["zichanbiaoqian"], one["pinpai"], one["xinghao"], one["xuliehao"], one["shebeileixing"], one["shujuzhongxinweizhi"], one["jifangweizhi"],one["jiguiweizhi"], one["gaodu"], one["shebeizhuangtai"], one["edinggonglv"], one["yongdiandengji"], one["guanliip"], one["yewuip"], one["beizhu"], 1)
            self.cursor.execute(sql)
            self.db.commit()
        return {"data": data, "message": "成功"}


class Getmachine(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","mysql","mysql","ysman" )
        self.cursor = self.db.cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("pagenumber",  type=int, default=1)
        self.get_args.add_argument("pageSize",  type=int, default=10)
        self.args = self.get_args.parse_args()

    def total_page(self, offset, userid):
        sql = '''select count(id) from machineroom where status=1'''
        self.cursor.execute(sql)
        number = self.cursor.fetchone()
        return number[0]

    def get(self):
        userid = request.cookies.get('userid')
        pagenumber = self.args["pagenumber"]
        pagesize = self.args["pageSize"]
        total_page = self.total_page(pagesize, userid)

        start_page = (pagenumber-1) * pagesize
        sql = '''select * from machineroom  where status = 1 limit %d, %d''' %(start_page, pagesize)
        print(sql)
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        ll = []
        for one in res:
            u = one[2]
            if not one[2] or one[2] == "None":
                u = "其他"
            dd = {}
            dd["id"] = one[0]
            dd["zichanbiaoqian"] = one[1]
            dd["pinpai"] = one[2]
            dd["xinghao"] = one[3]
            dd["xuliehao"] = one[4]
            dd["shebeileixing"] = one[5]
            dd["shujuzhongxinweizhi"] = one[6]
            dd["jifangweizhi"] = one[7]
            dd["jiguiweizhi"] = one[8]
            dd["gaodu"] = one[9]
            dd["shebeizhuangtai"] = one[10]
            dd["edinggonglv"] = one[11]
            dd["yongdiandengji"] = one[12]
            dd["guanliip"] = one[13]
            dd["yewuip"] = one[14]
            dd["beizhu"] = one[15]
            dd["create_time"] = str(one[16])
            ll.append(dd)
        res = {}
        res["data"] = ll
        res["total_page"] = total_page
        return res
