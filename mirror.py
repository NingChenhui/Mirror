# -*- coding: utf-8 -*-
from diarymonth import*
from diarything import*
from diaryyear import*
from card import Card
from event import Event
import time
import random



class Backpack:
    '''
    持有物
    '''
    
    def __init__(self,backpack):
        '''
        根据backpack生成新的对象
        	 "backpack": {
            	"cards": [{'id':str,'num':int}],
            	"shop": []
             }
        '''
        self.backpack=backpack
        self.cards=backpack['cards']
        
    def show(self):
        print(self.backpack)
        
    def hasCard(self,card):
        for myCard in self.cards:
            if myCard['id'] == card.id:
                return True
        return False
    
    def pushCard(self,card):
        if self.hasCard(card):
            for i in range(len(self.cards)):
                if self.cards[i]['id'] == card.id:
                    self.cards[i]['num'] += 1
                    break
        else:
            self.cards.append({"id":card.id,"num":1})
        
    def save(self):
        self.backpack['cards']=self.cards
        return self.backpack

class Task:
    '''
    存储一个任务
    tag：    生成任务所有信息的源
    task：   生成事件的源
    ddl：    任务截止时间，没有的话为无穷大。eg：'181210'
    info：   任务描述
    progress：任务目前进度
    thing：  任务内容，以Thing存储 时长为0则为特殊任务
    exp：    完成任务的奖励exp值
    light：  完成任务的奖励light值
    achievement：完成任务的成就称号
    finishDate：任务完成时间,未完成为‘999999’
    finishTimes：任务完成次数
        
    
    * 主线任务
    % 日常任务
    '''
    
    
    
    def __init__(self,task):
        '''
        根据tag生成新的Task对象
        tag eg: 复习-数分-60/0 0/999999 999999/沉迷 10 10/日常任务 学习数分一小时'
        '''
        #if task["type_id"]==0:
        task["type_id"]=Thing.getIndex(Thing,task['type'])
        self.task=task
        self.thing=Thing(task)
        self.achievement=task['achievement']
        self.exp=task['exp']
        self.light=task['light']
        self.finishDate=task['finishDate']
        self.ddl=task['ddl']
        self.progress=task['progress']
        self.finishTimes=task['finishTimes']
        self.info=task['info']
        

        
    def check(self,thing,date):
        '''
        更新任务进度并检查在进行的任务是否完成。完成返回True
        仅用于按时长的任务
        thing 为做的事
        date 为做的日期
        '''
        #print(self.thing.what.values())
        
        isC=True#为真是广泛事物
        for v in self.thing.what.values():
            if v != '':
                isC=False
                break
        #print(thing.what)
        #print(self.thing.what)
        if (self.thing.do!=thing.do) or ((not (thing.what == self.thing.what)) and isC==False):
            return False
        
        
        
        self.progress+=thing.duration
        
        #if (thing.do == '游戏') and (self.thing.do == '游戏'):
        #    print(self.progress)
        if  self.finishDate!='999999':#有完成日期的不能再次完成
            return False

        if self.progress>=self.thing.duration and self.thing.duration!=0 and date<=self.ddl:
            self.finishDate=date
            self.finishTimes+=1
            print('任务 完！成！辣！')
            self.show()
            if self.task["is_main"]:
                self.progress=0
            return True
        return False

    def show(self):
        print('任务内容：',self.info)
        print('任务奖励：','达成成就"%s"'%self.achievement,'%+d exp'%self.exp,'%+d light'%self.light)
        if self.thing.duration!=0:
            print('任务进度：','%d/%d'%(self.progress,self.thing.duration))
        print('任务状况：完成%d次'%self.finishTimes)
        if self.finishDate!='999999':
            print('完成日期：',self.finishDate,'\n')
        if self.ddl!='999999':
            print('截止日期：',self.ddl,'\n')
            
    def updateTag(self):
        '''
        info=self.thing.tag+'/'+str(self.progress)+' '+str(self.finishTimes)+'/'+self.finishDate\
                +' '+self.ddl+'/'+self.reward+'/'+self.info+'\n'
        self.tag=self.tag[0]+info
        '''
        self.task["finishTimes"]=self.finishTimes
        self.task["progress"]=self.progress
        self.task['finishDate']=self.finishDate
        return self.task
    
class Mirror:
    '''
    镜子系统
    context：源数据
    lv：     当前等级
    exp：    总经验
    light：  光（系统货币）
    new：    上次更新到的日期
    dayState: 每日状态
    dailyTasks：日常任务
    mainTasks：主线任务
    months： 存储所有日记内容，以月为单位
    '''
    def __init__(self,no):
        '读档'
        import json
        with open('./data/'+no+'.json','r',encoding='UTF-8') as load_f:
            self.context = json.load(load_f)
        self.lv=self.context['lv']
        self.exp=self.context['exp']
        self.light=self.context['light']
        self.new=self.context['new']
        self.dayState=self.context['day']
        #print(self.dayState)
        self.dailyTasks=[]
        self.mainTasks=[]
        self.months={}
        self.cards={}
        self.nowEvents=[]
        self.oldEvents=[]
        self.ftrEvents=[]
        self.backpack=Backpack(self.context['backpack'])
        self.date=time.strftime("%y%m%d")
        
            
        for task in self.context['tasks']:
            if task["is_main"]:
                self.mainTasks.append(Task(task))
            else:
                self.dailyTasks.append(Task(task))
        
        with open('./event.json','r',encoding='UTF-8') as load_f:
            self.eventContext = json.load(load_f)
        
        for event in self.eventContext['events']:
            if event["end"]<self.date:
                self.oldEvents.append(Event(event))
            elif event["end"]>=self.date and event["start"]<=self.date:
                self.nowEvents.append(Event(event))
            else:
                self.ftrEvents.append(Event(event))
                #self.events[-1].show()
        for card in self.eventContext['cards']:
            self.cards[card['id']]=Card(card)
            #self.cards[card['id']].show()
            
    def gacha(self,num):
        gList=self.nowEvents[num].gacha
        ssrList=[]
        srList=[]
        rList=[]
        for gi in gList:
            g=self.cards[gi]
            if g.rarity == 'SSR':
                ssrList.append(g)
            elif g.rarity == 'SR':
                srList.append(g)
            elif g.rarity == 'R':
                rList.append(g)
        
        ossrList=[]
        osrList=[]
        orList=[]
        for event in self.oldEvents:
            gList=event.gacha
            if event.type=='常驻活动':
                for gi in gList:
                    g=self.cards[gi]
                    if g.rarity == 'SSR':
                        ossrList.append(g)
                    elif g.rarity == 'SR':
                        osrList.append(g)
                    elif g.rarity == 'R':
                        orList.append(g)   
                        
        if len(ssrList)==0:
            ssrList=ossrList
        if len(srList)==0:
            srList=osrList
        if len(rList)==0:
            rList=orList   
                        
        if len(ossrList)==0:
            ossrList=ssrList
            osrList=srList
            orList=rList
            
            
        rate4=0.03
        rate2=0.885
        rateu4=0.6666  #是up的概率
        rateu3=0.8588
        rateu2=0.8933
        
        if 'Fes' in self.nowEvents[num].type:
            rate4=0.06
            rate2=0.855
        
                
        luck=random.random()
        up=random.random()
        if luck>=1-rate4: #3% Fes6%
            if up>rateu4: #1.0002% Fes2.0004%
                i=random.randint(0,len(ssrList)-1)  
                item=ssrList[i]
            else: #1.9998% Fes3.9996%
                i=random.randint(0,len(ossrList)-1)  
                item=ossrList[i]
        elif luck>=rate2: #8.5%
            if up>rateu3: #1.2002%
                i=random.randint(0,len(srList)-1)
                item=srList[i]
            else: #7.2998%
                i=random.randint(0,len(osrList)-1)
                item=osrList[i]
        else: #88.5% Fes85.5%
            if up>rateu2: #9.44295% Fes9.12285%
                i=random.randint(0,len(rList)-1)
                item=rList[i]
            else: #79.05705% Fes76.37715%
                i=random.randint(0,len(orList)-1)
                item=orList[i]
                    
                
        return item
    
    def check(self,num,isNow):
        if isNow:
            gList=self.nowEvents[num].gacha
        else:
            gList=self.oldEvents[num].gacha
        allHave=True
        for gi in gList:
            g=self.cards[gi]
            if self.backpack.hasCard(g):
                pass
            else:
                allHave=False
                break
        return allHave
    
    def showBackpack(self):
        gList=self.backpack.cards
        num={'SSR':0,'SR':0,'R':0}
        tot=0
        for g in gList:
            print('-------------')
            self.cards[g['id']].show(False)
            print('数量：',g['num'])
            num[self.cards[g['id']].rarity]+=g['num']
            tot+=g['num']
            
        print('-------------')
        
        for key in num.keys():
            print(key,'数量：',num[key],'占比:','{:.3%}'.format(num[key]/tot))
        print('总数：',tot)
        
        print('-------------')
        
    def showEvent(self,num):
        gList=self.nowEvents[num].gacha
        print('-------------')
        self.nowEvents[num].show()
        for g in gList:
            print('-------------')
            self.cards[g].show()
        print('-------------')
        
    def showEvents(self):
        print('现在正在开展的任务有这些哟(＾Ｕ＾)ノ~ＹＯ')
        for i in range(len(self.nowEvents)):
            print('\nNo.',i)
            self.nowEvents[i].show()
                
    def showNowMainTasks(self):
        for i in range(len(self.mainTasks)):
            task=self.mainTasks[i]
            if task.finishTimes==0:
                print('\nNo.',i)
                task.show()
                
    def showFinMainTasks(self):
        for i in range(len(self.mainTasks)):
            task=self.mainTasks[i]
            if task.finishTimes!=0:
                print('\nNo.',i)
                task.show()      
    
    def addTask(self,isMain):
        '添加任务 TODO 改成传入参数，交互在start中'
        task={
           "interval_minites": "0",
           "type_id": 0,
           "comment": "",
           "update": False,
           "type": "",
           "is_main": isMain,
           "achievement": "",
           "exp": 10,
           "light": 100,
           "finishDate": "999999",
           "ddl": "999999",
           "progress": 0,
           "finishTimes": 0,
           "info": ""
          }
        task["type"]=input('是哪种任务呢？（do） -')
        if task["type"] is 'q':
            print('那再考虑一下吧，Ruby等着你哦！')
            return
        task["comment"]=input('唔，需要细化吗？（what） -')
        if task["comment"] is 'q':
            print('那再考虑一下吧，Ruby等着你哦！')
            return
        try:
            task["interval_minites"]=input('有时长要求吗？（0为无要求） -')
        except:
            print("告诉我数字啦！")
            return
        if task["interval_minites"] is 'q':
            print('那再考虑一下吧，Ruby等着你哦！')
            return
        task["achievement"]=input("成就称号是？ -")
        if task["achievement"] is 'q':
            print('那再考虑一下吧，Ruby等着你哦！')
            return
        task["info"]=input("告诉Ruby一些补充信息吧？ -")
        if task["info"] is 'q':
            print('那再考虑一下吧，Ruby等着你哦！')
            return
        try:
            task["exp"]=eval(input("设定奖励经验吧！ -"))
        except:
            print("告诉我数字啦！")
            return
        if task["exp"] is 'q':
            print('都讲到这了……都怪笨蛋小灰02010号没记录，又要重新讲一遍。')
            return
        try:
            task["light"]=eval(input("设定奖励光点吧！ -"))
        except:
            print("告诉我数字啦！")
            return
        if task["light"] is 'q':
            print('都讲到这了……都怪笨蛋小灰02010号没记录，又要重新讲一遍。')
            return
        task["ddl"]=input("任务的截止日期？（格式TTMMDD，999999为无日期） -")
        if task["ddl"] is 'q':
            print('都讲到这了……都怪笨蛋小灰02010号没记录，又要重新讲一遍。')
            return
        task=Task(task)
        print('Ruby正在努力规划任务……')
        task.show()
        cmd=input('这样可以么RubyRuby[y/n] -')
        if cmd is 'y':
            if isMain:
                self.mainTasks.append(task)
            else:
                self.dailyTasks.append(task)
            print('任务已生效！要努力完成哦，Ruby会监督你的（盯——')
        else:
            print('那再考虑一下吧，Ruby等着你哦！')
        
        
            
    def showDailyTasks(self):
        for i in range(len(self.dailyTasks)):
            task=self.dailyTasks[i]
            print('\nNo.',i)
            task.show()
            
                
    def save(self,no):
        '存档'
        import json
        
        tasks=[]
        for task in self.dailyTasks:
            tasks.append(task.updateTag())
        for task in self.mainTasks:
            tasks.append(task.updateTag())
            
        events=[]
        for event in self.nowEvents:
            events.append(event.updateTag())
        for event in self.oldEvents:
            events.append(event.updateTag())
        for event in self.ftrEvents:
            events.append(event.updateTag())
            
        data={
            "lv":self.lv,
            "exp":self.exp,
            "light":self.light,
            "new":self.new,
            "day":self.dayState,
            "tasks":tasks,
            "backpack":self.backpack.save()
            }
        with open('./data/'+no+".json","w",encoding='UTF-8') as dump_f:
            json.dump(data,dump_f,ensure_ascii=False,indent = 1)
            
        data={
            "events":events,
            "cards":self.eventContext['cards']
            }
        with open("./event.json","w",encoding='UTF-8') as dump_f:
            json.dump(data,dump_f,ensure_ascii=False,indent = 1)

                
    def add(self):
        '向系统中加入日记内容'
        '从数据读入一月的情况'
        #self.months[date]=DiaryMonth(date)
        import json
        with open("itime.db3.json",'r',encoding='UTF-8') as load_f:
            load_dict = json.load(load_f)
        for item in load_dict['itime.db3']['record']:
            if item['record_id']<=self.new:
                '该事件已更新过'
                item['update']=True
            else:
                item['update']=False
                self.new=item['record_id']
            date=item['year']+'-'+item['month']
            if date in self.months.keys():
                self.months[date].addThing(item)
            else:
                self.months[date]=DiaryMonth(date)
                self.months[date].dayState=self.dayState.get(date,{})
                self.months[date].addThing(item)
        
        '更新镜子系统'
        for date in self.months.keys():
            for day in self.months[date].days:
                '按一天为单位处理 获得该天的日期'
                isUpdate=False
                '''
                dateNow=date+day.date
                if dateNow<=self.new:
                    '该天已更新过'
                    continue
                #print(self.exp)
                self.new=dateNow
                '''
                '初始化每日任务'
                for task in self.dailyTasks:
                    task.finishDate='999999'
                    task.progress=0
                '花钱会扣light'
                self.light-=day.cost*100
                for thing in day.things.things:
                    '获得事物权重并更新exp与light  但如果事情没有更新不能更完后更新标签'
                    if thing.update:
                        continue
                    isUpdate=True
                    w=[0.998,9.98,'']
                    if thing.category !=None:
                        w=Thing.things[thing.category].get(thing.do,[0.999,9.99,''])
                    #w2=Thing.places.get(thing.at.split('-')[0],0.999) 
                    
                    dexp=thing.duration*w[-3]
                    dlight=thing.duration*w[-2]
                    
                    '''
                    if w[-2]<0 and thing.duration>15:
                        '附加惩罚'
                        dlight+=15*w[-2]
                    '''
                    #print(thing.tag,end=' ')
                    self.update(dexp,dlight)
                    
                    '更新任务'
                    dateStr=date.split('-')
                    if len(dateStr[1])==1:
                        dateStr[1]='0'+dateStr[1]
                    dateStr[0]=dateStr[0][2:]
                    if len(day.date)==1:
                        dateStr=dateStr[0]+dateStr[1]+'0'+day.date
                    else:
                        dateStr=dateStr[0]+dateStr[1]+day.date
                                           
                    for task in self.mainTasks:
                        if task.check(thing,dateStr):
                            self.exp+=task.exp
                            self.light+=task.light
                if isUpdate and day.things.totalTime<1440:
                    pause=input(day.date+'号这一天还没记录完哦！')
                    
                if isUpdate and day.things.totalTime==1440:
                    for thing in day.things.things:
                        for task in self.dailyTasks:
                            if task.check(thing,dateStr):
                                self.exp+=task.exp
                                self.light+=task.light
                    '升级处理'
                    if self.exp>=self.lv*(self.lv+4)*500:
                        self.lv+=1
                        print('升级了！现在是Level%d！'%self.lv)
                        self.update(0,self.lv*800)
                    self.show()
                    print('————'+date+'-'+day.date+' 已更新完毕————')
                    
                    if date in self.dayState.keys():
                        self.dayState[date][day.date]=[self.exp,self.light]
                    else:
                        self.dayState[date]={}
                        self.dayState[date][day.date]=[self.exp,self.light]
                    self.months[date].dayState[day.date]=[self.exp,self.light]
                
    def update(self,dexp,dlight):
        '''
        if dexp!=0:
            print('%+.2f exp '%dexp,end='')
        if dlight!=0:
            print('%+.2f light '%dlight,end='')
        print()
        '''
        self.exp+=dexp
        self.light+=dlight
        
    def show(self):
        print('Level:',self.lv)
        print('Exp:%.2f'%self.exp)
        print('Light:%.2f'%self.light)
        print('Uptate:',self.new)
