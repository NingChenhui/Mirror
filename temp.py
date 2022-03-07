# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import json
with open("itime.db3.json",'r',encoding='UTF-8') as load_f:
    load_dict = json.load(load_f)
    #print(load_dict)
itime_data=load_dict['itime.db3']
record_type=itime_data['record_type']

record_type_index={}

for item in record_type:
    record_type_index[item['type_id']]=item

load_dict['itime.db3']['record_type'][0]['type_name']="工作_测试"
with open("itime.db32.json","w",encoding='UTF-8') as dump_f:
    json.dump(load_dict,dump_f,ensure_ascii=False,indent = 1)


'''
load_dict['smallberg'] = [8200,{1:[['Python',81],['shirt',300]]}]
print(load_dict)

with open("../config/record.json","w") as dump_f:
    json.dump(load_dict,dump_f)
    
with open("itime.db32.json","w",encoding='UTF-8') as dump_f:
    json.dump(load_dict,dump_f)
'''