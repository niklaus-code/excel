import hmac, random
import xlrd


class Encryption(object):

    def __init__(self):
        self.key = "bigdata"

    def hmac_md5(self, s):
        return hmac.new(self.key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()


class Excel(object):

    def __init__(self):
        pass

    def get(self, excelfile):
        workbook = xlrd.open_workbook(file_contents=excelfile)
        sheet_name = workbook.sheet_names()[0]

        # 根据sheet索引或者名称获取sheet内容
        sheet = workbook.sheet_by_index(0)

        ncols = sheet.ncols
        nrows = sheet.nrows

        all_data = []
        for i in range(nrows):
            if i == 0:
                continue
            all_data.append(sheet.row_values(i))
        return all_data
