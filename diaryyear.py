# -*- coding: utf-8 -*-

from diarymonth import*

pyecharts.globals._WarningControl.ShowWarning = False


class DiaryYear:
    '''
    年终总结用
    '''
    def __init__(self,year,months):
        self.year=year
        self.months=(months)
        self.num=12
        
    def findLastSleep(self):
        '找哪天睡得最晚，起的最早'
        sleep_time = datetime.datetime.strptime('00:00','%H:%M')
        sleep_date = 0
        wake_time = datetime.datetime.strptime('12:00','%H:%M')
        wake_date = 0
        for i in range(12):
            for j in range(self.months[i].num):
                day=self.months[i].days[j]             
                for k in range(day.things.num):
                    thing=day.things.things[k]
                    if thing.do=='睡觉':
                        if thing.start_time>sleep_time:
                            sleep_time=thing.start_time
                            sleep_date=self.months[i].date+'-'+day.date
                        if thing.end_time<wake_time:# and thing.end_time!=datetime.datetime.strptime('05:41','%H:%M'):
                            sleep_again=False
                            for l in range(1,5):
                                if  k+l<day.things.num:
                                    if day.things.things[k+l].do=='睡觉' and day.things.things[k+l].start_time<datetime.datetime.strptime('09:00','%H:%M'):
                                        sleep_again=True

                            if not sleep_again:
                                wake_time=thing.end_time
                                wake_date=self.months[i].date+'-'+day.date
                            
                        break
        # 如果是00：00，说明一年没有熬夜到零点
        print('今年睡得最晚的一天是',sleep_date)
        print('熬夜到了',sleep_time.time())
        print('今年起得最早的一天是',wake_date)
        print('时间是',wake_time.time())#8.75h
        print('****************')
                        
        
    def findMost(self,tag,color='#04B45F'):
        '找哪天哪一类最多'
        '预习，游戏，电影，运动'
        all_time=[]

        for i in range(12):
            for j in range(self.months[i].num):
                day=self.months[i].days[j]
                all_time.append([self.months[i].date+'-'+day.date,day.things.doTime.get(tag,0)])
                
        all_sorted=sorted(all_time,key=lambda x:-x[1])
                    
        
        print('今年',tag,'最多的一天是',all_sorted[0][0])
        print('做了',round(all_sorted[0][1]/60,2),'小时')
        print('日期       时长（分钟）')
        for i in range(3):
            print(all_sorted[i][0],all_sorted[i][1])
        print('****************')
        
        
        
        
        
        begin = datetime.date(eval(self.year), 1, 1)
        end = datetime.date(eval(self.year), 12, 31)

        
        c=(
            Calendar(init_opts=opts.InitOpts(height="300px"))
            .add(
                series_name="",
                yaxis_data=all_time,
                calendar_opts=opts.CalendarOpts(
                    #pos_top="50px",
                    range_=str(self.year),
                    yearlabel_opts=opts.CalendarYearLabelOpts(is_show=False),
                    daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
                    monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn")
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts( pos_left="left", title=tag+" 标签热力 (min)"),
                visualmap_opts=opts.VisualMapOpts(
                    max_=all_sorted[0][1], min_=0, 
                    orient="horizontal", 
                    is_piecewise=False,
                    #pos_top="100px",
                    pos_left="center",
                    range_color=["#F8F8F8", color]
                ),
            )
        )
        return c
        
        
        
    def findBest(self,preState,color='#5F04B4'):
        '找exp最高的10天'
        
        exp=[preState[0]]
        all_exp=[]
        for i in range(12):
            for j in range(self.months[i].num):
                state=self.months[i].dayState[str(j+1)]
                exp.append(state[0])       
                all_exp.append([self.months[i].date+'-'+str(j+1),state[0]-exp[-2]])
        
                
        all_sorted=sorted(all_exp,key=lambda x:-x[1])
                    
        
        print('今年','exp','最多的一天是',all_sorted[0][0])
        print('为',round(all_sorted[0][1],2))
        print('日期       exp')
        for i in range(3):
            print(all_sorted[i][0],all_sorted[i][1])
        print('****************')
        
        print('今年','exp','最少的一天是',all_sorted[-1][0])
        print('为',round(all_sorted[-1][1],2))
        print('日期       exp')
        for i in range(3):
            print(all_sorted[-1-i][0],all_sorted[-1-i][1])
        print('****************')
        
        
        begin = datetime.date(eval(self.year), 1, 1)
        end = datetime.date(eval(self.year), 12, 31)

        
        c=(
            Calendar(init_opts=opts.InitOpts(height="300px"))
            .add(
                series_name="",
                yaxis_data=all_exp,
                calendar_opts=opts.CalendarOpts(
                    #pos_top="50px",
                    range_=str(self.year),
                    yearlabel_opts=opts.CalendarYearLabelOpts(is_show=False),
                    daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
                    monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn")
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts( pos_left="left", title="经验热力"),
                visualmap_opts=opts.VisualMapOpts(
                    max_=all_sorted[0][1], min_=0, 
                    orient="horizontal", 
                    is_piecewise=False,
                    #pos_top="100px",
                    pos_left="center",
                    range_color=["#F8F8F8", color]
                ),
            )
        )
        return c
        
    def drawTagsTime(self,tags):
        '某小类的月分布'
        categories={}
        date=[]

        for i in range(12):
            tTime=self.months[i].calSumTagTime()
            for info in tTime:
                if info in tags:
                    category= categories.get(info,[0]*self.num)
                    category[i]=round(tTime[info]/60,2)
                    categories[info]=category
            date.append(self.months[i].date[5:7]+'月')
            

        c = (
            Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(date)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="标签时长"),
                tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                yaxis_opts=opts.AxisOpts(
                    axislabel_opts=opts.LabelOpts(formatter="{value} h"),
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
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
            c.add_yaxis(info, categories[info], stack="stack1", areastyle_opts=opts.AreaStyleOpts(opacity=0.5)).set_series_opts(
                label_opts=opts.LabelOpts(
                    is_show=False
                )
            )
        return c
        
        
    def drawState(self,preState,show=True):
        '绘制一年的经验与light情况'
        exp=[preState[0]]
        dexp=[0]
        light=[preState[1]]
        dlight=[0]
        date=[]
        for i in range(12):
            num=self.months[i].num
            state=self.months[i].dayState[str(num)]
            exp.append(state[0])
            light.append(state[1])
            date.append(self.months[i].date[5:7]+'月')
            dexp.append(state[0]-exp[-2])
            dlight.append(state[1]-light[-2])   


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
                title_opts=opts.TitleOpts(title="经验状况"),
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
                title_opts=opts.TitleOpts(title="光点状况"),
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
        
        
    def drawDoTimeDo(self):
        '绘制一年的所做小类事词云'
        categories={}
        for i in range(12):
            doTime=self.months[i].calSumTagTime()
            for info in doTime:
                category= categories.get(info,0)
                category=category+(doTime[info])
                categories[info]=category
        data=[]
        for info in categories:
            if info != '睡觉':
                data.append((info,str(round(categories[info]/60,2))))

        c = (
            WordCloud()
            .add(series_name="事务", data_pair=data, word_size_range=[15, 150])
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="标签云", title_textstyle_opts=opts.TextStyleOpts(font_size=23)
                ),
                tooltip_opts=opts.TooltipOpts(is_show=True),
            )
        )
        return c
        

    def drawTimeDo(self,show=True):
        '绘制一年的所做事时长，按月分，折线图'
        categories={}
        date=[]

        for i in range(12):
            cTime=self.months[i].calSumCategorieTime()
            for info in cTime:
                category= categories.get(info,[0]*self.num)
                category[i]=round(cTime[info]/60,2)
                categories[info]=category
            date.append(self.months[i].date[5:7]+'月')
            

        c = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis(date)
            .set_global_opts(
                title_opts=opts.TitleOpts(title="事务时长"),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} h")),
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
                        "function(x){return Number(x.data/24/30 * 100).toFixed() + '%';}"
                    ),
                )
            )
        return c

    def drawTimeDoPie(self,show=True):
        '绘制各类事情总时间占比，返回时间大类饼图'
        categories={}
        
        for i in range(12):
            cTime=self.months[i].calSumCategorieTime()
            for info in cTime:
                category= categories.get(info,[0]*self.num)
                category[i]=(cTime[info])
                categories[info]=category


        dataSorted=sorted(categories.items(),key=lambda x:-sum(x[1]))
        X=[]
        Y=[]
        for p in dataSorted:
            Y.append(round(sum(p[1])/60,2))
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
                title_opts=opts.TitleOpts(title="总时长 (h)"),
                )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
                # label_opts=opts.LabelOpts(formatter="{b}: {c}")
            ) 
        )
        return p
    

    def report(self,preState):
        
        for i in range(12):
            for j in range(self.months[i].num):
                day=self.months[i].days[j]
                
                for k in range(day.things.num):
                    day.things.things[k].start_time=datetime.datetime.strptime(day.things.things[k].start_time,'%H:%M')
                    if day.things.things[k].end_time!= '24:00':
                        day.things.things[k].end_time=datetime.datetime.strptime(day.things.things[k].end_time,'%H:%M')
                    else:
                        day.things.things[k].end_time=datetime.datetime.strptime('23:59:59','%H:%M:%S')
                self.months[i].days[j].things.things=sorted(day.things.things,key=lambda x:x.start_time)
                
        
        page = Page(layout=Page.SimplePageLayout)
        state=self.drawState(preState,False)
        print('****************'),
        page.add(
            state[0],
            state[1],
            self.findBest(preState),
            self.drawTimeDo(),
            #self.drawTagsTime(['运动','洗澡']),
            self.drawTagsTime(['游戏','音游']),
            self.drawTagsTime(['影视','看番','漫画']),
            self.drawTagsTime(['学习','论文','读书','讲座']),
            #self.drawTagsTime(['日语','英语']), 只在7月5.2h
            self.drawTagsTime(['唱歌','听歌']),
            
            self.findMost('运动'),
            self.findMost('游戏',"#00FF7F"),
            self.findMost('音游',"#00BFFF"),
            self.findMost('影视',"#ADD8E6"),
            self.findMost('看番',"#B0E0E6"),
            self.findMost('预习',"#32CD32"),
            self.drawTimeDoPie(),
            self.drawDoTimeDo()
        )
        page.render(self.year+" 报告"+".html")
        self.findLastSleep()

     
