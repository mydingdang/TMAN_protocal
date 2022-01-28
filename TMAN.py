""" Cloud Homework1 t-man 
    student: Yuqiu(Martin) Luo """

import numpy as np
import random 

class network():
    def __init__(self,N,k):
        self.N = N
        self.k = k
        self.node = self.initnodes()
        self.cach = {}

       
    def initnodes(self):
        node = []
        color = []
        for i in range(self.N):
            if i < self.N/3:
                j = [random.randint(200,255),random.randint(0,80),random.randint(0,80),"R"]
                color.append(j)
            elif i < self.N/2:
                j = [random.randint(0,80),random.randint(200,255),random.randint(0,80),"G"]
                color.append(j)
            else:
                j = [random.randint(0,80),random.randint(0,80),random.randint(200,255),"B"]
                color.append(j)
        random.shuffle(color)
        
        for i in range(self.N):
            theta = (np.pi/2-(i-1)*np.pi/(self.N-2))
            node.append([i+1,np.cos(theta),np.sin(theta),color.pop()])
        return node

    def cal_dis(self,s,t):
        s = s[3]
        t = t[3]
        sR,sG,sB = s[0],s[1],s[2]
        L_s,a_s,b_s = self.transform(sR,sG,sB)
        tR,tG,tB = t[0],t[1],t[2]  
        L_t,a_t,b_t = self.transform(tR,tG,tB) 
        dis = ((L_t-L_s)**2+(a_t-a_s)**2+(b_t-b_s)**2)**0.5
        return dis

    def transform(self,sR,sG,sB):
        var_R = sR/255
        var_G = sG/255
        var_B = sB/255

        if  var_R > 0.04045 :
            var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
        else :
            var_R = var_R / 12.92
        if  var_G > 0.04045 : 
            var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
        else :
            var_G = var_G / 12.92
        if var_B > 0.04045 : 
            var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
        else :
            var_B = var_B / 12.92

        var_R = var_R * 100
        var_G = var_G * 100
        var_B = var_B * 100
        X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
        Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
        Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505

        Reference_X = 94.811
        Reference_Y = 100.00
        Reference_Z = 107.304 

        var_X = X / Reference_X
        var_Y = Y / Reference_Y
        var_Z = Z / Reference_Z

        if  var_X > 0.008856 :
            var_X = var_X ** ( 1/3 )
        else :
            var_X = ( 7.787 * var_X ) + ( 16 / 116 )
        if  var_Y > 0.008856 :
            var_Y = var_Y ** ( 1/3 )
        else :
            var_Y = ( 7.787 * var_Y ) + ( 16 / 116 )
        if  var_Z > 0.008856 :
            var_Z = var_Z ** ( 1/3 )
        else :
            var_Z = ( 7.787 * var_Z ) + ( 16 / 116 )  
        
        CIE_l = ( 116 * var_Y ) - 16
        CIE_a = 500 * ( var_X - var_Y )
        CIE_b = 200 * ( var_Y - var_Z )
        return CIE_l, CIE_a, CIE_b
    
    def merge(self,s,arr1,arr2): 
        """use the merge sortig method"""
        result = []
        while arr1 and arr2:
            dis1 = self.cal_dis(s,arr1[0]) # calculate the distance between the base node and the node set elements
            dis2 = self.cal_dis(s,arr2[0])
            if dis1 < dis2:
                result.append(arr1.pop(0))
            else:
                result.append(arr2.pop(0))
        if arr1:
            result += arr1
        if arr2:
            result += arr2
        return result

    def merge_sort(self,s,views):
        """
        归并排序
        :param arr: 待排序的List
        :return: 排好序的List
        """
        v = np.shape(views)
        elements = v[0]
        if elements <= 1:
            return views
        mid = elements // 2
        return self.merge(s,self.merge_sort(s,views[:mid]), self.merge_sort(s,views[mid:]))
    
    def selectPeer(self,s,views=None):
        
        if s[0] in self.cach:
            
            views = []
            rand = np.random.randint(0,self.N,self.k)
            for i in rand:  
                views.append(self.node[i])   
        else :
            views = self.cach[s[0]]
        sort = self.merge_sort(s,views)
        self.cach[s[0]] = sort[:self.k]    
        return sort[0]

    # def selectView(self):
    #     a = [1,2,3]
    #     self.cach.append(a)



net = network(300,10)
node = net.node
# net.selectView()
print(net.cach)
cs = node[15]
print()
print(net.selectPeer(cs))



