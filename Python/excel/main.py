# -*- coding: gbk-*-

__author__ = 'lybc'
import excel
# import sys

def cut():
    filename = raw_input("������Ҫ������ļ�·��(���ļ�ֱ���ϵ������ڼ���): ")
    branch_index = input("��������Ҫ����һ���з�: ")
    branch_index = branch_index - 1
    ex = excel.excel()
    if filename:
        print("���ڴ���, ��ȴ�....")
        ex.branch_index = branch_index
        print(ex.cut(filename))
    option = raw_input("�������, �Ƿ����? (Y/N)")
    if option == "n" or option == "N":
        exit()


def merge():
    filename = raw_input("������Ҫ������ļ�·��: ")
    ex = excel.excel()
    if filename:
        print("���ڴ���, ��ȴ�....")
        print(ex.merge(filename))
    option = raw_input("�������, �Ƿ����? (Y/N)")
    if option == "n" or option == "N":
        exit()

def contract():
    filename = raw_input("������Ҫ������ļ�·��(���ļ�ֱ���ϵ������ڼ���): ")
    contract_index = input("��ͬ��������һ��: ")
    ex = excel.excel()
    if filename:
        print("���ڴ���, ��ȴ�....")
        ex.branch_index = contract_index - 1
        print(ex.filter_contract(filename))
    option = raw_input("�������, �Ƿ����? (Y/N)")
    if option == "n" or option == "N":
        exit()

if __name__ == "__main__":
    while(True):
        print("""
                       ��ӭʹ��EXCEL����С����!

                               _oo0oo_
                              o8888888o
                              88" . "88
                              (| -_- |)
                              0\  =  /0
                            ___/`---'\___
                          .' \\|     |// '.
                         / \\|||  :  |||// \
                        / _||||| -:- |||||- \
                       |   | \\\  -  /// |   |
                       | \_|  ''\---/''  |_/ |
                       \  .-\__  '-'  ___/-. /
                     ___'. .'  /--.--\  `. .'___
                  ."" '<  `.___\_<|>_/___.' >' "".
                 | | :  `- \`.:`\ _ /`:.`/ - ` : | |
                 \  \ `_.   \_ __\ /__ _/   .-` /  /
             =====`-.____`.___ \_____/___.-`___.-'=====
                               `=---='


             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

                       ���汣��         ����BUG

             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
             ��ѡ������Ҫ���еĲ���:
             1. ����ĳ�зָ��ļ�
             2. �ϲ�Ŀ¼�µ������ļ�
             3. ��������ɸѡ��ͬ��
        """)
        print("��ѡ��Ҫ���еĲ���: ")
        option = input()
        if option == 1:
            cut()
        elif option == 2:
            merge()
        elif option == 3:
            contract()