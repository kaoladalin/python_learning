#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import xlwt
import re
from datetime import datetime
from functools import reduce

def process_log_action(log_file):
    date={}
    date_ave=[]
    pat_start=re.compile(r'(\d+)/(\d+)\s*(\d+):(\d+):(\d+),(\d+).+?ACTION\s*([a-zA-Z]+).+?started')
    pat_end=re.compile(r'(\d+)/(\d+)\s*(\d+):(\d+):(\d+),(\d+).+?ACTION\s*([a-zA-Z]+).+?finished')
    action_name_start = ''
    action_name_end= ''
    start_time=end_time=datetime.now()
    with open(log_file,'r',encoding='UTF-8') as f:
   # with open(log_file,'r') as f:
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
        average=reduce(lambda x,y:x+y,value)/times
        each_line.append('%.3f' % average)
        each_line.append(times)
        date_ave.append(each_line)
    date_ave=sorted(date_ave,key=lambda date_ave:date_ave[2])
    return date_ave

def process_log(log_file):
    date_act_start={}
    date_act_end={}
    date_act={}
    date_act_ave=[]
    date_opt_start={}
    date_opt_end={}
    date_opt={}
    date_opt_ave=[]
    L=[]
    with open(log_file,'r',encoding='UTF-8') as f:
    #with open(log_file,'r') as f:
        for eachline in f:
            if re.findall('OPERATION',eachline):
                L=eachline.split()
                operation_name=L[4]
                if L[5] == '[started]':
                    time_str='2018'+' '+L[0]+' '+L[1]
                    start_time=datetime.strptime(time_str,'%Y %m/%d %H:%M:%S,%f')
                    if operation_name not in date_opt_start.keys():
                        date_opt_start[operation_name]=[]
                    date_opt_start[operation_name].append(start_time)
                if L[5] == '[finished]':
                    time_str='2018'+' '+L[0]+' '+L[1]
                    end_time=datetime.strptime(time_str,'%Y %m/%d %H:%M:%S,%f')
                    if operation_name not in date_opt_end.keys():
                        date_opt_end[operation_name]=[]
                    date_opt_end[operation_name].append(end_time)
            if re.findall('ACTION',eachline):
                L=eachline.split()
                operation_name=L[4]
                if L[5] == '[started]':
                    time_str='2018'+' '+L[0]+' '+L[1]
                    start_time=datetime.strptime(time_str,'%Y %m/%d %H:%M:%S,%f')
                    if operation_name not in date_act_start.keys():
                        date_act_start[operation_name]=[]
                    date_act_start[operation_name].append(start_time)
                if L[5] == '[finished]':
                    time_str='2018'+' '+L[0]+' '+L[1]
                    end_time=datetime.strptime(time_str,'%Y %m/%d %H:%M:%S,%f')
                    if operation_name not in date_act_end.keys():
                        date_act_end[operation_name]=[]
                    date_act_end[operation_name].append(end_time)

    for key in date_opt_start.keys():
      #  date_opt[key]=map('%.3f' % (lambda x,y:(y-x).seconds+(y-x).microseconds/1000000,date_opt_start[key],date_opt_end[key]))
        date_opt[key]=[]
        for i in range(len(date_opt_start[key])):
            duration=(date_opt_end[key][i]-date_opt_start[key][i]).seconds+(date_opt_end[key][i]-date_opt_start[key][i]).microseconds/1000000
            date_opt[key].append('%.3f' % (duration))

    for key,value in date_opt.items():
        each_line=[]
        each_line.append(key)
        times=len(value)
        value=list(map(float,value))
        average=reduce(lambda x,y:x+y,value)/times
        each_line.append('%.3f' % average)
        each_line.append(times)
        date_opt_ave.append(each_line)
    date_opt_ave=sorted(date_opt_ave,key=lambda date_opt_ave:date_opt_ave[2])

    for key in date_act_start.keys():
      #  date_act[key]=map('%.3f' % (lambda x,y:(y-x).seconds+(y-x).microseconds/1000000,date_act_start[key],date_act_end[key]))
        date_act[key]=[]
        for i in range(len(date_act_start[key])):
            duration=(date_act_end[key][i]-date_act_start[key][i]).seconds+(date_act_end[key][i]-date_act_start[key][i]).microseconds/1000000
            date_act[key].append('%.3f' % (duration))

    for key,value in date_act.items():
        each_line=[]
        each_line.append(key)
        times=len(value)
        value=list(map(float,value))
        average=reduce(lambda x,y:x+y,value)/times
        each_line.append('%.3f' % average)
        each_line.append(times)
        date_act_ave.append(each_line)
    date_act_ave=sorted(date_act_ave,key=lambda date_act_ave:date_act_ave[2])

    return date_opt_ave,date_act_ave


def create_xls(date_act_ave,date_opt_ave):
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet1=workbook.add_sheet('date_action', cell_overwrite_ok=True)
    sheet2=workbook.add_sheet('date_opteration', cell_overwrite_ok=True)
    style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow')
    sheet1.write(0, 0, 'action_name')
    sheet1.write(0, 1, 'average_time')
    sheet1.write(0, 2, 'frequency')
    sheet2.write(0, 0, 'operation_name')
    sheet2.write(0, 1, 'average_time')
    sheet2.write(0, 2, 'frequency')
    for i, each_line in enumerate(date_act_ave):
        if float(each_line[1]) >= 2:
            for j,value in enumerate(each_line):
                sheet1.write(i+1, j, value, style)
        else:
            for j,value in enumerate(each_line):
                sheet1.write(i+1, j, value)
    for i, each_line in enumerate(date_opt_ave):
        if float(each_line[1]) >= 2:
            for j,value in enumerate(each_line):
                sheet2.write(i+1, j, value, style)
        else:
            for j,value in enumerate(each_line):
                sheet2.write(i+1, j, value)
    workbook.save('log_date.xls')

if __name__ == '__main__':
    floder = os.path.dirname(os.path.realpath(__file__))
    srcfile = floder + u'/case_log.txt'
    print("srcfile:%s" % (srcfile))
    #log_date=process_log_action(srcfile)
    date_opt,date_act=process_log(srcfile)
    create_xls(date_act,date_opt)
