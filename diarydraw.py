# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from pylab import mpl  
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['font.sans-serif']=['SimHei'] #显示中文标签
plt.rcParams['axes.unicode_minus']=False


def drawBar(data,xname,xlabel,ylabel,title):
    '''根据传入的字典按绘条形图和
    字典样例：
    {
     'a':3, 
     'b':4,
    }
    '''
    plt.ion()
    plt.figure(figsize=(10,8))
    X=range(len(xname))
    for Y in data:
        plt.bar(X,data[Y],label=Y)
        for a,b in zip(X,data[Y]):
            plt.text(a, b+0.05, '%.1f' % b, ha='center', va= 'bottom',fontsize=10)
        
        sumY=sum(data[Y])
        ave=sumY/len(data[Y])
        plt.plot(X,[ave]*len(data[Y]),label='Ave',color='chocolate')

    plt.xticks(X,xname, rotation=45)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.ioff()
    plt.show()

def drawBarh(data,xname,xlabel,ylabel,title):
    '''根据传入的字典按大小排序绘排行榜-横条图
    字典样例：
    {
     'a':3, 
     'b':4,
    }
    '''
    plt.ion()
    sortedData=sorted(data.items(),key=lambda x:x[1])
    Y=[]
    X=[]
    for p in sortedData:
        X.append(p[0])
        Y.append(p[1])
    x=range(len(X))

    plt.figure(figsize=(10,8))
    plt.barh(x,Y,label=xname)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.yticks(x,X,rotation=45)
    plt.title(title)
    for a,b in zip(x,Y):
        plt.text(b+0.15, a, '%.0f' % b, ha='center', va= 'bottom',fontsize=10)
    plt.ioff()
    plt.show()
    
def drawPie(data,title):
    '''根据传入的字典按大小排序绘饼状图
    TODO Pie传入的数据需要更改。不需要date因此调用该函数的代码也要改
    字典样例：
    {
     'a':[1,2,3,], 
     'b':[1,2,3,],
    }
    求列表和的饼图
    '''
    plt.ion()
    dataSorted=sorted(data.items(),key=lambda x:-sum(x[1]))
    X=[]
    Y=[]
    for p in dataSorted:
        Y.append(sum(p[1]))
        X.append(p[0])
    #plt.figure(figsize=(6,9)) #调节图形大小
    #colors = ['red','yellowgreen','lightskyblue','yellow'] #每块颜色定义
    #explode = (0,0,0,0) #将某一块分割出来，值越大分割出的间隙越大

    plt.figure(figsize=(10,8))
    plt.pie(Y,
          #explode=explode,
          labels=X,
          #colors=colors,
          autopct = '%3.2f%%', #数值保留固定小数位
          shadow = False, #无阴影设置
          startangle =0, #逆时针起始角度设置
          rotatelabels=True,
          pctdistance=0.9,#数值距圆心半径倍数距离
          #wedgeprops = {'linewidth': 23},
          ) 
    #patches饼图的返回值，texts1饼图外label的文本，texts2饼图内部的文本
    # x，y轴刻度设置一致，保证饼图为圆形
    plt.axis('equal')
    plt.legend(labels=X, loc='best')
    plt.tight_layout()
    plt.title(title)
    plt.ioff()
    plt.show()

def drawPlot(data,xname,xlabel,ylabel,title):
    '''
    参数：数据，x周变量名，x标签，y标签，图标题
    根据传入的字典和x轴标签在一个图中画多条折线
    字典样例：
    {
     'a':[1,2,3], 
     'b':[1,3,2],
    }
    '''
    plt.ion()
    plt.figure(figsize=(10,8))
    X=range(len(xname))
    for Y in data:
        plt.plot(X,data[Y],label=Y)
        if len(data)==1:
            for a,b in zip(X,data[Y]):
                plt.text(a, b+0.05, '%.0f' % b, ha='center', va= 'bottom',fontsize=10)
    
    if title=='本月心情走势':
        plt.ylim(0,100)
        
    plt.xticks(X,xname, rotation=45)
    plt.legend()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.ioff()
    plt.show()
    
