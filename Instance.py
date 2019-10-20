# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 22:22:35 2019

@author: chend
"""
from Seller import *
from Generator import *

class Instance():
    
    def __init__(self,item,customer):
        
        self.item = item
        self.customer = customer
        self.seller = Seller(item,customer)
        self.customer_sequence = []
        self.generator = Generator(customer)
        self.revenue = 0
        
        self.log = {}
        
    
    def Run_Single_Day(self,t):
        #生成一个新客户
        func_type = 1                             #---生成方式
        customer = self.generator.Generate_Customer(func_type))
        #卖家提供商品集合
        provided_set = self.seller.Provide_Set(customer.type)
        #客户做出购买选择
        choose_type = 1                               #--- 选择方式
        customer_choice = customer.Choose_Product(provided_set,self.seller,choose_type)
        #卖家更新库存、计算收益等
        self.seller.Update_Inventory(customer_choice)
        self.revenue += self.item[customer_choice]['price']
        self.customer_sequence.append(customer.type)
        
        self.log['Day{}'.format(t)] = {'customer_type':customer.type,
                                       'provided_set':provided_set,
                                       'customer_choice':customer_choice,
                                       'inventory': [it['inventory'] for it in self.item],
                                       'revenue_today':customer_choice*self.item[customer_choice]['price']
                                       }
        
        
    def Record_Ratio_to_Upper_bound(self):
        #卖家计算hindsight的收益上限,并记录到Instance中
        self.revenue_upper_bound = self.seller.Calculate_Upper_bound(self.customer_sequence)
    
    
    def Run(self,time_length):
        #调用Run函数，进行模拟
        for t in range(1,1+time_length):
            self.Run_Single_Day(t)  
            
            
    def Draw_Revenue_Day_by_Day(self):
        import numpy as np
        import matplotlib.pyplot as plt
        
        #计算画图用的数据
        revenue_accumulated = np.cumsum([self.log['Day{}'.format(t)]['revenue_today'] for t in range(1,1+len(self.customer_sequence))])
        
        #画图
        figure_setting = {'markersize':20,
                          'linewidth':5,
                          }
        
        fig = plt.figure(figsize=(20,10))
        ax = fig.subplots()
        plt.xlabel(r'$t$')
        plt.ylabel('Revenue')
        plt.title('Seller\'s revenue and the upper bound')
        
        ax.plot(x = revenue_accumulated, y = range(len(self.customer_sequence)),  #卖家的收益图
                label='Paat', marker='o',**figure_setting)
        ax.plot(x = [self.revenue_upper_bound]*len(self.customer_sequence),y = range(len(self.customer_sequence)), #upper_bound收益，是一条与x轴平行的直线
                label='Upper_Bound',marker='D',**figure_setting)
    
    
if __name__ == '__main__':
    
    ITEM = [{'id':0,'price':0,'inventory':9999999,'initial_inventory':9999999},
            {'id':1,'price':10,'inventory':5},
            {'id':2,'price':6,'inventory':10},
            {'id':3,'price':5,'inventory':10},
            {'id':4,'price':4,'inventory':10},
            {'id':5,'price':3,'inventory':10}]
    N_ITEM = len(ITEM)
    CUSTOMER = [{'preference': [0] + [1]*N_ITEM},
                {'preference': [0] + [3]*N_ITEM}]
    
    instance = Instance(ITEM,CUSTOMER)
    
    # Input parameters
    T = 10
    
    for t in range(1,T+1):
        instance.Run_Single_Day(t)
    
    
    
    
