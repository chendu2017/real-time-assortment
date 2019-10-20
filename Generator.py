# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 22:42:31 2019

@author: chend
"""
import numpy as np
import random
import json
class Generator():
    
    def __init__(self,customer):
        
        self.potential_customer = customer
        
    def Generate_Customer_Type(self,funcType): #--- funcType 调用不同的生成方法
        #TODO
        #--- 以一种随机的方式生成customer的type
        if funcType == 'uniform':                     #--- 均匀分布
           customer_type = random.randint(1,10) 

        elif funcType == 'normal' :                   #--- 正态分布
            random_mean = random.uniform(1,10) 
            CV = 1.0
            customer_type = round(random.normalvariate(random_mean,(CV*random_mean)**2)) 

        elif funcType == 'betaMax&Min':                   #---Beta分布 （极端值概率大）
            customer_type = round(random.betavariate(0.5,0.5)*10)

        else:                                  #---Beta分布 （小值概率大）
            customer_type = round(random.betavariate(1,3)*10)   
        return customer_type
    
    def Generate_Customer(self,funcType):
        
        customer_type = self.Generate_Customer_Type(funcType)
        customer = Customer(self.potential_customer,customer_type)
        
        return customer
    
    
class Customer():
    
    def __init__(self,potential_customer,customer_type):
        
        self.type = customer_type
        self.preference = potential_customer[customer_type]['preference'] #preference 不是 utility
        
    def Choose_Product(self,provided_set,seller,chooseType):
        #TODO
        #Input: List provided_set: 提供的商品集合，不包括0；例如provided_set = [1,2,4]
        key = json.dumps({
            'customer_type':self.type,
            'offered_set':provided_set
        })

        PROBABILITY = seller.PROBABILITY[key]


        #Output: Int customer_choice: 选择了哪个商品
        if  chooseType == "inProbability":                     #--- 按概率大小选择
            choice_list = list(PROBABILITY.keys())
            probability = list(PROBABILITY.values())
        
            customer_choice = np.random.choice(choice_list,probability)
             
        elif  chooseType == 'maxPreference':                   #--- 选preference最大
            customer_choice = max(PROBABILITY,key=PROBABILITY.get)

        elif  chooseType == 'minPreference':                   #--- 选preference最小
            customer_choice = min(PROBABILITY,key=PROBABILITY.get)

        elif  chooseType == 'minInventory':                    #--- 选库存最小
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
    
    
        