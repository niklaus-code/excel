from flask import Flask, request, make_response, redirect
from flask_restful import Resource, Api, reqparse
from utils import Excel
from io import BytesIO
import pymysql
import os
import csv
from io import StringIO
from machine import Getmachine 


ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
api = Api(app)


class Upload_file(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","ysman","123456","ysman" )
        self.cursor =self.db. cursor()
        self.get_args = reqparse.RequestParser()
        self.get_args.add_argument("pagenumber",  type=int, default=1)
        self.get_args.add_argument("pagesize",  type=int, default=20)
        self.args = self.get_args.parse_args()

    def endwith(self, filename):
        if str.endswith(filename, "xlsx") or str.endswith(filename, "xls") or str.endswith(filename, "csv"):
            return True
        return False

    def insert(self, datalist, pagenumber, pagesize):
        dataobj = Getmachine()
        try:
            for one in datalist:
                sql = '''insert into machineroom (zichanbiaoqian, pinpai, xinghao, xuliehao, shebeileixing, shujuzhongxinweizhi, jifangweizhi, jiguiweizhi, gaodu, shebeizhuangtai, edinggonglv, yongdiandengji, guanliip, yewuip, beizhu, status) values ('%s', '%s', '%s','%s', '%s','%s', '%s', '%s', '%s','%s', '%s','%s', '%s','%s', '%s', %d)''' % (str(one[0]), str(one[1]), str(one[2]), str(one[3]), str(one[4]), str(one[5]), str(one[6]), str(one[7]), str(one[8]), str(one[9]), str(one[10]), str(one[11]), str(one[12]), str(one[13]), str(one[14]), 1)
                self.cursor.execute(sql)
                self.db.commit()
            data = dataobj.get(pagenumber, pagesize)
            return {"data": data, "message": True}
        except:
            data = dataobj.get(pagenumber, pagesize)
            return {"data": data, "message": False}
        

    def post(self):
        pagenumber = self.args["pagenumber"]
        pagesize = self.args["pagesize"]


        upload_file = request.files['file']
        filename = upload_file.filename

        if not self.endwith(filename):
            return False
    
        f = upload_file.read()
        if os.path.splitext(filename)[-1] == ".csv":
            strfile = f.decode('utf-8')
            f = StringIO(strfile, newline='')
            reader = csv.reader(f)
            res = self.insert(reader, pagenumber, pagesize)
            return res

        exobj = Excel()
        data = exobj.get(f)
        res = self.insert(data, pagenumber, pagesize)
        return res
