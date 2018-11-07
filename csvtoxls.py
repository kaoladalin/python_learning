#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import xlwt

list = []


def parsefile(filepath, mark):
    dic = {}
    try:
        begin = time.time()
        [des_filename, extname] = os.path.splitext(filepath)
        nfilename = des_filename + '_' + str("r") + extname
        f_read = open(filepath, encoding='UTF-8')
        rownum = 0
        for eachline in f_read:
            splitarr = eachline.split(mark)
            list.append(splitarr)
            rownum = rownum + 1
            if (rownum % 10000 == 0):
                print("[info]parse_file %s" % (rownum))
    except:
        print(sys.exc_info()[0], sys.exc_info()[1])
    finally:
        f_read.close()
        end = time.time()
        print("[info]======>format file %s  ,spend time %d s" % (filepath, (end - begin)))
        return dic;


def create_xls(file_path, list):
    styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour blue; font: bold on;')
    styleredBkg = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
    styleyellowBkg = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
    workbook = xlwt.Workbook(encoding = 'utf-8')
    sheet1 = workbook.add_sheet('库存状态', cell_overwrite_ok=True)
    for i, j in enumerate(list):
        if (i % 10000 == 0):
            print(" come to line %s " % (i + 1))
            for s, k in enumerate(j):
                sheet1.write(i, s, str(k),styleBlueBkg)
        else:
            for s, k in enumerate(j):
                if (str(k)=='无货'):
                    sheet1.write(i, s - 1,str(j[s-1]),styleyellowBkg)
                if (str(k)=='空'):
                    sheet1.write(i, s - 2,str(j[s-2]),styleredBkg)
                sheet1.write(i, s, str(k))
    file_path = file_path.replace('\\', '/')
    workbook.save(file_path)
    print('csv to excel finish!')
    return file_path


if __name__ == '__main__':
    srcfile = '/home/znniwal/study/inventory.csv'
    floder = os.path.dirname(os.path.realpath(__file__))
    srcfile=floder+u'/inventory.csv'
    print("srcfile:%s"%(srcfile))
    [des_filename, extname] = os.path.splitext(srcfile)
    parsefile(srcfile,'，')
    create_xls(des_filename + u"_r.xls", list)
