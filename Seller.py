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
        
        #--- 可能提供的所有集合
        self.possible_offer_set = []
        
        #--- 找出每一个customer_type 在任意offer_set下的购买概率
        self.PROBABILITY = {}
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
                        
                        self.PROBABILITY[key] = probability 
                        
                        #记录下所有可能由商家提供的集合
                        self.possible_offer_set.append(list(offered_set))
        
    def Provide_Set(self,customer_type):
        #Input: Int customer_type: 表示来的是第几类客户，编码从0开始
        #Output: List: 包含提供的商品ID（不包括0），例如 [1,2,4]表示提供1/2/4这三件商品
        provided_set = []
        #TODO
        
        return provided_set
    
    def Update_Inventory(self,customer_choice):
        #Input: Int customer_choice: 顾客选择购买的商品数
        self.item[customer_choice]['inventory'] -= 1
        
            
    def Calculate_Upper_bound(self,customer_sequence):
        #TODO check compatibility and correctness
        #Input: List customer_sequence: 每个元素表明客户类型，从0编码
        #Output: 
        #通过解Paat Lemma1 中的LP得到Upper Bound
        from gurobipy import gurobipy as grb
        
        #--- 申明问题
        primal_problem = grb.Model() 
        primal_problem.setParam('OutputFlag',0) 
        primal_problem.modelSense = grb.GRB.MAXIMIZE
        
        #--- 申明变量
        num_col = len(self.possible_offer_set)
        num_row = len(customer_sequence)
        Y = primal_problem.addVars(range(num_row),range(1,num_col+1), #行为set集合，index从0开始；列为时间T，index从1开始
                                   vtype=grb.GRB.CONTINUOUS, lb=0,up=1, 
                                   name='y')
        
        #--- 设置objective function
        obj = 0
        for t,customer_type in enumerate(len(customer_sequence)):
            t = t+1  #时间变到正常的从1 开始 到 T
            for s,offer_set in enumerate(self.possible_offer_set):
                
                key = json.dumps({
                                'customer_type':customer_type,
                                'offered_set':offer_set
                                })
                item_prob = self.PROBABILITY[key]
                
                for item_id in offer_set: # 不在offer_set里面无收益
                    obj += item_prob[item_id]*self.item[item_id]['price']*Y[s,t]
                    
                    
                    
        #--- 加入constraints
        
        #capacity 限制
        for item_id in list(self.item.keys())[1:]:
            
            possible_buy_number = 0
            for t,customer_type in enumerate(len(customer_sequence)):
                t = t+1 #时间变到正常的从1 开始 到 T
                
                for s,offer_set in enumerate(self.possible_offer_set):
                    
                    if item_id in offer_set:
                        key = json.dumps({
                                    'customer_type':customer_type,
                                    'offered_set':offer_set
                                    })
                        item_prob = self.PROBABILITY[key]
                        
                        possible_buy_number += item_prob[item_id]*Y[s,t]
            primal_problem.addConstr(possible_buy_number<=self.item[item_id]['initial_inventory'])
            
        #possibility 约束
        for t in range(1,len(customer_sequence)+1): #1-->T
            possibility = grb.quicksum([Y[s,t] for s in range(self.possible_offer_set)])
            primal_problem.addConstr(possibility==1)
            
        
        primal_problem.solve()
        
        if primal_problem.status == grb.GRB.Status.OPTIMAL:
            return primal_problem.ObjVal
        
        else:   
            print('something wrong with solving upper bound problem.')
            
            
if __name__ == '__main__':
    
    ITEM = [{'id':1,'price':10,'inventory':5,'initial_inventory':5},
            {'id':2,'price':6,'inventory':10,'initial_inventory':10},
            {'id':3,'price':5,'inventory':10,'initial_inventory':10},
            {'id':4,'price':4,'inventory':10,'initial_inventory':10},
            {'id':5,'price':3,'inventory':10,'initial_inventory':10}]
    N_ITEM = len(ITEM)
    CUSTOMER = [{'preference': [0] + [1]*N_ITEM},
                {'preference': [0] + [3]*N_ITEM}]
    
    seller = Seller(ITEM,CUSTOMER)
    
    

