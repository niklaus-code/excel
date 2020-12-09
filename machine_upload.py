from flask import Flask, request, make_response, redirect
from flask_restful import Resource, Api, reqparse
from utils import Excel
from io import BytesIO
import pymysql
import os
import csv
from io import StringIO


ALLOWED_EXTENSIONS = set(['xlsx'])

app = Flask(__name__)
api = Api(app)


class Upload_file(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","ysman","123456","ysman" )
        self.cursor =self.db. cursor()
        self.get_args = reqparse.RequestParser()
        self.args = self.get_args.parse_args()

    def endwith(self, filename):
        if str.endswith(filename, "xlsx") or str.endswith(filename, "xls") or str.endswith(filename, "csv"):
            return True
        return False

    def insert(self, datalist):
        try:
            for one in datalist:
                sql = '''insert into machineroom (zichanbiaoqian, pinpai, xinghao, xuliehao, shebeileixing, shujuzhongxinweizhi, jifangweizhi, jiguiweizhi, gaodu, shebeizhuangtai, edinggonglv, yongdiandengji, guanliip, yewuip, beizhu, status) values ('%s', '%s', '%s','%s', '%s','%s', '%s', '%s', '%s','%s', '%s','%s', '%s','%s', '%s', %d)''' % (str(one[0]), str(one[1]), str(one[2]), str(one[3]), str(one[4]), str(one[5]), str(one[6]), str(one[7]), str(one[8]), str(one[9]), str(one[10]), str(one[11]), str(one[12]), str(one[13]), str(one[14]), 1)
                self.cursor.execute(sql)
                self.db.commit()
            return True
        except:
            return False
        

    def post(self):
        upload_file = request.files['file']
        filename = upload_file.filename

        if not self.endwith(filename):
            return False
        
        if os.path.splitext(filename)[-1] == ".csv":
            strfile = upload_file.read().decode('utf-8')
            f = StringIO(strfile, newline='')
            reader = csv.reader(f)
            res = self.insert(reader)
            return res

        exobj = Excel()
        data = exobj.get(f)
        res = self.insert(data)
        return data
