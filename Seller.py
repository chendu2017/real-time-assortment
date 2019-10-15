# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import itertools
import json
import math

def MNL(preference):
    #Input: List, OUtput: List
    score = [math.exp(k) for k in preference]
    total = sum(score)
    score = [k/total for k in score]
    return score
    

class Seller():
    
    def __init__(self,item,customer, RANKING = False):
        
        #--- 按价格从高到低排序后，给到seller; Seller.item[0]表示第0个商品 （不购买）
        item = [{'id':0,'price':0,'inventory':9999999}] + item
        self.item = {indiv['id']:indiv for indiv in item}
        
        #--- 找出每一个customer_type 在任意offer_set下的购买概率
        Seller.PROBABILITY = {}
        # RANKING = Ture，则认为相同产品，但排序不同的两个set是不同的
        if RANKING == False:
            for customer_type,indiv in enumerate(customer):
                preference = customer[customer_type]['preference']
                for n in range(1, len(self.item.keys())): # from 1 to N 
                    for offered_set in itertools.combinations(list(self.item.keys())[1:],n):
                        key = json.dumps({
                                'customer_type':customer_type,
                                'offered_set':list(offered_set)
                                })
                        offered_set_plus_no = [0] + list(offered_set)
                        preference_offered_set = [preference[item_id] for item_id in offered_set_plus_no]
                        
                        probability = MNL(preference_offered_set)
                        probability = {item_id:probability[k] for k,item_id in enumerate(offered_set_plus_no)}
                        
                        Seller.PROBABILITY[key] = probability 
        
    def Provide_Set(self,customer_type):
        #Input: Int customer_type: 表示来的是第几类客户，编码从0开始
        #Output: List: 包含提供的商品ID（不包括0），例如 [1,2,4]表示提供1/2/4这三件商品
        provided_set = []
        #TODO
        
        return provided_set
    
    def Update_Inventory(self,customer_choice):
        #Input: Int customer_choice: 顾客选择购买的商品数
        self.item[customer_choice]['inventory'] -= 1
        

if __name__ == '__main__':
    
    ITEM = [{'id':1,'price':10,'inventory':5},
            {'id':2,'price':6,'inventory':10},
            {'id':3,'price':5,'inventory':10},
            {'id':4,'price':4,'inventory':10},
            {'id':5,'price':3,'inventory':10}]
    N_ITEM = len(ITEM)
    CUSTOMER = [{'preference': [0] + [1]*N_ITEM},
                {'preference': [0] + [3]*N_ITEM}]
    
    seller = Seller(ITEM,CUSTOMER)
    
    

