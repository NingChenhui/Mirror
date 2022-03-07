# -*- coding: utf-8 -*-
from diarything import*
from diarydraw import*
import datetime


class DayThings:
    '''
    储存一天的事件的类
    things  #事件列表
    time    #按事件大类的时间
    num     #事件总数
    cost    #事件花费
    totalTime #当天已记录时长
    '''
    def __init__(self):
        self.things=[]  #事件列表
        self.time={}    #按事件大类的时间
        self.doTime={}
        self.num=0      #事件总数
        self.totalTime=0
        
    def add(self,thing):
        ' 添加一个事件 按照事件的类别更新时间'
        self.things.append(thing)
        category=thing.category
        do=thing.do
        self.num+=1
        self.time[category]=self.time.get(category,0)+thing.duration
        self.doTime[do]=self.doTime.get(do,0)+thing.duration
        self.totalTime+=thing.duration
        
    
    def show(self):
        for thing in self.things:
            thing.show()
    def drawCategoryPie(self):
        '画一天的事情占比'
        print(self.time)
        data={}
        for c in self.time:
            data[c]=[self.time[c]]
        drawPie(data,'各事物总时间占比') 
        
    
class DiaryDay:
    '''
    储存一天所有属性的类
    self.date           #日期
    self.score          #心情分数
    self.weekdate       #星期几
    self.info           #在标题中附加的信息 和 日记中的重要信息
    self.weather        #今天的天气
    self.original       #数据源文
    self.text           #日记主要内容
    self.dream          #梦境
    self.things         #今天做的所有事
    self.attachments     #日记中的附件信息
    self.important       #大事事件戳
    self.places          #今天到的所有地点  ‘时刻 地点’
    '''
    
    
    def __init__(self,date):
        #tags=context.split()
        self.date=str(date.day)     #日期
        self.score=0       #心情分数
        self.weekdate=str(date.weekday()+1)     #星期几
        self.info={'标题信息':''}   #在标题中附加的信息 和 日记中的重要信息
        self.weather=''            #今天的天气
        self.original=[]        #数据源文
        self.things=DayThings() #今天做的所有事
        self.places=[]          #今天到的所有地点
        self.attachments=[]     #日记中的附件信息
        #self.aboutPerson={}     #对某个人的想法
        self.important=[]       #大事事件戳
        self.text=[]            #日记主要内容
        self.dream=[]
        self.cost=0
        
    def addThing(self,record):
        '添加事件'
        self.things.add(Thing(record))
        



    def analyse(self,context,lineNo):
        self.original.append(context)
        '【】标签单独占一行，优先处理'
        if context[0]=='【':
            split=context[1:].split('】')
            tags=split[1].split()
            for tag in tags:
                info=tag.split('：')
                infoi=self.info.get(split[0],{})
                infoi[info[0]]=info[1]
                self.info[split[0]]=infoi
            return
        if context[0] in '？?' :
            self.dream.append(context[1:])
            return 
        if context[0] in '#' :
            self.attachments.append(context[1:])
            return
        
        '处理日记内容，tag与text分离'
        splitSlash=context.split('/')
        try:
            self.text.append(splitSlash[1])
        except:
            pass
        if context[0] not in '1234567890*￥+':
            self.text.append(context)
            return
            
        '分析tags'
        tags=splitSlash[0].split()
        timeTag=[]
        
        i=0
        l=len(tags)
        while i<l:
            tag=tags[i]
            if tag[0] == '￥':
                try:
                    self.cost+=eval(tag[1:])
                except:
                    print('%error money at line ',context)        
            elif tag[0] == '+':
                '''
                names=tag[1:].split('，')
                for name in names:
                    self.aboutPerson[name]=self.aboutPerson.get(name,0)+1
                '''
                pass
            elif tag[0] == '*':
                self.important.append(tag[1:])
            elif isT(tags[i]) and isT(tags[i+1]):
                timeTag.append(timeDuration(tags[i],tags[i+1]))
                i+=1
                pass
            else:
                timeTag.append(tag)
            i+=1
        
        '''
        for i in range(len(tags)):
            tag=tags[i]
            if tag[0] == '￥':
                try:
                    self.cost+=eval(tag[1:])
                except:
                    print('%error money at line ',context)        
            elif tag[0] == '+':
                ''
                names=tag[1:].split('，')
                for name in names:
                    self.aboutPerson[name]=self.aboutPerson.get(name,0)+1
                ''
                pass
            elif tag[0] == '*':
                self.important.append(tag[1:])
            elif isT(tags[i]) and isT(tags[i+1]):
                timeTag.append(timeDuration(tags[i],tags[i+1]))
                i+=1
                pass
            else:
                timeTag.append(tag)
        '''
        i=0
        l=len(timeTag)
        #print(timeTag)
        '''
        while True:
            if i>=l:
                break
        '''
        while i<l:
            
            if isT(timeTag[i]):
                '''
                if timeTag[i+1] == '睡觉':
                    thing=Thing(timeDuration(timeTag[i],'3.')+' 睡觉')
                    self.things.add(thing)
                elif timeTag[i+1] == '起床':
                    thing=Thing(timeDuration('3.',timeTag[i])+' 起床')
                    self.things.add(thing)
                else:
                    '''
                self.places.append(timeTag[i+1])
                i+=2
                '''
            elif isD(timeTag[i]):
                s=timeTag[i]+' '+timeTag[i+1]
                i+=2
                if i<l:
                    if isD(timeTag[i])==False:
                        s=s+' '+timeTag[i]
                        i+=1
                thing=Thing(s)
                self.things.add(thing)
                '''
            else:
                print('%error thing at line ',context)
                x=input()
        
        
        
    def show(self):
        print('===========一天============')
        #print('日期:',self.date,'星期：',self.weekdate,'天气：',self.weather,'评分：',self.score)
        print('日期:',self.date,'星期：',self.weekdate)
        print('今天做的事：\n')
        self.things.show()
        #print('今天去的地方：\n',self.places)
        #print('今天去的地方时间：\n',self.timeAt)
        #print('今天花的钱：\n',round(self.cost,2))
        #print('日记中的附件：\n',self.attachments)
        #print('重要节点：\n',self.important)
        #print('重要信息：\n',self.info)
        #print('日记文本：\n',self.text)
        #print('相关人：\n',self.aboutPerson)
        
        
def isT(s):
    '判断是否为时刻'
    if '.' in s:
        if s.split('.')[0][0] in '1234567890':
            return True
    return False

def isD(s):
    '判断是否为时间'
    if s[0] in '1234567890':
        if '.' not in s:
            try:
                t=eval(s)
                return True
            except:
                return False
    return False
