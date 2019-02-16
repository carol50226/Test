import numpy as np
import os
import math
import struct
import time, sys
from datetime import datetime
def Write_SP3Error(file_name,svid,error_distance,error_time):
    file_name.write( svid+' ')
    file_name.write( str(max(error_distance))+' ') 
    file_name.write( str(max(error_time)) ) 
    file_name.write('\n')  
            
def Write_SP3Header(file_name,WN,TOW,SV_total_num):
    file_name.seek(0)
    file_name.write(struct.pack('1i1i1B',WN,TOW,SV_total_num))
    
def Fine_SP3Index(YYYY,MON,DD,HH,MM,day,mon,hour,year,minute):
    
    MM=0
    tmp_MON=transfer_type(MON)
    tmp_DD=transfer_type(DD)
    tmp_HH=transfer_type(HH)
    tmp_MM=transfer_type(MM)
    
    list_day=unique_index([j[0] for j in day] , tmp_DD)
    list_mon=unique_index([j[0] for j in mon] , tmp_MON)
    list_hour=unique_index([j[0] for j in hour] , tmp_HH)
    list_year=unique_index([j[0] for j in year] , YYYY)
    list_minute=unique_index([j[0] for j in minute] , tmp_MM)
    list_a=list_set(list_day,list_mon)
    list_b=list_set(list_hour,list_a)
    list_c=list_set(list_year,list_b)
    list_d=list_set(list_minute,list_c)
    return list_d
def Write_SP3ASCIIFormat(file_name,svid,px,py,pz,pt):
    file_name.write( svid+' ')
    for i in range(0,len(px)):
        file_name.write(str(px[i])+' ')
    file_name.write('\n')
    for i in range(0,len(py)):
        file_name.write(str(py[i])+' ')
    file_name.write('\n')
    for i in range(0,len(pz)):
        file_name.write(str(pz[i])+' ')
    file_name.write('\n')
    for i in range(0,len(pt)):
        file_name.write(str(pt[i])+' ')
    file_name.write('\n')
def Write_SP3BinaryFormat(file_name,system,sv_num,px,py,pz,pt):
    file_name.write(struct.pack("1c1b", system, sv_num))  
    file_name.write((px))   
    file_name.write((py))
    file_name.write((pz))
    file_name.write((pt)) 
    
    
def UTC2GPST(YEAR,MON,DAY,HOUR,MINUTE):
    #utc to gpst
    doy=[0,31,59,90,120,151,181,212,243,273,304,334]
    yearsElasped=int(YEAR)-1980
    aa=0
    LeapDay=0
    while aa<=yearsElasped:
        if aa%100 == 20:
            if aa%400 == 20:
                LeapDay=LeapDay+1
        elif aa%4 == 0:
            LeapDay=LeapDay+1
        aa=aa+1
    if(yearsElasped%100==20 )& (MON<=2):
        if(yearsElasped%100==20 )& (MON<=2):
            LeapDay=LeapDay-1
    elif (yearsElasped%4==0 )& (MON<=2):  
        LeapDay=LeapDay-1
    
    DaysElapsed= yearsElasped*365+doy[MON-1]+DAY-1+LeapDay-6
    WN=DaysElapsed//7
    TOW=(DaysElapsed%7)*86400+HOUR*3600+MINUTE*60
    return WN,TOW
def list_set(listA,listB):
    set_AB = set(listA) & set(listB)
    list_AB = list(set_AB)   
    return list_AB
def transfer_type(Value): # '01'->' 1'
    tmp_Value=Value
    if int(Value)<10:
        tmp_Value=' '+str(int(Value))
    return tmp_Value
def unique_index(L, find):
    return [i for i,v in enumerate(L) if v==find]
def Gen_QSP3_WHU(file_name,utc_time):
    YYYY,MON,DD,HH,MM,SS=utc_time.strftime("%Y %m %d %H %M %S ").split()
    print (YYYY,MON,DD,HH,MM,SS)
    year = []
    mon = []
    day = []
    hour = []
    minute=[]
    svid = []
    sv_num=[]
    pos_x = []
    pos_y = []
    pos_z = []
    pos_t = []
    total_calander=0
    
    try:    
        f = open(file_name, 'r')
    except FileNotFoundError:
        print ("FileNotFoundError!!!")
        return 
    
    
    while 1:
        line = f.readline()
        if line[0:4]=='+   ':
            sv_num.append(line[3:6])
        if line[0:3]=='EOF':
            break
        if line[0:1]=='*':
            total_calander=total_calander+1
            
    f.close()
    
    for i in range(0,int(sv_num[0]),1):
        svid.append([])
        pos_x.append([])
        pos_y.append([])
        pos_z.append([])
        pos_t.append([])
    for i in range(0,total_calander,1):
        year.append([])
        mon.append([])
        day.append([])
        hour.append([])
        minute.append([])
    
    sv_idx=0
    calender_idx=0
    
    f = open(file_name, 'r')

    while 1:
        line = f.readline()
        if line[0:1]=='*':
            year[calender_idx].append(line[3:7])
            mon[calender_idx].append(line[8:10])
            day[calender_idx].append(line[11:13])
            hour[calender_idx].append(line[14:16])
            minute[calender_idx].append(line[17:19])
            calender_idx=calender_idx+1
            sv_idx=0

    
        if line[0:1]=='P':
            svid[sv_idx].append(line[0:4])
            pos_x[sv_idx].append(line[5:18]) 
            pos_y[sv_idx].append(line[19:32])  
            pos_z[sv_idx].append(line[33:46])  
            pos_t[sv_idx].append(line[47:60]) 
            sv_idx=sv_idx+1
        if line[0:3]=='EOF':
            break
    f.close()

    SP3_Idx=Fine_SP3Index(YYYY,MON,DD,HH,MM,day,mon,hour,year,minute)


    deg=18
    time_deg=2
    estimate_time=6 # 6hr
    shift_min=30
    SP3_TimeError_threshold=1     #unit:1m
    SP3_DistanceError_threshold=1 #unit:1m
    
    sample_between_min= int(minute[1][0])-int(minute[0][0]) #15 min
    num_sample_in_hour=60//sample_between_min # 4 times
    sample_between_sec= 3600//num_sample_in_hour # 15min=900sec
    interval= estimate_time*num_sample_in_hour
    shift=shift_min//sample_between_min # shift sample   
    sp3_start_point= 4*interval
    
    
    try:
        sp3_start_point=SP3_Idx[0]
    except IndexError:
        print ("FALSE!!! No corresponding time !!!")
        return 
    
    sp3_end_point=sp3_start_point

    offset_estimate=int(sp3_start_point-shift)
    start_sample=offset_estimate
    num_sample_estimate=(num_sample_in_hour*estimate_time)+offset_estimate+shift*2
    x_time=range(0,(num_sample_estimate-offset_estimate)*sample_between_sec,sample_between_sec)
   
    if  offset_estimate<0:
        print("FALSE!!! TOO EARLY !!!")
        return
    
    
    if  num_sample_estimate>192:
        print("FALSE!!! TOO LATE !!!")
        return

    
    
    folder_new=file_name+'_'+'6hr'+'_'+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    folder_new_binary=file_name[0:3]+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    folder_new_binary_G=file_name[0:3]+'G'+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    folder_new_binary_R=file_name[0:3]+'R'+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    folder_new_binary_E=file_name[0:3]+'E'+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    folder_new_binary_C=file_name[0:3]+'C'+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    folder_new_binary_J=file_name[0:3]+'J'+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    
    
    folder_error=file_name[0:3]+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))+'_'+'error'
    
    f_new = open(folder_new, 'w')
    f_new_binary = open(folder_new_binary, 'wb')
    f_new_binary_G = open(folder_new_binary_G, 'wb')
    f_new_binary_R = open(folder_new_binary_R, 'wb')
    f_new_binary_E = open(folder_new_binary_E, 'wb')
    f_new_binary_C = open(folder_new_binary_C, 'wb')
    f_new_binary_J = open(folder_new_binary_J, 'wb')
    
    f_error = open(folder_error,'w')
    
    #utc to gpst
    WN,TOW=UTC2GPST(int(year[start_sample][0]),int(mon[start_sample][0]),int(day[start_sample][0]),int(hour[start_sample][0]),int(minute[start_sample][0]))

    Write_SP3Header(f_new_binary,WN,TOW,int(sv_num[0]))
    Write_SP3Header(f_new_binary_G,WN,TOW,int(sv_num[0]))
    Write_SP3Header(f_new_binary_R,WN,TOW,int(sv_num[0]))
    Write_SP3Header(f_new_binary_E,WN,TOW,int(sv_num[0]))
    Write_SP3Header(f_new_binary_C,WN,TOW,int(sv_num[0]))
    Write_SP3Header(f_new_binary_J,WN,TOW,int(sv_num[0]))  


    SV_total_num=0
    SV_total_num_G=0
    SV_total_num_E=0
    SV_total_num_R=0
    SV_total_num_C=0
    SV_total_num_J=0

    for sv_i in range(0,int(sv_num[0]),1):
        #check all value is ok
        ax=[float(pos_x[sv_i][start_sample+j])- 999999.999999 for j in range(len(pos_x[sv_i][start_sample:num_sample_estimate]))]
        ay=[float(pos_y[sv_i][start_sample+j])- 999999.999999 for j in range(len(pos_y[sv_i][start_sample:num_sample_estimate]))]
        az=[float(pos_z[sv_i][start_sample+j])- 999999.999999 for j in range(len(pos_z[sv_i][start_sample:num_sample_estimate]))]
        at=[float(pos_t[sv_i][start_sample+j])- 999999.999999 for j in range(len(pos_t[sv_i][start_sample:num_sample_estimate]))]
        
        px=np.polyfit(x_time, list(map(float,pos_x[sv_i][start_sample:num_sample_estimate])),deg )
        py=np.polyfit(x_time, list(map(float,pos_y[sv_i][start_sample:num_sample_estimate])),deg )
        pz=np.polyfit(x_time, list(map(float,pos_z[sv_i][start_sample:num_sample_estimate])),deg )
        pt=np.polyfit(x_time, list(map(float,pos_t[sv_i][start_sample:num_sample_estimate])),time_deg )
        
        if max(abs(np.array(ax)))<=10e-5 or max(abs(np.array(ay)))<=10e-5 or max(abs(np.array(az)))<=10e-5 or max(abs(np.array(at)))<=10e-5:
            continue
        ans_fitx=np.polyval(px,x_time)
        ans_fity=np.polyval(py,x_time)
        ans_fitz=np.polyval(pz,x_time)
        ans_fitt=np.polyval(pt,x_time)
        
        x_diff=[float(pos_x[sv_i][start_sample+j])- ans_fitx[j] for j in range(len(pos_x[sv_i][start_sample:num_sample_estimate]))]
        y_diff=[float(pos_y[sv_i][start_sample+j])- ans_fity[j] for j in range(len(pos_y[sv_i][start_sample:num_sample_estimate]))]
        z_diff=[float(pos_z[sv_i][start_sample+j])- ans_fitz[j] for j in range(len(pos_z[sv_i][start_sample:num_sample_estimate]))]
        t_diff=[float(pos_t[sv_i][start_sample+j])- ans_fitt[j] for j in range(len(pos_t[sv_i][start_sample:num_sample_estimate]))]
        
        
        x_diff=np.array(x_diff)*np.array(x_diff)
        y_diff=np.array(y_diff)*np.array(y_diff)
        z_diff=np.array(z_diff)*np.array(z_diff)
        
        error_distance=np.sqrt(x_diff+y_diff+z_diff)*1000 # unit: m
        error_time=np.array(t_diff)*3*10**8*10**-6  # unit: m


        #TODO BIG ERROR
        SV_total_num=SV_total_num+1
        #SV POLYNOMIAL
        Write_SP3ASCIIFormat(f_new,svid[sv_i][0],px,py,pz,pt)        
        #SV ERROR
        Write_SP3Error(f_error,svid[sv_i][0],error_distance,error_time)

        
        
        #SV binary
        Write_SP3BinaryFormat(f_new_binary,bytes(svid[sv_i][0][1],"utf-8"),int(svid[sv_i][0][2:4]),px,py,pz,pt)   
        
        if(svid[sv_i][0][1]=='G'):
            Write_SP3BinaryFormat(f_new_binary_G,bytes(svid[sv_i][0][1],"utf-8"),int(svid[sv_i][0][2:4]),px,py,pz,pt)
            SV_total_num_G=SV_total_num_G+1
        if(svid[sv_i][0][1]=='R'):
            Write_SP3BinaryFormat(f_new_binary_R,bytes(svid[sv_i][0][1],"utf-8"),int(svid[sv_i][0][2:4]),px,py,pz,pt)
            SV_total_num_R=SV_total_num_R+1
        if(svid[sv_i][0][1]=='E'):
            Write_SP3BinaryFormat(f_new_binary_E,bytes(svid[sv_i][0][1],"utf-8"),int(svid[sv_i][0][2:4]),px,py,pz,pt)
            SV_total_num_E=SV_total_num_E+1
        if(svid[sv_i][0][1]=='C'):
            Write_SP3BinaryFormat(f_new_binary_C,bytes(svid[sv_i][0][1],"utf-8"),int(svid[sv_i][0][2:4]),px,py,pz,pt)
            SV_total_num_C=SV_total_num_C+1
        if(svid[sv_i][0][1]=='J'):
            Write_SP3BinaryFormat(f_new_binary_J,bytes(svid[sv_i][0][1],"utf-8"),int(svid[sv_i][0][2:4]),px,py,pz,pt)
            SV_total_num_J=SV_total_num_J+1                
            
    Write_SP3Header(f_new_binary,WN,TOW,SV_total_num)
    Write_SP3Header(f_new_binary_G,WN,TOW,SV_total_num_G)
    Write_SP3Header(f_new_binary_R,WN,TOW,SV_total_num_R)
    Write_SP3Header(f_new_binary_E,WN,TOW,SV_total_num_E)
    Write_SP3Header(f_new_binary_C,WN,TOW,SV_total_num_C)
    Write_SP3Header(f_new_binary_J,WN,TOW,SV_total_num_J)   

    f_error.close()
    f_new_binary.close()
    f_new_binary_G.close()
    f_new_binary_R.close()
    f_new_binary_E.close()
    f_new_binary_C.close()
    f_new_binary_J.close()
def Gen_QSP3_IGU(file_name,utc_time):
    YYYY,MON,DD,HH,MM,SS=utc_time.strftime("%Y %m %d %H %M %S ").split()
    print (YYYY,MON,DD,HH,MM,SS)
    year = []
    mon = []
    day = []
    hour = []
    minute=[]
    svid = []
    sv_num=[]
    pos_x = []
    pos_y = []
    pos_z = []
    pos_t = []
    total_calander=0
    
    try:    
        f = open(file_name, 'r')
    except FileNotFoundError:
        print ("FileNotFoundError!!!")
        return 
    
    
    while 1:
        line = f.readline()
        if line[0:4]=='+   ':
            sv_num.append(line[3:6])
        if line[0:3]=='EOF':
            break
        if line[0:1]=='*':
            total_calander=total_calander+1
            
    f.close()
    
    for i in range(0,int(sv_num[0]),1):
        svid.append([])
        pos_x.append([])
        pos_y.append([])
        pos_z.append([])
        pos_t.append([])
    for i in range(0,total_calander,1):
        year.append([])
        mon.append([])
        day.append([])
        hour.append([])
        minute.append([])
    
    sv_idx=0
    calender_idx=0
    
    f = open(file_name, 'r')

    while 1:
        line = f.readline()
        if line[0:1]=='*':
            year[calender_idx].append(line[3:7])
            mon[calender_idx].append(line[8:10])
            day[calender_idx].append(line[11:13])
            hour[calender_idx].append(line[14:16])
            minute[calender_idx].append(line[17:19])
            calender_idx=calender_idx+1
            sv_idx=0

    
        if line[0:1]=='P':
            svid[sv_idx].append(line[0:4])
            pos_x[sv_idx].append(line[5:18]) 
            pos_y[sv_idx].append(line[19:32])  
            pos_z[sv_idx].append(line[33:46])  
            pos_t[sv_idx].append(line[47:60]) 
            sv_idx=sv_idx+1
        if line[0:3]=='EOF':
            break
    f.close()

    SP3_Idx=Fine_SP3Index(YYYY,MON,DD,HH,MM,day,mon,hour,year,minute)


    deg=18
    time_deg=2
    estimate_time=6 # 6hr
    shift_min=30
    SP3_TimeError_threshold=1     #unit:1m
    SP3_DistanceError_threshold=1 #unit:1m
    
    sample_between_min= int(minute[1][0])-int(minute[0][0]) #15 min
    num_sample_in_hour=60//sample_between_min # 4 times
    sample_between_sec= 3600//num_sample_in_hour # 15min=900sec
    interval= estimate_time*num_sample_in_hour
    shift=shift_min//sample_between_min # shift sample   
    sp3_start_point= 4*interval
    
    
    try:
        sp3_start_point=SP3_Idx[0]
    except IndexError:
        print ("FALSE!!! No corresponding time !!!")
        return 
    
    sp3_end_point=sp3_start_point

    offset_estimate=int(sp3_start_point-shift)
    start_sample=offset_estimate
    num_sample_estimate=(num_sample_in_hour*estimate_time)+offset_estimate+shift*2
    x_time=range(0,(num_sample_estimate-offset_estimate)*sample_between_sec,sample_between_sec)
   
    if  offset_estimate<0:
        print("FALSE!!! TOO EARLY !!!")
        return
    
    
    if  num_sample_estimate>192:
        print("FALSE!!! TOO LATE !!!")
        return

    
    
    folder_new=file_name+'_'+'6hr'+'_'+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    folder_new_binary_G=file_name[0:3]+'G'+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))
    folder_error=file_name[0:3]+str(int(year[start_sample][0]))+'_'+str(int(mon[start_sample][0]))+'_'+str(int(day[start_sample][0]))+'_'+str(int(hour[start_sample][0]))+'_'+str(int(minute[start_sample][0]))+'_'+'error'
    
    f_new = open(folder_new, 'w')
    f_new_binary_G = open(folder_new_binary_G, 'wb')

    
    f_error = open(folder_error,'w')
    
    #utc to gpst
    WN,TOW=UTC2GPST(int(year[start_sample][0]),int(mon[start_sample][0]),int(day[start_sample][0]),int(hour[start_sample][0]),int(minute[start_sample][0]))

    Write_SP3Header(f_new_binary_G,WN,TOW,int(sv_num[0]))

    SV_total_num_G=0


    for sv_i in range(0,int(sv_num[0]),1):
        #check all value is ok
        ax=[float(pos_x[sv_i][start_sample+j])- 999999.999999 for j in range(len(pos_x[sv_i][start_sample:num_sample_estimate]))]
        ay=[float(pos_y[sv_i][start_sample+j])- 999999.999999 for j in range(len(pos_y[sv_i][start_sample:num_sample_estimate]))]
        az=[float(pos_z[sv_i][start_sample+j])- 999999.999999 for j in range(len(pos_z[sv_i][start_sample:num_sample_estimate]))]
        at=[float(pos_t[sv_i][start_sample+j])- 999999.999999 for j in range(len(pos_t[sv_i][start_sample:num_sample_estimate]))]
        
        px=np.polyfit(x_time, list(map(float,pos_x[sv_i][start_sample:num_sample_estimate])),deg )
        py=np.polyfit(x_time, list(map(float,pos_y[sv_i][start_sample:num_sample_estimate])),deg )
        pz=np.polyfit(x_time, list(map(float,pos_z[sv_i][start_sample:num_sample_estimate])),deg )
        pt=np.polyfit(x_time, list(map(float,pos_t[sv_i][start_sample:num_sample_estimate])),time_deg )
        
        if max(abs(np.array(ax)))<=10e-5 or max(abs(np.array(ay)))<=10e-5 or max(abs(np.array(az)))<=10e-5 or max(abs(np.array(at)))<=10e-5:
            continue
        ans_fitx=np.polyval(px,x_time)
        ans_fity=np.polyval(py,x_time)
        ans_fitz=np.polyval(pz,x_time)
        ans_fitt=np.polyval(pt,x_time)
        
        x_diff=[float(pos_x[sv_i][start_sample+j])- ans_fitx[j] for j in range(len(pos_x[sv_i][start_sample:num_sample_estimate]))]
        y_diff=[float(pos_y[sv_i][start_sample+j])- ans_fity[j] for j in range(len(pos_y[sv_i][start_sample:num_sample_estimate]))]
        z_diff=[float(pos_z[sv_i][start_sample+j])- ans_fitz[j] for j in range(len(pos_z[sv_i][start_sample:num_sample_estimate]))]
        t_diff=[float(pos_t[sv_i][start_sample+j])- ans_fitt[j] for j in range(len(pos_t[sv_i][start_sample:num_sample_estimate]))]
        
        
        x_diff=np.array(x_diff)*np.array(x_diff)
        y_diff=np.array(y_diff)*np.array(y_diff)
        z_diff=np.array(z_diff)*np.array(z_diff)
        
        error_distance=np.sqrt(x_diff+y_diff+z_diff)*1000 # unit: m
        error_time=np.array(t_diff)*3*10**8*10**-6  # unit: m


        #TODO BIG ERROR

        #SV POLYNOMIAL
        Write_SP3ASCIIFormat(f_new,svid[sv_i][0],px,py,pz,pt)        
        #SV ERROR
        Write_SP3Error(f_error,svid[sv_i][0],error_distance,error_time)

        
        
        #SV binary
        if(svid[sv_i][0][1]=='G'):
            Write_SP3BinaryFormat(f_new_binary_G,bytes(svid[sv_i][0][1],"utf-8"),int(svid[sv_i][0][2:4]),px,py,pz,pt)
            SV_total_num_G=SV_total_num_G+1
      
            

    Write_SP3Header(f_new_binary_G,WN,TOW,SV_total_num_G)

    f_error.close()
    f_new_binary_G.close()

    

if __name__ == '__main__':
    ts=datetime.utcnow()
    #Gen_QSP3_WHU('whu20060_09.sp3',datetime(2018, 6, 17, 9, 30, 4, 310106))
    Gen_QSP3_IGU('igu16295_06.sp3',datetime(2011, 4, 1, 6, 30, 4, 310106))
    #Gen_QSP3_WHU('whu20060_09.sp3',datetime(2018, 6, 18, 2, 0, 4, 310106))
    #datetime.datetime(2018, 6, 17, 9, 0, 4, 310106)
    YYYY,MON,DD,HH,MM,SS=ts.strftime("%Y %m %d %H %M %S ").split()
    print (YYYY,MON,DD,HH,MM,SS)
