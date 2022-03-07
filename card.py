# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 22:08:11 2020

@author: Sinki
"""
import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np



class Card:
    '''
    卡片
    '''
    
    def __init__(self,card):
        '''
        根据card生成新的对象
        	{
        		"id": 1,
        		"name": "初心",
        		"rarity": "SSR",
        		"info": "请多指教！",
        		"fig": "",
        		"skill": "",
        	}
        '''
        self.card=card
        self.id=card['id']
        self.name=card['name']
        self.rarity=card['rarity']
        self.info=card['info']
        self.fig=card['fig']
        self.skill=card['skill']
        
    def show(self,fig=True):
        print('卡名：',self.name)
        print('稀有度：',self.rarity)
        print(self.info)
        if fig:
            if self.fig != "":
                lena = mpimg.imread('events/'+self.fig+'.png') 
                # 此时 lena 就已经是一个 np.array    
                plt.imshow(lena) # 显示图片
                plt.axis('off') # 不显示坐标轴
                plt.show()
            