# -*- coding:utf-8 -*-
import xlsxwriter
import xlrd
import sys
import os
reload(sys)
sys.setdefaultencoding('utf-8')

class excel:
    filename = "C:\Users\lybc\Desktop\SC0222.xls"
    excel_dict = {}

    def cut(self):
        filename = "C:\Users\lybc\Desktop\SC0222.xls"
        excel_dict = {}
        table = xlrd.open_workbook(filename)
        sheet = table.sheet_by_index(0)
        rows = sheet.nrows
        for row_index in range(1, rows):
            branch = sheet.cell(rowx=row_index, colx=1).value
            row_data = {
                "date": sheet.cell(rowx=row_index, colx=0).value,
                "csc": sheet.cell(rowx=row_index, colx=2).value,
                "contract": sheet.cell(rowx=row_index, colx=3).value,
                "number": sheet.cell(rowx=row_index, colx=4).value,
                "project": sheet.cell(rowx=row_index, colx=5).value,
                "lift": sheet.cell(rowx=row_index, colx=6).value,
                "units": sheet.cell(rowx=row_index, colx=7).value,
                "sman": sheet.cell(rowx=row_index, colx=8).value,
                "customerName": sheet.cell(rowx=row_index, colx=9).value,
                "comment": sheet.cell(rowx=row_index, colx=10).value
            }
            if branch in excel_dict.keys():
                excel_dict[branch].append(row_data)
            else:
                excel_dict[branch] = []

        dir_name = filename.split(".")[0]
        if not os.path.exists(dir_name):
            os.mkdir(dir_name[0])
        for company, data in excel_dict.items():
            workbook = xlsxwriter.Workbook(dir_name + "\\" + company + ".xlsx")
            worksheet = workbook.add_worksheet()
            row_index = 1
            worksheet.write(0, 0, "Date")
            worksheet.write(0, 1, "Branch")
            worksheet.write(0, 2, "CSC#")
            worksheet.write(0, 3, "Contract#")
            worksheet.write(0, 4, "")
            worksheet.write(0, 5, "Project")
            worksheet.write(0, 6, "Lift#")
            worksheet.write(0, 7, "Units")
            worksheet.write(0, 8, "Sman")
            worksheet.write(0, 9, u"客户名称")
            worksheet.write(0, 10, u"备注")
            for row in data:
                worksheet.write(row_index, 0, row["date"])
                worksheet.write(row_index, 1, company)
                worksheet.write(row_index, 2, row["csc"])
                worksheet.write(row_index, 3, row["contract"])
                worksheet.write(row_index, 4, row["number"])
                worksheet.write(row_index, 5, row["project"])
                worksheet.write(row_index, 6, row["lift"])
                worksheet.write(row_index, 7, row["units"])
                worksheet.write(row_index, 8, row["sman"])
                worksheet.write(row_index, 9, row["customerName"])
                worksheet.write(row_index, 10, row["comment"])
                row_index = row_index + 1
            workbook.close()

    def merge(self):
        dir_name = r"C:\Users\lybc\Desktop\SC0222\\"
        files = os.listdir(dir_name)
        merge_table = r"C:\Users\lybc\Desktop\SC0222\sc0222.xlsx"
        workbook = xlsxwriter.Workbook(merge_table)
        worksheet = workbook.add_worksheet()
        for filename in files:
            if u"~$" in filename:
                continue
            excel_file = dir_name + filename
            table = xlrd.open_workbook(excel_file)
            sheet = table.sheet_by_index(0)
            rows = sheet.nrows
            for row in range(0, rows):
                row_data = sheet.row_values(row)
                for i in range(0, len(row_data)):
                    worksheet.write(row, i, row_data[i])
        workbook.close()
ex = excel()
ex.merge()