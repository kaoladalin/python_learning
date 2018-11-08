#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import xlwt
list=[]

def parsefile(filepath, mark):
    l=[]
    begin = time.time()
    #[des_filename, extname] = os.path.splitext(filepath)
    #nfilename = des_filename + '_' + str("r") + extname
    f_read = open(filepath, encoding='UTF-8')
    i=1
    for eachline in f_read:
        if i == 1:
            splitarr=eachline.split(mark)
            list.append(splitarr)
            i = i+1
        else:
            splitarr = eachline.split(mark)
            l.append(splitarr)
    l= sorted(l,key=lambda num : num[0])
    list.extend(l)
    f_read.close()
    end = time.time()
    print("[info]======>format file %s  ,spend time %d s" % (filepath, (end - begin)))


def create_xls(file_path, list):
    styleBlueBkg = xlwt.easyxf('pattern: pattern solid, fore_colour blue; font: bold on;')
    styleredBkg = xlwt.easyxf('pattern: pattern solid, fore_colour red;')
    styleyellowBkg = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet1 = workbook.add_sheet('库存状态', cell_overwrite_ok=True)
    for i, j in enumerate(list):
        if i == 0:
            print(" come to line %s " % (i + 1))
            for s, k in enumerate(j):
                sheet1.write(i, s, str(k), styleBlueBkg)
        else:
            for s, k in enumerate(j):
                if str(k) == '无货':
                    sheet1.write(i, 1, str(j[1]), styleyellowBkg)
                if len(j) < 4 :
                    sheet1.write(i, 1, str(j[1]), styleredBkg)
                sheet1.write(i, s, str(k))
    file_path = file_path.replace('\\', '/')
    workbook.save(file_path)
    print('csv to excel finish!')
    return file_path


if __name__ == '__main__':
    srcfile = '/home/znniwal/study/inventory.csv'
    floder = os.path.dirname(os.path.realpath(__file__))
    srcfile = floder + u'/inventory.csv'
    print("srcfile:%s" % (srcfile))
    [des_filename, extname] = os.path.splitext(srcfile)
    parsefile(srcfile, '，')
    create_xls(des_filename + u"_r.xls", list)

