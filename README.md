# Prof.Rong-s_Simulation

## 目前我大概分为了三个模块

### 1. Seller.py

    class Seller():这个类是seller的类，也就是文章中的商家。
    
    Initilization函数中需要提供 item, customer的信息。其中item会用于初始化库存；customer信息会与item信息一同确定given S and customer_type $Z_t$, the probability of purchasing item i. (i.e., $\Phi_{i}^{Z_t}(S)$) 
    
    【NOTICE】这里第51行需要填写一个算法，即Reference【1】文章中的算法。
   
### 2. Generator.py
    
    class Generator():
    
    这个类用于产生顾客相关的信息；
    
    【NOTICE】其中第15行#TODO表示这个函数还未完成，需要填写。在生成customer时可以有多种方式。
    
    【NOTICE】第38行同理，需要完成；在做选择时，也可以有多种方式，甚至是故意选择使商家收益最差的。
    
    class Customer():
    
    这个类用于产生顾客实例，在申明后，仅在Generator中进行使用。
    
### 3. Instance.py

    class Instance():
    
    这个类就是模拟过程主要发生的场所了。 调用 Run_Single_Day() 函数将对一天的情况进行模拟。目前比较粗糙，仅记录了部分log，之后还会慢慢加上其他的函数，例如：画图。
    
## 输入参数

    输入参数主要考虑 item,customer
    
    item: 列表，其中每个元素是一个字典；这个列表中的商品是以 "价格降低" 进行排列
    
    customer: 列表，其中每个元素是一个字典；列表的index即为customer_type；preference表示这个类型的客户对所有商品的偏好，第一项0表示对不购买的偏好；注意，这个是preference，不是utility；所以如果用MNL的话，需要用exp()来计算
    
    
## Reference

     除了【1】之外，其他都是我最近读的paper。【4】也介绍了阿里目前是怎么做的，比较有借鉴意义
     
    【1】Golrezaei N, Nazerzadeh H, Rusmevichientong P. Real-time optimization of personalized assortments[J]. Management Science, 2014, 60(6): 1532-1551.
    
    【2】Davis J, Gallego G, Topaloglu H. Assortment planning under the multinomial logit model with totally unimodular constraint structures[J]. Work in Progress, 2013.
    
    【3】Rusmevichientong P, Shen Z J M, Shmoys D B. Dynamic assortment optimization with a multinomial logit choice model and capacity constraint[J]. Operations research, 2010, 58(6): 1666-1680.
    
    【4】Feldman J, Zhang D, Liu X, et al. Customer choice models versus machine learning: Finding optimal product displays on Alibaba[J]. Available at SSRN, 2019.
