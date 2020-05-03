# -*- coding: utf-8 -*-
"""
Created on Sat May  2 12:15:49 2020

@author: User
"""
#import errno
import matplotlib.pyplot as plt
#import pynmea2
#import math
import numpy as np
#import re
import sys
#import pymap3d as pm

def Read_TGD(SVtype,system):
    x=[-1]
    y=[-1]
    for i in range(0,len(SVtype)):
        if(SVtype[i]==system and x[len(x)-1]!=SVprn[i]  ):  
            x.append(SVprn[i])
            y.append(SV_TGD[i]*(3*10**8))
    x.remove(-1)
    y.remove(-1)           
    
    return x,y        
            
if __name__=='__main__': 
    file_name='brdm0240.20p'
    #file_name='brdm3280.19p'
    
    #file_name='brdm0840.20p'
    #file_name=sys.argv[1]
    
    #file_name = input('Input file:')
    '''      
    try :
        textfile = open(file_name, 'r')
        textfile.close()
        print("file is readable")
    except FileNotFoundError:
        print("No such file or directory")
    '''    

    file_name = sys.argv[1]         
            
    input_file = open(file_name, 'r')

    SVtype=[]
    SVprn=[]
    SV_YYYY=[]
    SV_MM=[]
    SV_DD=[]
    SV_HH=[]
    SV_mm=[]
    SV_TGD=[]
    idx = 0
    
    Gx_TGD=[]
    Gy_TGD=[]
    Cx_TGD=[]
    Cy_TGD=[]    
    Ex_TGD=[]
    Ey_TGD=[]
    Jx_TGD=[]
    Jy_TGD=[]    
    Ix_TGD=[]
    Iy_TGD=[] 
    for line in input_file:
        Data = line.split(' ')
        idx=idx+1
        if(line[0:3]!='   ' and line[3]==' ' ):
            if(line[0]=='G' or line[0]=='E' or line[0]=='C' or line[0]=='J' or line[0]=='I'):
                idx=100
                SVtype.append(line[0])
                SVprn.append(int(line[1:3]))
                SV_YYYY.append(int(Data[1]))
                SV_MM.append(int(Data[2]))
                SV_DD.append(int(Data[3]))
                SV_HH.append(int(Data[4]))
                SV_mm.append(int(Data[5]))


        if(idx==106):
            SV_TGD.append(float(line[42:61]))

    
    
    
    Gx_TGD,Gy_TGD=Read_TGD(SVtype,'G')
    Ex_TGD,Ey_TGD=Read_TGD(SVtype,'E')
    Cx_TGD,Cy_TGD=Read_TGD(SVtype,'C')
    Jx_TGD,Jy_TGD=Read_TGD(SVtype,'J')
    Ix_TGD,Iy_TGD=Read_TGD(SVtype,'I')
    
    
    plt.figure(figsize=(10,5))
    plt.plot(Gx_TGD,Gy_TGD, 'r-o', label='GPS')
    plt.plot(Cx_TGD,Cy_TGD, 'b-o', label='BDS')    
    plt.plot(Ex_TGD,Ey_TGD, 'y-o', label='GAL')    
    plt.plot(Jx_TGD,Jy_TGD, 'm-o', label='QZS')    
    plt.plot(Ix_TGD,Iy_TGD, 'c-o', label='NIC')   
    plt.legend()

    my_x_ticks = np.arange(0,61, 3)
    my_y_ticks = np.arange(-15, 16, 3)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)

    plt.title(file_name)
    plt.xlabel("prn")
    plt.ylabel("TGD_m")   
    plt.grid(True)
    plt.savefig(file_name+'.png', dpi=120)
    plt.show()  
    #fig = plt.gcf()    
    #.show()
    #fig.savefig('tessstttyyy.png', dpi=100)
    