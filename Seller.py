# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import itertools
import json
import math
from math import exp

def MNL(preference):
    #Input: List, OUtput: List
    score = [math.exp(k) for k in preference]
    total = sum(score)
    score = [k/total for k in score]
    return score

def Get_Inventory_Amend_Coefficient(item, function_type = None):
    
    if function_type == 'None':
        coef = 1
        return coef
        
    if function_type == 'linear':
        x = item['inventory']/item['adjusted_initial_inventory']
        coef = x
        return coef
    
    if function_type == 'exponential':
        x = item['inventory']/item['adjusted_initial_inventory']
        coef = exp(1)*(1-exp(-x))/(exp(1)-1)
        return coef
        
    if function_type == 'root':
        x = item['inventory']/item['adjusted_initial_inventory']
        coef = math.sqrt(x)
        return coef
    
    if function_type == 'piecewiselinear':
        coef = 1
        if item['inventory'] < 10:
            coef = item['inventory']/10
        return coef
    

class Seller():
    
    def __init__(self,item,customer, RANKING = False):
        
        #--- Seller.item[0]表示第0个商品 （不购买）
        self.item = {indiv['id']:indiv for indiv in item}
        
        #--- 可能提供的所有集合
        self.possible_offer_set = []
        
        #--- 找出每一个customer_type 在任意offer_set下的购买概率
        self.PROBABILITY = {}
        
        #--- customer
        self.customer = customer
        
        #--- replenishment
        self.replenishment_will_arrive = {}
        
        # RANKING = Ture，则认为相同产品，但排序不同的两个set是不同的
        if RANKING == False:
            for customer_type,indiv in enumerate(customer):
                preference = customer[customer_type]['preference']
                
                #当提供的商品集合为空时，顾客不做购买操作
                key = json.dumps({
                            'customer_type':customer_type,
                            'offered_set':list([])
                            })
                self.PROBABILITY[key] = {0:1}
                
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

        
    def Provide_Set(self,customer_type,IB_function_type,t):
        import numpy as np
        
        #Input: Int customer_type: 表示来的是第几类客户，编码从0开始
        #Output: List: 包含提供的商品ID（不包括0），例如 [1,2,4]表示提供1/2/4这三件商品
        provided_set = []
        #TODO
        
        #--- 构造prob_matrix：每一行为一个可能的offer set，每一列对应一个商品
        prob_matrix = np.zeros(shape=[len(self.possible_offer_set),len(self.item)])
        inventory_matrix = np.zeros(shape=[len(self.possible_offer_set),len(self.item)])
        for k,offer_set in enumerate(self.possible_offer_set):
            key = json.dumps({
                    'customer_type':customer_type,
                    'offered_set':offer_set}
                    )
            prob_purchase = self.PROBABILITY[key]
            for item_id in prob_purchase.keys():
                prob_matrix[k,item_id] = prob_purchase[item_id]
            
            #如果该assortment有任意一个商品库存小于等于0，则该assortment不再提供（该行向量为0，后面乘出来的revenue也都为0）
            if any([self.item[item_id]['inventory']<=0 for item_id in offer_set]):  
                inventory_matrix[k,:] = 0
            else:
                for item_id in prob_purchase.keys():
                    inventory_matrix[k,item_id] = 1
        
        
        #--- 将一维的revenue向量张成维度同prob_matrix的矩阵，每行的向量相同，为price
        revenue_matrix = np.tile([self.item[item_id]['price'] for item_id in self.item.keys()],  
                                  [len(self.possible_offer_set),1])
        
        
        #--- 为每个item计算库存调整量
        inventory_amend_vectore = np.asarray([ Get_Inventory_Amend_Coefficient(self.item[item_id],IB_function_type) 
                                                for item_id in self.item.keys()])
        inventory_amend_matrix = np.tile(inventory_amend_vectore,  [len(self.possible_offer_set),1])
        
        
        #--- 计算每行(即每个offer set)的收益
        revenue_per_set = np.sum(revenue_matrix*inventory_amend_matrix*prob_matrix*inventory_matrix,1)
        

        #--- 找出收益最大的possible set
        k = np.argmax(revenue_per_set)
        provided_set = self.possible_offer_set[k]
        
        return provided_set
    
    def Update_Inventory(self,customer_choice):
        #Input: Int customer_choice: 顾客选择购买的商品数
        self.item[customer_choice]['inventory'] -= 1
        
    def Calculate_Upper_bound(self,customer_sequence):
        #TODO check compatibility and correctness
        #Input: List customer_sequence: 每个元素是客户类对象
        #Output: 
        #通过解Paat Lemma1 中的LP得到Upper Bound
        from gurobipy import gurobipy as grb
        customer_sequence = [customer.type for customer in customer_sequence]
        
        #--- 申明问题
        primal_problem = grb.Model() 
        primal_problem.setParam('OutputFlag',0) 
        primal_problem.modelSense = grb.GRB.MAXIMIZE
        
        #--- 申明变量
        num_col = len(customer_sequence)
        num_row = int(len(self.possible_offer_set)/len(self.customer))
        
        Y = primal_problem.addVars(range(num_row),range(1,num_col+1), #行：set集合，index从0开始；  列：时间T，index从1开始
                                   vtype=grb.GRB.CONTINUOUS, lb=0,ub=1, 
                                   name='y')
        
        #--- 设置objective function
        obj = 0
        for t,customer_type in enumerate(customer_sequence):
            t = t+1  #时间变到正常的从1 开始 到 T
            for s,offer_set in enumerate(self.possible_offer_set[:num_row]):
                
                key = json.dumps({
                                'customer_type':customer_type,
                                'offered_set':offer_set
                                })
                item_prob = self.PROBABILITY[key]
                
                for item_id in offer_set: # 不在offer_set里面无收益
                    obj += item_prob[item_id]*self.item[item_id]['price']*Y[s,t]
        
        primal_problem.setObjective(obj)      
                    
                    
        #--- 加入constraints
        
        #capacity 限制
        for item_id in list(self.item.keys())[1:]:
            
            possible_buy_number = 0
            for t,customer_type in enumerate(customer_sequence):
                t = t+1 #时间变到正常的从1 开始 到 T
                
                for s,offer_set in enumerate(self.possible_offer_set[:num_row]):
                    
                    if item_id in offer_set:
                        key = json.dumps({
                                    'customer_type':customer_type,
                                    'offered_set':offer_set
                                    })
                        item_prob = self.PROBABILITY[key]
                        
                        possible_buy_number += item_prob[item_id]*Y[s,t]
            primal_problem.addConstr(possible_buy_number<=self.item[item_id]['initial_inventory']+self.item[item_id]['extra_inventory'])
            
        #possibility 约束
        for t in range(1,len(customer_sequence)+1): #1-->T
            possibility = grb.quicksum([Y[s,t] for s in range(len(self.possible_offer_set[:num_row]))])
            primal_problem.addConstr(possibility==1)
        
        primal_problem.write('11.lp')
        primal_problem.optimize()

        if primal_problem.status == grb.GRB.Status.OPTIMAL:
            print('successfully get hindsight upper bound')
            return primal_problem.ObjVal
        
        elif primal_problem.status == grb.GRB.Status.INFEASIBLE:
            print('upper bound model is infeasible.')
        
        else:
            print('something wrong with solving upper bound problem.')
            
    def Receive_Replenishment(self,t):
        if t >= 31:
            #print('收货量:',self.replenishment_will_arrive[t])
            for item_id in self.item.keys():
                
                if self.replenishment_will_arrive[t][item_id]>0:
                    
                    self.item[item_id]['inventory'] = self.item[item_id]['inventory'] + self.replenishment_will_arrive[t][item_id]
                    self.item[item_id]['extra_inventory'] = self.item[item_id]['extra_inventory'] + self.replenishment_will_arrive[t][item_id]   
                    self.item[item_id]['adjusted_initial_inventory'] = self.item[item_id]['inventory'] + self.replenishment_will_arrive[t][item_id]   
                    self.item[item_id]['inventory_in_transit'] = 0
                
                
    def Replenish_Products(self,t):
        #库存低到 THRESHOLD 以下后，便补货 REPLEVEL
        THRESHOLD = 10
        REPLEVEL = 20
        need_replenish = [REPLEVEL*(self.item[item_id]['inventory']+self.item[item_id]['inventory_in_transit']<=THRESHOLD) 
                         for item_id in self.item.keys()]
        
        #print('补货量:',need_replenish)
        #补货ETA后到
        ETA = 30
        self.replenishment_will_arrive[t+ETA] = need_replenish
        
        for item_id in self.item.keys():
            if need_replenish[item_id]>0:
                self.item[item_id]['inventory_in_transit'] = need_replenish[item_id]
                    
if __name__ == '__main__':
    
    ITEM = [{'id':0,'price':0,'inventory':9999999,'initial_inventory':9999999},
            {'id':1,'price':10,'inventory':5,'initial_inventory':5},
            {'id':2,'price':6,'inventory':10,'initial_inventory':10},
            {'id':3,'price':5,'inventory':10,'initial_inventory':10},
            {'id':4,'price':4,'inventory':10,'initial_inventory':10},
            {'id':5,'price':3,'inventory':10,'initial_inventory':10}]
    N_ITEM = len(ITEM)
    CUSTOMER = [{'preference': [0] + [1]*N_ITEM},
                {'preference': [0] + [3]*N_ITEM}]
    
    seller = Seller(ITEM,CUSTOMER)
    
    

