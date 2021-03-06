#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import xlwt
import re
from datetime import datetime
from functools import reduce

def process_log(log_file):
    date={}
    date_ave=[]
    pat_start=re.compile(r'(\d+)/(\d+)\s*(\d+):(\d+):(\d+),(\d+).+?ACTION\s*([a-zA-Z]+).+?started')
    pat_end=re.compile(r'(\d+)/(\d+)\s*(\d+):(\d+):(\d+),(\d+).+?ACTION\s*([a-zA-Z]+).+?finished')
    action_name_start = '' 
    action_name_end= ''
    start_time=end_time=datetime.now()
    with open(log_file,'r',encoding='UTF-8') as f:
        for eachline in f:
            m_start=pat_start.match(eachline)
            m_end=pat_end.match(eachline)
            if m_start:
                start_time=datetime(2018,int(m_start.group(1)),int(m_start.group(2)),int(m_start.group(3)),int(m_start.group(4)),int(m_start.group(5)),int(m_start.group(6))*1000)
                action_name_start=m_start.group(7)
            if m_end:
                end_time=datetime(2018,int(m_end.group(1)),int(m_end.group(2)),int(m_end.group(3)),int(m_end.group(4)),int(m_end.group(5)),int(m_end.group(6))*1000)
                action_name_end=m_end.group(7)
            if action_name_start == action_name_end and action_name_start != '' and action_name_end != '':
                dutation=(end_time-start_time).seconds+(end_time-start_time).microseconds/1000000
                if action_name_end not in date.keys():
                    date[action_name_end]=[]
                date[action_name_end].append('%.3f' % dutation)
                action_name_start=''
                action_name_end=''  
    
    for key,value in date.items():
        each_line=[]
        each_line.append(key)
        times=len(value)
        value=list(map(float,value))
        average=reduce(lambda x,y:x+y,value)
        each_line.append('%.3f' % average)
        each_line.append(times)
        date_ave.append(each_line)
    date_ave=sorted(date_ave,key=lambda date_ave:date_ave[2])
    return date_ave

def create_xls(*date_ave):
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet=workbook.add_sheet('log_stats', cell_overwrite_ok=True)
    style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow')
    sheet.write(0, 0, 'action_name')
    sheet.write(0, 1, 'average_time')
    sheet.write(0, 2, 'frequency')
    for i, date in enumerate(date_ave):
        for j, each_line in enumerate(date): 
            if float(each_line[1]) >= 2:
                for k,value in enumerate(each_line):
                    sheet.write(j+1, k, value, style)
            else:
                for k,value in enumerate(each_line):
                    sheet.write(j+1, k, value)
    workbook.save('log.xls')        
   
if __name__ == '__main__':
    floder = os.path.dirname(os.path.realpath(__file__))
    srcfile = floder + u'/case_log.txt'
    print("srcfile:%s" % (srcfile))
    log_date=process_log(srcfile)
    create_xls(log_date)


