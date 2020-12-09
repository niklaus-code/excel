from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse

import pymysql
import json
import pandas as pd
import numpy as np
from io import BytesIO
import xlsxwriter

from user import Login, UserAdd, User


app = Flask(__name__)
api = Api(app)


class Getmachine_excel(Resource):
    def __init__(self):
        self.db = pymysql.connect("127.0.0.1","ysman","123456","ysman" )
        self.cursor = self.db.cursor()
        self.get_args = reqparse.RequestParser()
        self.args = self.get_args.parse_args()

    def get(self):
        sql = '''select zichanbiaoqian, pinpai, xinghao, xuliehao, shebeileixing, shujuzhongxinweizhi, jifangweizhi, jiguiweizhi, gaodu, shebeizhuangtai, edinggonglv, yongdiandengji, guanliip, yewuip, beizhu, DATE_FORMAT(create_time,'%Y%m%d') from machineroom  where status = 1 '''
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        all_machine = []
        for machine in res:
            machine_l = list(machine)
            if machine_l[9] == 1:
                machine_l[9] = "关机"
            else:
                machine_l[9] = "开机"
            all_machine.append(machine_l)

        data = np.array(all_machine)
        data_df = pd.DataFrame(data)
        data_df.columns = ['资产标签','品牌','型号','序列号','设备类型','数据中心位置','机房位置','机柜位置','高度','设备状态','额定功率','用电等级','管理IP','业务IP','备注','创建时间']
        #定义索引
        data_df = data_df.set_index('资产标签', drop=True)
        bio = BytesIO()
        writer = pd.ExcelWriter(bio, engine='xlsxwriter')
        data_df.to_excel(writer,float_format='%.5f')

        # 省略pandas处理结果，results为最后生成的dataframe对象
        data_df.to_excel(writer, sheet_name='机器统计')
        writer.save()

        bio.seek(0)    # 文件指针
        rv = make_response(bio.getvalue())
        bio.close()

        # mime_type = mimetypes.guess_type(results)[0]  # 文件类型
        rv.headers['Content-Type'] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        rv.headers["Cache-Control"] = "no-cache"
        rv.headers['Content-Disposition'] = 'attachment; filename={}.xls'.format('machine_count')
        return rv
