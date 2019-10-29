# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 22:42:31 2019

@author: chend
"""
import json
import random
from numpy.random import choice 

class Generator():
    
    def __init__(self,customer):
        
        self.potential_customer = customer
        
    def Generate_Customer_Type(self,gene_mode = 'uniform'):
        #Copyright: Songsong Chen (GitHub: song95326)
        total_type = len(self.potential_customer)
        
        #--- 以一种随机的方式生成customer的type
        if gene_mode == 'uniform':            #--- 均匀分布
            customer_type = random.randint(0,total_type-1)
            
        elif gene_mode == 'normal' :                   #--- 正态分布
            random_mean = random.uniform(1,total_type) 
            CV = 1.0
            customer_type = round(random.normalvariate(random_mean,(CV*random_mean)**2)) 

        elif gene_mode == 'betaMax&Min':                   #---Beta分布 （极端值概率大）
            customer_type = round(random.betavariate(0.5,0.5)*10)

        else:                                  #---Beta分布 （小值概率大）
            customer_type = round(random.betavariate(1,3)*10)   
        return customer_type
        
        return customer_type
    
    def Generate_Customer(self,mode = 'uniform'):
        
        customer_type = self.Generate_Customer_Type(mode)
        customer = Customer(self.potential_customer,customer_type)
        
        return customer
    
    
class Customer():
    
    def __init__(self,potential_customer,customer_type):
        
        self.type = customer_type
        self.preference = potential_customer[customer_type]['preference'] #preference 不是 utility
        
    def Choose_Product(self,provided_set, seller, choose_mode='utility'):
        #Copyright: Songsong Chen (GitHub: song95326)

        #Input: List provided_set: 提供的商品集合，不包括0；例如provided_set = [1,2,4]
        #Output: Int customer_choice: 选择了哪个商品
        
        key = json.dumps({
                            'customer_type':self.type,
                            'offered_set':provided_set
                            })
        prob = seller.PROBABILITY[key]
        
        
        if choose_mode == 'utility':
            #按计算的utility表格进行选择
            customer_choice = choice(list(prob.keys()),p=list(prob.values()))
            
            
        if choose_mode == 'uniform':
            #uniformly选择一个物品
            index = random.randint(0,len(provided_set)-1)
            customer_choice = provided_set[index]
            
            
        if choose_mode == 'min_prob':
            #选择该客户最小可能购买的商品
            customer_choice = min(prob,key=prob.get) #选出概率最小值对应的key，也就是item_id
        
        if  choose_mode == 'max_prob':                   #--- 选preference最小
            customer_choice = max(prob,key=prob.get)
                
        if  choose_mode == 'minInventory':     #--- 选库存最小
            inv = 9999999
            index = 0
            for i in provided_set:
                if 0 < seller.item[i]['inventory'] < inv :
                    inv = seller.item[i]['inventory']
                    index = i
            customer_choice = index
            
        return customer_choice
    
    
if __name__ == '__main__':
    
    ITEM = [{'id':1,'price':10,'inventory':5},
            {'id':2,'price':6,'inventory':10},
            {'id':3,'price':5,'inventory':10},
            {'id':4,'price':4,'inventory':10},
            {'id':5,'price':3,'inventory':10}]
    N_ITEM = len(ITEM)
    CUSTOMER = [{'preference': [0] + [1]*N_ITEM},
                {'preference': [0] + [3]*N_ITEM}]
    
    generator = Generator(CUSTOMER)
    
    
        