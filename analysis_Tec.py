
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
file_name='c2pg1520.19i'

def PLOT_3D_TEC(Data,time_index):
    # X, Y value
    X = np.arange(-87.5,87.5+1, 2.5)
    Y = np.arange(-180, 180+1, 5)    
    X, Y = np.meshgrid(X, Y)    # x-y 

    matrix=[]
    for lon_index in range(0,len(Data[0][1])):
        
        a=Data[time_index][1][lon_index][1]
        a=np.array(a)
        matrix.append(a)

    matrix_b=np.array(matrix)
    matrix_b = matrix_b.T

    # height value
    Z =matrix_b
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
    date_plot=Data[time_index][0]
    plt.title("IONEX date= %s  "%(date_plot))
    plt.xlabel("lat") 
    plt.ylabel("lon")
    plt.show()    
    
    
def PLOT_TEC(data,len_x,date_plot,lon_plot,lat_plot):
    t=range(0,len_x,1)
    plt.figure('TEC')
    plt.plot(t,data, 'r',marker ='o')
    plt.grid(True)
    plt.xlabel("hour") 
    plt.ylabel("TEC")
    plt.xticks(range(-1,25))
    plt.yticks(range(0,400,50))
    plt.title("IONEX date= %s lon= %s lat = %s  "%(date_plot,lon_plot,lat_plot))
    
    plt.show()  
    
def PLOT_LatTEC(data,len_x,date_plot,lat_plot):
    lon_value=[]
    for i in range(0,len_x,1):
        lon_value.append((i-36)*5)
    #t=range(0,len_x,1)
    plt.figure('TEC')
    plt.plot(lon_value,data, 'r',marker ='o')
    plt.grid(True)
    plt.xlabel("longitude") 
    plt.ylabel("TEC")
    plt.xticks(range(-210,210,30))
    plt.yticks(range(0,400,50))
    plt.title("IONEX date= %s lat= %s "%(date_plot,lat_plot))
    
    plt.show()
def PLOT_LonTEC(data,len_x,date_plot,lon_plot):
    lat_value=[]
    for i in range(0,len_x,1):
        lat_value.append((i-35)*2.5)
    #t=range(0,len_x,1)
    plt.figure('TEC')
    plt.plot(lat_value,data, 'r',marker ='o')
    plt.grid(True)
    plt.xlabel("latitude") 
    plt.ylabel("TEC")
    plt.xticks(range(-100,100,10))
    plt.yticks(range(0,400,50))
    plt.title("IONEX date= %s lon = %s  "%(date_plot,lon_plot))
    
    plt.show()
if __name__ == '__main__':
    Data=[]
    lat_data=[]
    total_data=[]
    tmp_data=[]
    ## Open file
    try:    
        fp = open(file_name, 'r')
    except FileNotFoundError:
        print ("FileNotFoundError!!!")
    line = fp.readline()   
    
    
    while line:
        line_split=line.split( )
        '''
        char1=line_split.find('EPOCH')
        char2=line_split.find('OF')
        char3=line_split.find('CURRENT')
        char4=line_split.find('MAP')
        '''
        time_tag=line.find('EPOCH OF CURRENT MAP')
        lon_value=line.find('LAT/LON1/LON2/DLON/H')
        time_end=line.find('END OF TEC MAP')
        
        if(time_tag>0):
            
            time_list=line.split( )
            utc_time=datetime(int(time_list[0]), int(time_list[1]), int(time_list[2]), int(time_list[3]), int(time_list[4]), int(time_list[5]), 0)
            #YYYY,MON,DD,HH,MM,SS=utc_time.strftime("%Y %m %d %H %M %S ").split()
            #print (YYYY,MON,DD,HH,MM,SS)
            #Data.append(utc_time)
        if(lon_value>0):
            
            lon=float(line[3:8])
            #lat_data.append(lon)
            for i in range(0,5):
                line = fp.readline()
                line_split_lat=line.split() 
                for index in range(len(line_split_lat)):    
                    lat_data.append(float(line_split_lat[index]))
            
            total_data.append([lon,lat_data])
            #total_data.append(lat_data)
            lat_data=[]  
            #lat = fp.readline()
        if(time_end>0):
            Data.append([utc_time,total_data]) 
            total_data=[]           
        line = fp.readline()
     
    fp.close()  
    
    for time_index in range(0,len(Data)):      
        lon_index=35
        lat_index=36
        tmp_data.append(Data[time_index][1][lon_index][1][lat_index])
        date_plot=Data[time_index][0]
        lon_plot=Data[time_index][1][lon_index][0]
        lat_plot=(lat_index-36)*5#Data[time_index][1][lon_index][1][lat_index]
    #print(tmp_data)
    
    PLOT_TEC(tmp_data,len(Data),date_plot,lat_plot,lon_plot)
        
    #for lon_index in range(0,Data[0][1][0][1])):
 
    #地球呼拉圈 varable=lon_index
    for time_index in range(0,len(Data)):
        lon_index=35
    date_plot=Data[time_index][0]
    lon_plot=Data[time_index][1][lon_index][0] 
    lat_plot=(lat_index-36)*5#Data[time_index][1][lon_index][1][lat_index]
    PLOT_LatTEC(Data[time_index][1][lon_index][1],len(Data[0][1][0][1]),date_plot,lon_plot)
    
    
    
    
    
    #地球重直 varable=lat_index
    tmp_data=[]
    time_index=0
    for time_index in range(0,len(Data)):
        tmp_data=[]
        for lon_index in range(0,len(Data[0][1])): 
            
            lat_index=0
            tmp_data.append(Data[time_index][1][lon_index][1][lat_index])
            
    date_plot=Data[time_index][0]
    lon_plot=Data[time_index][1][lon_index][0]
    lat_plot=(lat_index-36)*5#Data[time_index][1][lon_index][1][lat_index]
    PLOT_LonTEC(tmp_data,len(Data[0][1]),date_plot,lat_plot)
    
    
    
    time_index=24
    for time_index in range(0,len(Data)):
        time_index=24
        
    PLOT_3D_TEC(Data,time_index)
    