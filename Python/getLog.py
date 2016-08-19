# coding: utf-8
import MySQLdb
import xlsxwriter
from pprint import pprint
import argparse
from tqdm import tqdm
import time


class downloadLog():
    __host = ''
    __username = ''
    __passwd = ''
    __db = 'lenovo'
    __path = ''

    def __init__(self):
        self.conn = MySQLdb.connect(
            host=self.__host,
            user=self.__username,
            passwd=self.__passwd,
            db=self.__db,
        )
        self.cursor = self.conn.cursor(MySQLdb.cursors.DictCursor)

    def export(self, serviceOrderCode = ''):
        sql = "select id,userId,uname,companyId,name,request,old,new,success,createTime,url from Log where new like '%{}%'"
        filename = self.__path + serviceOrderCode + '.xlsx'
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        menu = ['id', 'userId', 'uname', 'companyId', 'name', 'request', 'old', 'new', 'success', 'createTime', 'url']
        x = y = 0
        for m in menu:
            worksheet.write(x, y, m)
            y += 1
        x = x + 1
        self.cursor.execute(sql.format(serviceOrderCode))
        result = self.cursor.fetchall()
        for row in result:
            y = 0
            worksheet.write(x, y, row['id'])
            worksheet.write(x, y + 1, row['userId'])
            worksheet.write(x, y + 2, row['uname'])
            worksheet.write(x, y + 3, row['companyId'])
            worksheet.write(x, y + 4, row['name'])
            worksheet.write(x, y + 5, row['request'])
            worksheet.write(x, y + 6, row['old'])
            worksheet.write(x, y + 7, row['new'])
            worksheet.write(x, y + 8, row['success'])
            worksheet.write_datetime(x, y + 9, row['createTime'])
            worksheet.write_url(x, y + 10, row['url'])
            x += 1
        workbook.close()


    def main(self, srs):
        if srs is not None:
            print "#### 开始导出... ####"
            start = time.time()
            srs = srs.split(',')
            for sr in tqdm(srs):
                self.export(sr)
            end = time.time()
            print "#### 成功导出{}单，共用时{}秒 ####".format(len(srs), end-start)
        # self.export('dlallsddkdkdkf')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help="input serviceOrder code")
    args = parser.parse_args()
    if args.s:
        log = downloadLog()
        log.main(args.s)