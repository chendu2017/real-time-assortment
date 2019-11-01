# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 22:22:35 2019

@author: chend
"""
from Seller import *
from Generator import *
import time
import numpy as np
import matplotlib.pyplot as plt
font = {'family' : 'simhei',
        'weight' : 'bold',
        'size'   : 40}
plt.rc('font', **font)

plt.rc('xtick', labelsize=40)    # fontsize of the tick labels
plt.rc('ytick', labelsize=40)    # fontsize of the tick labels

class Instance():
    
    def __init__(self,item,customer):
        
        self.item = item
        self.customer = customer
        self.seller = Seller(item,customer)
        self.customer_sequence = []
        self.generator = Generator(customer)
        self.revenue = {}
        #self.revenue_upper_bound = {}
        #只需要获取最后一天的upper_bound
        self.revenue_upper_bound=0
        
        self.time_length = 0
        self.IB_function_type = ''
        self.IB_function_type_sequence = []
        self.customer_choose_mode = ''
        
        self.log = {}

    #不需要每天计算（record_ratio_to_upper_bound在后续程序中并未调用）    
    def Record_Ratio_to_Upper_bound(self):
        #卖家计算hindsight的收益上限,并记录到Instance中
        self.revenue_upper_bound = self.seller.Calculate_Upper_bound(self.customer_sequence)
    
    def Run(self,time_length,**setting):
        
        self.IB_function_type = setting['IB_function_type']
        self.IB_function_type_sequence.append(setting['IB_function_type'])
        self.customer_choose_mode = setting['customer_choose_mode']        
        self.time_length = time_length
        self.revenue['{}'.format(self.IB_function_type)] = 0
        self.log['IB{}'.format(self.IB_function_type)] = {}
        
        if setting['run_again'] == True:
            #复原库存信息
            for item_id in self.seller.item.keys():
                self.seller.item[item_id]['inventory'] = self.seller.item[item_id]['initial_inventory']
                self.seller.item[item_id]['adjusted_initial_inventory'] = self.seller.item[item_id]['initial_inventory']
                self.seller.item[item_id]['extra_inventory'] = 0
                self.seller.item[item_id]['inventory_in_transit'] = 0
        
        #调用Run函数，进行模拟
        for t in range(1,1+time_length):
            
            print('t = {}   ing...'.format(t))
            
            if setting['replenishment'] == True:
                #seller接受之前的订货,并计算 adjusted_initial_inventory_level
                self.seller.Receive_Replenishment(t)
            
            if setting['run_again'] == False:
                #生成一个新客户
                customer = self.generator.Generate_Customer(mode = setting['generate_customer_mode'])
                self.customer_sequence.append(customer)
            else:
                customer = self.customer_sequence[t-1]
                
            #卖家提供商品集合
            provided_set = self.seller.Provide_Set(customer.type, IB_function_type = setting['IB_function_type'],t=t)
            #客户做出购买选择
            customer_choice = customer.Choose_Product(provided_set,self.seller,
                                                      choose_mode=setting['customer_choose_mode'])
            #卖家更新库存、计算收益等
            self.seller.Update_Inventory(customer_choice)
            self.revenue['{}'.format(self.IB_function_type)] += self.item[customer_choice]['price'] 
            
            if setting['replenishment'] == True:
                #查看是否需要补货，并订货
                self.seller.Replenish_Products(t) 
            #只在最后一天计算upper_bound
            if t==time_length:
                #商家的收益
                self.revenue_upper_bound= self.seller.Calculate_Upper_bound(self.customer_sequence)
                
            
            
            #日志
            self.log['IB{}'.format(self.IB_function_type)]['Day{}'.format(t)] = {'customer_type':customer.type,
                                                                               'provided_set':provided_set,
                                                                               'customer_choice':customer_choice,
                                                                               'inventory': [it['inventory'] for it in self.item],
                                                                               'revenue_today':self.item[customer_choice]['price']
                                                                               }
        print('{}天模拟结束\n'.format(time_length))

        
    def Draw_Revenue_Day_by_Day(self):
        
        last_day = len(self.customer_sequence)
        
        #画图
        figure_setting = {'markersize':5,
                          'linewidth':5,
                          }
        
        fig = plt.figure(figsize=(20,10))
        ax = fig.subplots()
        plt.xlabel(r'$t$')
        plt.ylabel('Revenue')
        plt.title('Seller\'s revenue and the upper bound')
        
        #upper bound
        lst=[self.revenue_upper_bound]*last_day
        upper_line_x,upper_line_y = range(last_day),lst
        ax.plot(upper_line_x,upper_line_y , #upper_bound收益，是一条与x轴平行的直线
                label='Upper_Bound',marker='D',**figure_setting)
        ax.text(x= round(len(self.log)*0,1),y=round(self.revenue_upper_bound*0.9)-5,
                    s = 'hindsight收益：{}'.format(round(self.revenue_upper_bound],2)))
        
        
        #计算画图用的数据
        for IB_function_type in self.IB_function_type_sequence:
            log = self.log['IB{}'.format(IB_function_type)]
            
            revenue_accumulated = np.cumsum([log['Day{}'.format(t)]['revenue_today'] 
                                        for t in range(1,1+last_day)])
        
            seller_line_x,seller_line_y = range(last_day),revenue_accumulated

            ax.plot(seller_line_x, seller_line_y,  #卖家的收益图
                    label='{}:{}%'.format(IB_function_type,
                          round(seller_line_y[-1]/self.revenue_upper_bound*100,3)), 
                           marker='o',**figure_setting)
            
        ax.legend()
        
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
        instance.Run(t)
    
    
    
    
