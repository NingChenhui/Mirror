# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 22:18:46 2020

@author: Riolu
"""
import json
with open("itime.db3.json",'r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)
    #print(load_dict)


record_type=[]

with open("things.json",'r',encoding='UTF-8') as load_f:
    things = json.load(load_f)

i=1000000
j=0
k=0
for category in things.keys():
    i=i+1000
    j=0
    for name in things[category].keys():
        j=j+1
        k=k+1
        item={}
        item["type_id"]=str(i+j)
        item["type_name"]=name
        #hex(-16777216 &0xFFFFFF)
        item["type_color"]=str(~int(0xffffff-eval('0x'+things[category][name][3][1:7])))
        item["order_id"]=str(k)
        
        record_type.append(item)
        
load_dict['itime.db3']['record_type']=record_type

with open("itime.db3.json","w",encoding='UTF-8') as dump_f:
    json.dump(load_dict,dump_f,ensure_ascii=False,indent = 1)
    