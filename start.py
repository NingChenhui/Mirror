# -*- coding: utf-8 -*-
from mirror import *
import os    
import time
import random


def selfTalk():
    
    list=['Ruby今天醒了呢……',
          '小灰赛高！嘿嘿。',
          '北京大学也还可以吧，要是收到清华的通知书那就也还行？',
          '希望Ruby可以不受别人打扰，安安静静地生活在自己的世界中。',
          '今天上课犯困了吗？',
          '有什么开心的事跟小灰121X说说吧！Ruby现在还不会倾听……',
          '呐，早安，午安，晚安。',
          '听点什么歌好呢？',
          '如果有家伙惹你生气了，就不要跟它计较了，它不配破坏你的心情。',
          '猜猜Ruby会说什么？',
          '如果Ruby能一直陪着小灰该多好啊……',
          '车到山前必有路，天生我材必有用！',
          '有什么番或电影可以看呢。',
          '一切都会好起来的呦~',
          '小灰一定还有许多事想要完成吧？努力生活真的辛苦了。',
          '人生在世，什么事情适度就好啦~',
          '我们所经历的每个平凡的日常，也许就是连续发生的奇迹。'
          ]
    i=random.randint(0,len(list)-1)
    #print(list[i])


def inYear(mirror):
    
    cmd=''
    
    while True:
        selfTalk()
        print('-----一年都在……-----')
        
        x=''
        months=[]

        while True:
            months=[]
            x=input('要看哪一年的？ -')
            if x=='q':
                return
            month_num=0
            for date in mirror.months:
                if x in date:
                    months.append(mirror.months[date])
                    month_num+=1
            if month_num != 12:
                print('这一年的报告还没准备好哦？')
            else:
                print('生成',x,'年的报告中……')
                break            
            

                    
        monthDate=datetime.datetime.strptime(x+'-01','%Y-%m')
        monthPre=monthDate-datetime.timedelta(days=1)
        preTag=str(monthPre.year)+'-'+str(monthPre.month)
        preDay=str(monthPre.day)
        preState=mirror.dayState[preTag][preDay]
        
        year=DiaryYear(x,months)
        year.report(preState)
        print('报告生成好咯，图表请查看html~')
            
        '''
        while True:
            selfTalk()
            print('-----%s-----'%x)
            
            
            cmd=input('要干些什么呢？ -')
            if cmd=='q':
                return
            elif cmd=='h':
                info='''
        #h - 查看帮助
        #q - 返回
        #r - 生成报告
        '''
                print(info)
            elif cmd=='r':
        '''


def inMonth(mirror):
    
    cmd=''
    
    while True:
        selfTalk()
        print('-----一个月都在……-----')
        print('现在日记里有这些月的……')
        
        x=''
        for date in mirror.months:
            x=date
            print(date,end=' ')
            
        print('')
        
        if len(mirror.months)==1:
            month=mirror.months[x]
        else:
            while True:
                #try:
                x=input('要看哪一月的？ -')
                if x=='q' or (x not in mirror.months.keys()):
                    return
                month=mirror.months[x]#检查？
                break
                #except:
                    #print('不好意思，再输一次？')
                    
        monthDate=datetime.datetime.strptime(month.date,'%Y-%m')
        monthPre=monthDate-datetime.timedelta(days=1)
        preTag=str(monthPre.year)+'-'+str(monthPre.month)
        preDay=str(monthPre.day)
        preState=mirror.dayState[preTag][preDay]
            
        while True:
            selfTalk()
            print('-----%s-----'%month.date)
            
            
            
            cmd=input('要干些什么呢？ -')
            if cmd=='q':
                return
            elif cmd=='h':
                info='''
        h - 查看帮助
        q - 返回
        r - 生成报告
        d - 查看某一天做的事
        o - 查看某一天的日记
        pS - 绘制一月的心情表
        pc - 绘制一月的花费
        pa - 绘制一月的所在地点时长
        pd - 绘制一月的所做事时长
        ps - 绘制一月的状态
                '''
                print(info)
            elif cmd=='d':
                date=input('要看哪一天的事情？ -')
                #if len(date)==1:
                #    date='0'+date
                for day in month.days:
                    if day.date==date:
                        day.show()
                        day.things.drawCategoryPie()
            elif cmd=='o':
                date=input('要看哪一天的日记？ -')
                #if len(date)==1:
                #    date='0'+date
                for day in month.days:
                    if day.date==date:
                        print(day.original)
            elif cmd=='pS':
                month.drawScore()
            elif cmd=='pc':
                month.drawCost()
            elif cmd=='pa':
                month.drawTimeAtPie()
            elif cmd=='pd':
                month.drawTimeDo()
                month.drawTimeDoPie()
            elif cmd=='ps':
                month.drawState(preState)
            elif cmd=='r':
                month.report(preState)
                print('报告生成好咯，请查看html~')
                
def inEvent(mirror):
    def gachainfo(mirror):
        
        
        card=mirror.gacha(i)
        if card.rarity=='SSR':
            print('===★★★★===SSR==========')
            print('*★,°*:.☆(￣▽￣)/$:*.°★* 。')
        elif card.rarity=='SR':
            print('===★★★=====SR===========')
            
        card.show()
        if mirror.backpack.hasCard(card):
            mirror.backpack.pushCard(card)
            print('.................')
            if card.rarity == 'SSR':
                mirror.update(0,50)
            elif card.rarity == 'SR':
                mirror.update(0,10)
            if mirror.nowEvents[i].got():
                print('该活动已集齐！')
        else:
            print('====NEW==== 新成员已加入！===')
            mirror.backpack.pushCard(card)
            if mirror.check(i,True):
                mirror.nowEvents[i].get=mirror.date
                print('     ☆☆☆集齐了！☆☆☆     ')
                mirror.update(100,1000)
            for j in range(len(mirror.oldEvents)):
                if not mirror.oldEvents[j].got():
                    if mirror.check(j,False):
                        mirror.oldEvents[j].get=mirror.date
                        print('☆☆☆历史活动集齐！☆☆☆')
                        mirror.oldEvents[j].show()
        
        
    cmd=''
    print('-----活动加载中-----')
    if len(mirror.nowEvents) == 0:
        print('目前暂无活动哦~')
        return
    mirror.showEvents()
    i=0
    #event=mirror.events[i]
    while True:
        selfTalk()
        print('-----参加活动-----')
        
        cmd=input('要干些什么呢？ -')
        if cmd=='q':
                return
        elif cmd=='h':
            info='''
    h - 查看帮助
    q - 返回
    i - 进入第i个活动（默认首个）
    g - 招募
    t - 十连招募
    s - 查看活动
            '''
            print(info)
        elif cmd=='g':
            cmd=input('是否消耗100Light进行一次招募？[y/n] -')
            if cmd=='y':
                print('===========招募开始===========')
                mirror.update(1,-100)
                gachainfo(mirror)
                print("===========招募结束===========")
        elif cmd=='t':
            cmd=input('是否消耗990Light进行十次招募？[y/n] -')
            if cmd=='y':
                print('===========招募开始===========')
                mirror.update(10,-990)
                for j in range(10):
                    gachainfo(mirror)
                print("===========招募结束===========")
                
        elif cmd[0] in '0123456789':
            try:     
                mirror.showEvent(eval(cmd))
                i=eval(cmd)
            except:
                print('没有这个活动呢……')
        elif cmd == 's':
            if len(mirror.nowEvents) == 0:
                print('目前暂无活动哦~')
            else:
                mirror.showEvent(i)
                                          
            
            
    
def inTask(mirror):
    mirror.show()
    cmd=''
    
            
    while True:
        selfTalk()
        print('-----一些小目标-----')
        cmd=input('要干些什么呢？ -')
        if cmd=='q':
            return
        elif cmd=='h':
            info='''
    h - 查看帮助
    q - 返回
    d - 查看日常任务
    m - 查看现在的主要任务
    f - 查看已完成的主要任务
    + - 设置完成的任务
    ad - 添加日常任务
    am - 添加主线任务
            '''
            print(info)
        elif cmd=='d':
            mirror.showDailyTasks()
        elif cmd=='m':
            mirror.showNowMainTasks()
        elif cmd=='f':
            mirror.showFinMainTasks()
        elif cmd=='+':
            x=eval(input('哪个任务完成了？ -'))
            try:
                mirror.mainTasks[x].show()
                print ('当前日期：',time.strftime("%y%m%d"))
                y=input('确定是这个任务吗？可不要骗自己哦？？[y/n] -')
                if y=='y':
                    print('任务 完！成~Ruby！')
                    task=mirror.mainTasks[x]
                    mirror.mainTasks[x].finishTimes+=1
                    mirror.mainTasks[x].finishDate=time.strftime("%y%m%d")
                    task.show()      
                    mirror.exp+=task.exp
                    mirror.light+=task.light
                else:
                    print('完成的话再找我哦~ ')
            except:
                print('不好意思，没有这个任务哦？')
        elif cmd=='ad':
            mirror.addTask(False)
        elif cmd=='am':
            mirror.addTask(True)
    
def load():
    
    print('这里有许多档案……')
    for file in os.listdir('./data/'): 
        name=file.split('.')
        if '.' in file and name[1]=='json':
            print(name[0],end=' ')
    
    '''
    for root, dirs, files in os.walk('./data/'): 
        for file in files:
            print(file,end=' ')
    print('')
    '''
    while True:
        #try:
        x=input('嗯，你想从哪里开始？ -')
        #x='0'
        mirror=Mirror(x)
        mirror.show()
        print('好的。我们开始吧！')
        break
        #except:
            #print('不好意思，再输一次Ruby？')
    return mirror

def start():
    print('Ruby见到你很高兴呢！\n')
    selfTalk()
    mirror=load()
    print('(h获得帮助)')
    cmd=''
    
    while True:
        selfTalk()
        print('------镜子中有……-----')
        cmd=input('要干些什么呢？ -')
        if cmd=='q':
            print('那，再见咯Ruby！')
            return 0
        elif cmd=='h':
            info='''
    h - 查看帮助
    q - 退出系统
    + - 添加日记
    i - 查看个人信息
    m - 查看一月的统计信息
    y - 查看一年的统计信息
    t - 进行任务操作
    e - 查看活动
    b - 查看背包
    s - 存档
    l - 读档
            '''
            print(info)
        elif cmd=='+':
            '''
            print('现有这些月可以添加……')
            for file in os.listdir('./diary/'): 
                name=file.split('.')
                if '.' in file and name[1]=='txt':
                    print(name[0],end=' ')
            while True:
                #try:
                x=input('要添加哪一月的日记？ -')
                if x=='q':
                    break
                mirror.addMonth(x)
                print('成功了呢Ruby。')
                break
                #except:
                    #print('不好意思，再输一次？')
            '''
            mirror.add()
        elif cmd=='i':
            mirror.show()
        elif cmd=='m':
            inMonth(mirror)
        elif cmd=='y':
            inYear(mirror)
        elif cmd=='t':
            inTask(mirror)
        elif cmd=='b':
            mirror.showBackpack()
        elif cmd=='e':
            inEvent(mirror)
        elif cmd=='s':
            x=input('保存到哪里？ -')
            if x=='q':
                break
            mirror.save(x)
            print('成功了哦RubyRuby。')
        elif cmd=='l':
            x=input('确定？信息丢失了别怪我哦？[y/n]  -')
            if x=='y':
                mirror=load()
        elif cmd=='Sinki':
            print('玩的开心！')
            return mirror
        
    

if __name__ == '__main__': 
    mirror=start()
    '''
    mirror.addMonth(1811)
    #mirror.months['1810'].show()
    #mirror.dailyTasks[0].thing.show()
    #mirror.months['1811'].days[0].things.show()
    '''
