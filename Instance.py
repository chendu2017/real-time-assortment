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
        customer = self.generator.Generate_Customer()
        #卖家提供商品集合
        provided_set = self.seller.Provide_Set(customer.type)
        #客户做出购买选择
        customer_choice = customer.Choose_Product(provided_set)
        #卖家更新库存、计算收益等
        self.seller.Update_Inventory(customer_choice)
        self.revenue += self.item[customer_choice]['price']
        self.customer_sequence.append(customer.type)
        
        self.log['Day{}'.format(t)] = {'customer_type':customer.type,
                                       'provided_set':provided_set,
                                       'customer_choice':customer_choice,
                                       'inventory': [it['inventory'] for it in self.item]
                                       }
    
    
if __name__ == '__main__':
    
    ITEM = [{'id':1,'price':10,'inventory':5},
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
    
    
    
    