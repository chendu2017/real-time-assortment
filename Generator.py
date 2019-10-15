# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 22:42:31 2019

@author: chend
"""

class Generator():
    
    def __init__(self,customer):
        
        self.potential_customer = customer
        
    def Generate_Customer_Type(self):
        #TODO
        #--- 以一种随机的方式生成customer的type
        customer_type = 0
        
        
        return customer_type
    
    def Generate_Customer(self):
        
        customer_type = self.Generate_Customer_Type()
        customer = Customer(self.potential_customer,customer_type)
        
        return customer
    
    
class Customer():
    
    def __init__(self,potential_customer,customer_type):
        
        self.type = customer_type
        self.preference = potential_customer[customer_type]['preference'] #preference 不是 utility
        
    def Choose_Product(self,provided_set):
        #TODO
        
        #Input: List provided_set: 提供的商品集合，不包括0；例如provided_set = [1,2,4]
        #Output: Int customer_choice: 选择了哪个商品
        customer_choice = 0
        
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
    
    
        