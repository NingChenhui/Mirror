# -*- coding: utf-8 -*-
from diaryday import*
from diarydraw import*
#import datetime
import calendar

import pyecharts
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Pie,Grid, Page, WordCloud, Calendar
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from pyecharts.commons.utils import JsCode

pyecharts.globals._WarningControl.ShowWarning = False

def getContext(x):
    '获得日记内容'
    context=[]
    with open('./diary/'+x+'.txt','r',encoding='UTF-8') as f:
        context=f.readlines()
    return context

class DiaryMonth:
    '''
    储存一月所有属性的类
    days：   所有天
    num：    总数
    date:    日期
    tasks:   本月完成的任务 （TODO）
    '''
    def __init__(self,date):
        self.days=[]
        self.date=date
        date=datetime.datetime.strptime(date,'%Y-%m')
        self.num=calendar.monthrange(date.year,date.month)[1]
        #self.date=date
        for i in range(self.num):
            self.days.append(DiaryDay(date+datetime.timedelta(days=i)))
        self.dayState={}
        
        self.tasks=[]
        
        '''
        context=getContext(date)
        print('%读取日记完毕')
        day=DiaryDay('·0 0 晴 others -1')
        for i in range(1,len(context)):
            '去除两端空格 空行跳过'
            context[i]=context[i].strip()
            if len(context[i])==0:
                continue
            '开头为· 即为新的一天'
            if context[i][0]=='·':
                self.add(day)
                #day.show()
                #t=0
                #for k in day.timeAt:
                #    t+=day.timeAt[k]
                day=DiaryDay(context[i])
                continue
            day.analyse(context[i],i)
            
        '处理最后一天'
        self.add(day)
        print('%日信息处理完毕')
        '''
        
    def addThing(self,record):
        '添加事件'
        '''
        if day.date=='00':
            return
        self.num+=1
        self.days.append(day)
        '''
        
        for i in range(self.num):
            if self.days[i].date==record['day']:
                self.days[i].addThing(record)
        
    def drawState(self,preState,show=True):
        '绘制一月的经验与light情况'
        exp=[preState[0]]
        dexp=[0]
        light=[preState[1]]
        dlight=[0]
        date=[]
        weekchar=['','一','二','三','四','五','六','日']
        for day in self.days:
            state=self.dayState.get(day.date,[0,0])
            exp.append(state[0])
            light.append(state[1])
            date.append(day.date+','+weekchar[eval(day.weekdate)])
            dexp.append(state[0]-exp[-2])
            dlight.append(state[1]-light[-2])
            if dexp[-1]<0:
                dexp.pop()
                dlight.pop()
                exp.pop()
                light.pop()
                date.pop()
                break
            
        print('月增长：')
        print('Exp:',round(exp[-1]-exp[0],2))
        print('Light:',round(light[-1]-light[0],3))
        print('pt:',round(((exp[-1]-exp[0])*1000+(light[-1]-light[0])*10)/self.num))

        if show:
            drawPlot({'Exp':exp[1:],'Delta':dexp[1:]},date,'Date','Exp','本月经验状况')
            drawPlot({'Light':light[1:],'Delta':dlight[1:]},date,'Date','Light','本月光点状况')


        bar1 = (
            Bar()
            .add_xaxis(date)
            .add_yaxis("Delta", dexp[1:])
            .extend_axis(
                yaxis=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} Exp"),
                    name='Exp',
                    is_scale=True,
                )
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=self.date+" 经验状况"),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} Exp"),name='Delta',is_scale=True),
                datazoom_opts=[opts.DataZoomOpts(range_start=0,range_end=100), opts.DataZoomOpts(type_="inside")],
            )
        )

        line = Line().add_xaxis(date).add_yaxis("Exp", exp[1:], yaxis_index=1).set_series_opts(
            label_opts=opts.LabelOpts(is_show=False)
            )
        bar1.overlap(line)

        bar2 = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(date)
            .add_yaxis("Delta", dlight[1:])
            .extend_axis(
                yaxis=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} Light"),
                    name='Light',
                    is_scale=True
                )
            )
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
                title_opts=opts.TitleOpts(title=self.date+" 光点状况"),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} Light"),name='Delta',is_scale=True),
                datazoom_opts=[opts.DataZoomOpts(range_start=0,range_end=100), opts.DataZoomOpts(type_="inside")],
            )
        )

        line = (
            Line().add_xaxis(date).add_yaxis("Light", light[1:], yaxis_index=1)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        )
        bar2.overlap(line)
        return [bar1,bar2]
        
        
    def drawScore(self):
        '绘制一月的心情表'
        score=[]
        date=[]
        for day in self.days:
            score.append(day.score)
            date.append(day.date+','+day.weekdate)
        drawPlot({'Feeling':score},date,'Date','Score','本月心情走势')
        
    def drawCost(self):
        '绘制一月的花费'
        cost=[]
        date=[]
        for day in self.days:
            cost.append(day.cost)
            date.append(day.date+','+day.weekdate)
        sumCost=sum(cost)
        print('总消费 %.2f'%sumCost,'日均消费 %.2f'%(sumCost/len(cost)))
        drawBar({'Money':cost},date,'Date','Cost','每日消费额')
        

    def drawTimeAtPie(self):
        '绘制各所在地点总时间占比'
        '''
        places={}
        num=0
        for day in self.days:
            for info in day.timeAt:
                place=places.get(info,[0]*self.num)
                place[num]=(day.timeAt[info])
                places[info]=place
            num+=1
        drawPie(places,'各所在地点总时间占比')
        '''
    def drawDoTimeDo(self,show=True):
        '绘制一月的所做小类事词云'
        categories={}
        for day in self.days:
            for info in day.things.doTime:
                category= categories.get(info,0)
                category=category+(day.things.doTime[info])
                categories[info]=category
        data=[]
        for info in categories:
            if info != '睡觉':
                data.append((info,str(categories[info])))
        #print(data)
        c = (
            WordCloud()
            .add(series_name="事务", data_pair=data, word_size_range=[15, 150])
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title=self.date+" 词云", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
        )
        return c
        

    def drawTimeDo(self,show=True):
        '绘制一月的所做事时长，按天分，折线图' #TODO:改成小时
        categories={}
        date=[]
        num=0
        weekchar=['','一','二','三','四','五','六','日']
        for day in self.days:
            for info in day.things.time:
                category= categories.get(info,[0]*self.num)
                category[num]=(day.things.time[info])
                categories[info]=category
            date.append(day.date+','+weekchar[eval(day.weekdate)])
            num+=1
        if show:
            drawPlot(categories,date,'Date','TimeDo(min)','各事物每天时长')

        c = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(date)
            .set_global_opts(
                title_opts=opts.TitleOpts(title=self.date+" 事务时长"),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} min")),
                datazoom_opts=[opts.DataZoomOpts(range_start=0,range_end=100), opts.DataZoomOpts(type_="inside")],
                toolbox_opts=opts.ToolboxOpts(is_show=True,
	             pos_top="top",
	             pos_left="right",
	             feature={"saveAsImage": {} ,
	                "restore": {} ,
	                "magicType":{"show": True, "type":["line","bar","tiled","stack"]},
	                "dataView": {} })

            )
        )
        for info in categories:
            c.add_yaxis(info, categories[info], stack="stack1", category_gap="50%").set_series_opts(
                label_opts=opts.LabelOpts(
                    position="inside",
                    formatter=JsCode(
                        "function(x){return Number(x.data/1440 * 100).toFixed() + '%';}"
                    ),
                )
            )
        return c

    def drawTimeDoPie(self,show=True):
        '绘制各所事情总时间占比，返回时间大类饼图' #TODO:改成日均小时
        places={}
        num=0
        for day in self.days:
            for info in day.things.time:
                place=places.get(info,[0]*self.num)
                place[num]=(day.things.time[info])
                places[info]=place
            num+=1
        if show:
            drawPie(places,'各所事物总时间占比')

        dataSorted=sorted(places.items(),key=lambda x:-sum(x[1]))
        X=[]
        Y=[]
        for p in dataSorted:
            Y.append(sum(p[1]))
            X.append(p[0])
        p=(
            Pie()
            .add(
                series_name="时间",
                data_pair=[list(z) for z in zip(X, Y)],
                radius=["50%", "70%"],
                label_opts=opts.LabelOpts(is_show=True, position="inside"),
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(pos_right="5%", orient="horizontal"),
                title_opts=opts.TitleOpts(title=self.date+" 总时长"),
                )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
                # label_opts=opts.LabelOpts(formatter="{b}: {c}")
            ) 
        )
        return p
    
    def calSumTagTime(self):
        categories={}
        for day in self.days:
            for info in day.things.doTime:
                category= categories.get(info,0)
                category=category+(day.things.doTime[info])
                categories[info]=category
        return categories
    
    def calSumCategorieTime(self):
        categories={}
        for day in self.days:
            for info in day.things.time:
                category= categories.get(info,0)
                category=category+(day.things.time[info])
                categories[info]=category
        return categories

    def report(self,preState):
        page = Page(layout=Page.SimplePageLayout)
        state=self.drawState(preState,False)
        page.add(
            state[0],
            state[1],
            self.drawTimeDo(False),
            self.drawTimeDoPie(False),
            self.drawDoTimeDo()
        )
        page.render(self.date+" 报告"+".html")

    def show(self):
        self.drawScore()
        self.drawCost()
        self.drawTimeAtPie()
        self.drawTimeDo()
        self.drawTimeDoPie()
        pass        
