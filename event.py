# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 22:15:47 2020

@author: Sinki
"""

class Event:
    '''
    活动
    '''
    
    def __init__(self,event):
        '''
        根据event生成新的对象
        	 {
            	"name": "初心纪念活动",
            	"start": "201101",
            	"end": "201121",
            	"gacha": [1,2,3]
             }
        '''
        self.event=event
        self.name=event['name']
        self.start=event['start']
        self.end=event['end']
        self.gacha=event['gacha']
        self.type=event['type']
        self.get=event['get']
        
        
    def show(self):
        print('活动名：',self.name)
        print('活动类型：',self.type)
        print('开始日期：',self.start)
        print('结束日期：',self.end)
        
        if self.got():
            print('已在',self.get,'集齐！')
        
    def updateTag(self):
        self.event['get']=self.get
        return self.event
    
    def got(self):
        if self.get=='999999':
            return False
        return True
    
    