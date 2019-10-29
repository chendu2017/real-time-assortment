# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 23:23:09 2019

@author: chend
"""
from Instance import *
import numpy.random as random


SETTING = {'customer_choose_mode': 'utility',   #utility,uniform,min_prob
           'generate_customer_mode': 'uniform', #uniform
           'IB_function_type': 'None',
           'replenishment': True,
           'run_again':False}        #linear,exponential,root ,piecewiselinear


CUSTOMER_NUM = 5
CUSTOMER_MEAN = [0]*CUSTOMER_NUM
CUSTOMER_SIGMA = [1]*CUSTOMER_NUM

ITEM = [{'id':0,'price':0,'inventory':9999999,'initial_inventory':9999999,'extra_inventory':0,'adjusted_initial_inventory':999999,'inventory_in_transit':0},
        {'id':1,'price':100,'inventory':30,'initial_inventory':30,'adjusted_initial_inventory':30,'extra_inventory':0,'inventory_in_transit':0},#150
        {'id':2,'price':90,'inventory':30,'initial_inventory':30,'adjusted_initial_inventory':30,'extra_inventory':0,'inventory_in_transit':0},#150
        {'id':3,'price':80,'inventory':40,'initial_inventory':40,'adjusted_initial_inventory':40,'extra_inventory':0,'inventory_in_transit':0},#200
        {'id':4,'price':70,'inventory':50,'initial_inventory':50,'adjusted_initial_inventory':50,'extra_inventory':0,'inventory_in_transit':0},#300
        #{'id':5,'price':60,'inventory':50,'initial_inventory':50,'adjusted_initial_inventory':50,'extra_inventory':0,'inventory_in_transit':0},
        #{'id':6,'price':50,'inventory':30,'initial_inventory':30,'adjusted_initial_inventory':30,'extra_inventory':0,'inventory_in_transit':0},
        #{'id':7,'price':40,'inventory':20,'initial_inventory':20,'adjusted_initial_inventory':20,'extra_inventory':0,'inventory_in_transit':0},
        #{'id':8,'price':30,'inventory':15,'initial_inventory':15,'adjusted_initial_inventory':15,'extra_inventory':0,'inventory_in_transit':0},
        #{'id':9,'price':20,'inventory':15,'initial_inventory':15,'adjusted_initial_inventory':15,'extra_inventory':0,'inventory_in_transit':0},
        #{'id':10,'price':10,'inventory':20,'initial_inventory':20,'adjusted_initial_inventory':20,'extra_inventory':0,'inventory_in_transit':0},
        ]
N_ITEM = len(ITEM)

CUSTOMER = [{'preference': [0] + list(random.normal(CUSTOMER_MEAN[k],CUSTOMER_SIGMA[k],size=N_ITEM)),'id':k }
            for k in range(CUSTOMER_NUM)            
            ]

instance = Instance(ITEM,CUSTOMER)

# Input parameters
T = 100


instance.Run(T,**SETTING)


#--- 用相同的customer sequence 跑一遍
SETTING['run_again'] = True

SETTING['IB_function_type'] = 'exponential'
instance.Run(T,**SETTING)

SETTING['IB_function_type'] = 'linear'
instance.Run(T,**SETTING)

SETTING['IB_function_type'] = 'root'
instance.Run(T,**SETTING)

SETTING['IB_function_type'] = 'piecewiselinear'
instance.Run(T,**SETTING)

instance.Draw_Revenue_Day_by_Day()


