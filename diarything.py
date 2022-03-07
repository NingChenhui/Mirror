# -*- coding: utf-8 -*-
import datetime
class Thing:
    '''
    基本的事件单元对象
    tag             #生成这件事的源tag
    do              #这是件什么事
    money           #这件事所消耗的钱
    withPerson      #与谁一起做这件事
    category        #这件事所属的类别
    duration        #这件事持续的时长
    what            #这件事的其他属性
    at              #在哪里做的事
    
    things规定了每件事的属性和传入参数的格式
    最后两个为单位时间获得的exp，light的权重
    places规定了各地点的加成值
    '''
    
    import json
    with open("itime.db3.json",'r',encoding='UTF-8') as load_f:
        load_dict = json.load(load_f)
    record_type_index={}        #通过id识别事件
    record_type_name={}
    for item in load_dict['itime.db3']['record_type']:
        record_type_index[item['type_id']]=item['type_name']
        record_type_name[item['type_name']]=item['type_id']
        
    with open("things.json",'r',encoding='UTF-8') as load_f:
        things = json.load(load_f)      #事件种类
    
    places={
            '宿舍',
            '图书馆',
            '教学楼',
            '食堂',
            '操场',
            '大活',
            '机房',
            '清水亭',
            }
    
    def __init__(self,record):
        '通过record信息生成一个实例'
        '''
        eg 
        record={
            "record_id": "1582387031233",
            "start_time": "19:56",
            "end_time": "20:09",
            "interval_minites": "13",
            "year": "2020",
            "month": "2",
            "day": "22",
            "type_id": "100005",
            "comment": ""
           }
        '''
        

        #self.tag=tag            #生成这件事的源tag
        self.do=self.record_type_index[record['type_id']] #这是件什么事
        self.tag=self.do+'-'+record['comment']+'-'+record['interval_minites']
        #self.money=0            #这件事所消耗的钱
        #self.withPerson=None    #与谁一起做这件事
        self.category=None      #这件事所属的类别
        if 'start_time' in record.keys():  #只有启用年终总结时才应使用啊
            self.start_time=record['start_time']
            self.end_time=record['end_time']
        


        self.duration=eval(record['interval_minites'])         #这件事持续的时长
        self.what={}            #这件事的其他属性
        self.update=record['update']
        #self.at=None
        

        '处理其他类型事件'
        for category in self.things.keys():
            if self.do in self.things[category]:
                self.category=category
                
                part=record['comment']
                #print('part',part)
                mode=self.things[category][self.do][:-2]
                #print('mode',mode)
                if mode[0]!='':
                    if part=='':
                        "print('miss info')"
                        'print(self.tag)'
                    else:
                        self.what[mode[0]]=part
                        'print("successfully add")'
                        'print(self.tag)'
        if self.category==None:
            print('%no category:',self.tag)
                        
        #self.show()
    def show(self):
        #print('===========事件============')
        print(self.do,end=' ')
        print('时长：',self.duration,end=' ')
        print('类别：',self.category,end=' ')
        print(self.what)
    def getIndex(cls,do):
        return cls.record_type_name[do]


def timeDuration(tx,ty):
    '传入两个时刻，计算经过的时间'
    '''
    if '.' not in tx:
        tx=tx+'.0'
    if '.' not in ty:
        ty=ty+'.0'
    '''
    [hx,mx]=tx.split('.')
    [hy,my]=ty.split('.')
    hx=eval(hx)
    hy=eval(hy)
    if my=='':
        my='0'
    if mx=='':
        mx='0'
    
    if my[0]=='0'and len(my)>1:
        my=my[1]
    if mx[0]=='0' and len(mx)>1:
        mx=mx[1]
    mx=eval(mx)
    my=eval(my)

    if hy<hx:
        if hy!=3:
            print('%warning:',end='')
            print('%计算时间差：',tx,ty)
        hy+=24
    
    t=(hy-hx)*60+my-mx
    #print(t)
    return str(t)
