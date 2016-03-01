# -*- coding:utf-8 -*-
import xlsxwriter
import xlrd
import sys
import os
import re
from tqdm import tqdm
reload(sys)
sys.setdefaultencoding('utf-8')

class excel:
    excel_dict = {}
    branch_index = 2
    contract_index = 6
    sheet_index = 0
    reg = r"[A-Z]{2}[0-9]{7,9999}"

    def cut(self, filename):
        excel_dict = {}
        try:
            table = xlrd.open_workbook(filename)
            sheet = table.sheet_by_index(self.sheet_index)
        except:
            print("filename error please retry")
            exit()
        rows = sheet.nrows
        menu = sheet.row_values(0)
        for row_index in range(1, rows):
            row_data = sheet.row_values(row_index)
            branch = row_data[self.branch_index]
            if branch in excel_dict.keys():
                excel_dict[branch].append(row_data)
            else:
                excel_dict[branch] = []
                excel_dict[branch].append(row_data)
        dir_name = filename.split(".")[0]
        if not os.path.exists(dir_name):
            os.mkdir(dir_name[0])
        for company, data in tqdm(excel_dict.items()):
            workbook = xlsxwriter.Workbook(dir_name + "\\" + company + ".xlsx")
            worksheet = workbook.add_worksheet()
            menu_index = 0
            for m in menu:
                worksheet.write(0, menu_index, m)
                menu_index += 1
            x = 1
            for row in data:
                y = 0
                for field in row:
                    worksheet.write(x, y, field)
                    y += 1
                x += 1
            workbook.close()
        return dir_name

    def merge(self, dir_name):
        try:
            files = os.listdir(dir_name)
        except:
            print("filename error please retry")
            exit()
        merge_file_path = dir_name + "\merge.xlsx"
        workbook = xlsxwriter.Workbook(merge_file_path)
        worksheet = workbook.add_worksheet()
        x = 1
        menu = []
        for file_name in tqdm(files):
            file_path = dir_name + "\\" + file_name
            sheet = xlrd.open_workbook(file_path).sheet_by_index(self.sheet_index)
            rows = sheet.nrows
            menu = sheet.row_values(0)
            for row in range(1, rows):
                row_data = sheet.row_values(row)
                y = 0
                for data in row_data:
                    worksheet.write(x, y, data)
                    y += 1
                x += 1
        worksheet.write_row("A1", tuple(menu))
        workbook.close()
        return merge_file_path

    def filter_contract(self, filename):
        dir_name = filename.split(".")[0]
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        sheet = xlrd.open_workbook(filename).sheet_by_index(self.sheet_index)
        rows = sheet.nrows
        workbook = xlsxwriter.Workbook("{}\contract number.xlsx".format(dir_name))
        worksheet = workbook.add_worksheet()
        x = 1
        menu = sheet.row_values(0)
        menu.append("contract number")
        worksheet.write_row("A1", tuple(menu))
        for row_num in tqdm(range(1, rows)):
            text = sheet.cell_value(row_num, self.contract_index)
            row_data = sheet.row_values(row_num)
            y = 0
            contract = re.findall(self.reg, text)
            if contract:
                row_data.append(contract[0])
                for data in row_data:
                    worksheet.write(x, y, data)
                    y += 1
            x += 1
        workbook.close()