# -*- coding: utf-8 -*-
"""
Created on Wed Sep 12 21:14:13 2018

@author: User
"""
#from io import StringIO 
import numpy as np
import os
import math
import struct

'''
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".sp3"):
        folder=os.path.dirname(__file__)+'/'+file
        #f = open(folder, 'r')
        #line = f.readline()
        print file,
'''    
for root, dirs, files in os.walk(os.path.dirname(__file__)):
    for file in files:
        if file.endswith(".sp3"):
             folder=os.path.dirname(__file__)+'/'+file
             year = []
             mon = []
             day = []
             hour = []
             minute=[]
             svid = []
             pos_x = []
             pos_y = []
             pos_z = []
             pos_t = []
             total_sp3_SV_number=0
             #year.append([])
                
             f = open(folder, 'r')
             while 1:
                 line = f.readline()
                 if line[0:3]=='EOF':
                     break
                 if line[0:3]=='+  ':
                     total_sp3_SV_number=line[4:6]
                     break
             f.close()                             
             for i in range(0,int(total_sp3_SV_number),1):
                 svid.append([])
                 pos_x.append([])
                 pos_y.append([])
                 pos_z.append([])
                 pos_t.append([])
                
             f = open(folder, 'r')
             time_ith=0
             SV_idx=0
             while 1:
                 line = f.readline()
                 if line[0:3]=='EOF':
                     break
            
                 if line[0:1]=='P':
                     svid[time_ith].append(line[0:4])
                     pos_x[time_ith].append(line[5:18]) 
                     pos_y[time_ith].append(line[19:32])  
                     pos_z[time_ith].append(line[33:46])  
                     pos_t[time_ith].append(line[47:60]) 
                     time_ith=time_ith+1
                 if line[0:1]=='*':
                     year.append(line[3:7])
                     mon.append(line[8:10])
                     day.append(line[11:13])
                     hour.append(line[14:16])
                     minute.append(line[17:19])
                    
                     time_ith=0    
                
             f.close()
            
            
                
             deg=18
             time_deg=2
             shift_min=30
             sample_between_min= int(minute[1])-int(minute[0]) #15 min
             estimate_time=6 # 6hr
             num_sample_in_hour=60/sample_between_min # 4 times
            
             sample_between_sec= 3600/num_sample_in_hour # 15min=900sec
             interval= estimate_time*num_sample_in_hour
             shift=shift_min/sample_between_min # shift sample
                    
             sp3_start_point= 4*interval  
             sp3_end_point= len(year)-interval 
            
            
             for offset_estimate in range(sp3_start_point-shift,sp3_end_point-shift+1,interval):
            
                 start_sample=offset_estimate
                 num_sample_estimate=(num_sample_in_hour*estimate_time)+offset_estimate+shift*2
                 x_time=range(0,(num_sample_estimate-offset_estimate)*sample_between_sec,sample_between_sec)
            
                 if offset_estimate==sp3_end_point-shift:
                     start_sample=offset_estimate
                     num_sample_estimate=(num_sample_in_hour*estimate_time)+offset_estimate+shift
                     x_time=range(0,(num_sample_estimate-offset_estimate)*sample_between_sec,sample_between_sec)
                
                 filename=file[0:3]+str(int(year[start_sample]))+'_'+str(int(mon[start_sample]))+'_'+str(int(day[start_sample]))+'_'+str(int(hour[start_sample]))+'_'+str(int(minute[start_sample]))
                 filename_G=file[0:3]+'G'+str(int(year[start_sample]))+'_'+str(int(mon[start_sample]))+'_'+str(int(day[start_sample]))+'_'+str(int(hour[start_sample]))+'_'+str(int(minute[start_sample]))
                 filename_C=file[0:3]+'C'+str(int(year[start_sample]))+'_'+str(int(mon[start_sample]))+'_'+str(int(day[start_sample]))+'_'+str(int(hour[start_sample]))+'_'+str(int(minute[start_sample]))
                 filename_R=file[0:3]+'R'+str(int(year[start_sample]))+'_'+str(int(mon[start_sample]))+'_'+str(int(day[start_sample]))+'_'+str(int(hour[start_sample]))+'_'+str(int(minute[start_sample]))
                 filename_E=file[0:3]+'E'+str(int(year[start_sample]))+'_'+str(int(mon[start_sample]))+'_'+str(int(day[start_sample]))+'_'+str(int(hour[start_sample]))+'_'+str(int(minute[start_sample]))
                 filename_J=file[0:3]+'J'+str(int(year[start_sample]))+'_'+str(int(mon[start_sample]))+'_'+str(int(day[start_sample]))+'_'+str(int(hour[start_sample]))+'_'+str(int(minute[start_sample]))
                 
                 filename_error=file[0:3]+str(int(year[start_sample]))+'_'+str(int(mon[start_sample]))+'_'+str(int(day[start_sample]))+'_'+str(int(hour[start_sample]))+'_'+str(int(minute[start_sample]))+'_'+'error'
                 filename_binary=file[0:3]+str(int(year[start_sample]))+'_'+str(int(mon[start_sample]))+'_'+str(int(day[start_sample]))+'_'+str(int(hour[start_sample]))+'_'+str(int(minute[start_sample]))+'_'+'binary'
                 f_new = open(filename, 'w')
                 
                 f_new_G = open(filename_G, 'w')
                 f_new_R = open(filename_R, 'w')
                 f_new_E = open(filename_E, 'w')
                 f_new_C = open(filename_C, 'w')
                 f_new_J = open(filename_J, 'w')
                 
                 f_error = open(filename_error, 'w')   
                 f_binary = open(filename_binary, 'wb') 
                 for sv_idx in range(0,int(total_sp3_SV_number),1):
                     px=np.polyfit(x_time, map(float,pos_x[sv_idx][start_sample:num_sample_estimate]),deg )
                     py=np.polyfit(x_time, map(float,pos_y[sv_idx][start_sample:num_sample_estimate]),deg )
                     pz=np.polyfit(x_time, map(float,pos_z[sv_idx][start_sample:num_sample_estimate]),deg )
                     pt=np.polyfit(x_time, map(float,pos_t[sv_idx][start_sample:num_sample_estimate]),time_deg )
                    
                     ans_fitx=np.polyval(px,x_time)
                     ans_fity=np.polyval(py,x_time)
                     ans_fitz=np.polyval(pz,x_time)
                     ans_fitt=np.polyval(pt,x_time)
                    
                     x_diff=map(float,pos_x[sv_idx][start_sample:num_sample_estimate])-ans_fitx
                     y_diff=map(float,pos_y[sv_idx][start_sample:num_sample_estimate])-ans_fity
                     z_diff=map(float,pos_z[sv_idx][start_sample:num_sample_estimate])-ans_fitz
                     t_diff=map(float,pos_t[sv_idx][start_sample:num_sample_estimate])-ans_fitt
                     x_diff=x_diff*x_diff
                     y_diff=y_diff*y_diff
                     z_diff=z_diff*z_diff
                    
                     error_distance=np.sqrt(x_diff+y_diff+z_diff)*1000 # unit: m
                     error_time=t_diff*3*10**8*10**-6  # unit: m
                    
                    
                    
                     f_new.write( svid[sv_idx][0]+' ')
                     for i in range(0,len(px),1):
                         f_new.write(str(px[i])+' ')
                     f_new.write('\n')
                     for i in range(0,len(py),1):
                         f_new.write(str(py[i])+' ')
                     f_new.write('\n')
                     for i in range(0,len(pz),1):
                         f_new.write(str(pz[i])+' ')
                     f_new.write('\n')
                     for i in range(0,len(pt),1):
                         f_new.write(str(pt[i])+' ')
                     f_new.write('\n')
                    
                     f_error.write( svid[sv_idx][0]+' ')
                     f_error.write( str(max(error_distance))+' ') 
                     f_error.write( str(max(error_time)) ) 
                     f_error.write('\n')
                    
                    
                     #f_binary.write( svid[sv_idx][0]+' ')
                    
                    
                    
                    
                     f_binary.write(struct.pack("1c1b", svid[sv_idx][0][1], int(svid[sv_idx][0][2:4])))  
                     f_binary.write((px))   
                     '''
                     f_binary.write((py))
                     f_binary.write((pz))
                     f_binary.write((pt))
                     '''
                     '''
                     f_binary.write(bytearray(px))
                     f_binary.write('\n')
                     f_binary.write(bytearray(px))
                     f_binary.write('\n')
                     '''
                 '''
                 a=np.array([5.67403582e-75,2,3,2.5,222])
                 f_binary.write(a)   
                 '''
                 f_new.close()
                 f_new_G.close()
                 f_new_R.close()
                 f_new_E.close()
                 f_new_C.close()
                 f_new_J.close()
                 f_binary.close()
                 f_error.close()             
             
             
             
             
             
             
             
             
             
             
             
             print(os.path.join(root, file))        
        
        






