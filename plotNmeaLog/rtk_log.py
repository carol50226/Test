import matplotlib.pyplot as plt
import pynmea2
import math
import numpy as np
import re
import pymap3d as pm
import pandas as pd 
from math import radians, cos, sin, asin, sqrt
EARTH_REDIUS = 6378.137 # km

def get_closest(array,value):
    array=np.array(array)
    idxs=np.searchsorted(array,value,side='left')
    return idxs
def dms2dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60);
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd;

def dd2dms(deg):
    d = int(deg)
    md = abs(deg - d) * 60
    m = int(md)
    sd = (md - m) * 60
    return [d, m, sd]




def rad(d):
    return d * np.pi / 180.0

def getDistance(lat1, lng1, lat2, lng2):
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(math.sqrt(math.pow(sin(a/2), 2) + cos(radLat1) * cos(radLat2) * math.pow(sin(b/2), 2)))
    s = s * EARTH_REDIUS
    return s


def deg2num(lat_deg=0.0, lon_deg=0.0, zoom=12):
  lat_rad = math.radians(lat_deg)
  n = 2.0 ** zoom
  xtile = int((lon_deg + 180.0) / 360.0 * n)
  ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
  return (xtile, ytile)

def Write_RTKlibFormat(file_name,data):
    file_name.write(data)  

def parse_dms(a,b,c,d,a1,b1,c1,d1):
    #parts = re.split('[^\d\w]+', dms)
    lat = dms2dd(a, b, c, d)
    lng = dms2dd(a1,b1, c1, d1)

    return (lat, lng)
def plot_cdf(data):
    x=np.sort(data)
    y=np.arange(1,len(x)+1)/len(x)
    fig=plt.figure()
    bx=fig.add_subplot(111)
    bx.plot(x,y,marker='.')#,linestyles='none'
    plt.title('ERROR CDF')
    plt.ylabel('%')
    plt.xlabel('m')
    plt.grid(True)
    plt.show()
    
    idx95=get_closest(y,0.95)
    idx67=get_closest(y,0.67)
    idx50=get_closest(y,0.5)
    print("2D_95 error= %s 67=%s 50=%s" %(x[idx95],x[idx67],x[idx50]))
    
    
def plot_ecef(ecef_x,ecef_y,ecef_z):
    t=range(0,len(ecef_x),1)
    fig = plt.figure('ECEF')
    plt.subplot(311)
    plt.plot(t,ecef_x, 'r',)
    plt.grid(True)
    plt.subplot(312)
    plt.plot(t,ecef_y, 'r',)
    plt.grid(True)
    plt.subplot(313)
    plt.plot(t,ecef_z, 'r',)   
    plt.grid(True)
    fig.suptitle("ECEF", fontsize=16)
    plt.show()
def plot_enu(E,N,U):
    
    RMSE_E_error=sqrt(sum(np.power(E,2))/len(E))
    RMSE_N_error=sqrt(sum(np.power(N,2))/len(N))
    RMSE_U_error=sqrt(sum(np.power(U,2))/len(U))
    
    
    
    
    t=range(0,len(E),1)
    fig = plt.figure('ENU')
    a = plt.subplot(311)
    plt.plot(t,E, 'b',)
    plt.grid(True)
    b = plt.subplot(312)
    plt.plot(t,N, 'b',)
    plt.grid(True)
    c = plt.subplot(313)
    plt.plot(t,U, 'b',)  
    
    
    fig.suptitle("ENU", fontsize=16) 
    a.title.set_text("E RMSE= %s "%(RMSE_E_error))
    b.title.set_text("N RMSE= %s "%(RMSE_N_error))
    c.title.set_text("U RMSE= %s "%(RMSE_U_error))
    
    plt.grid(True)
    plt.show()


    print("Rmse_error E= %s N=%s U=%s" %(RMSE_E_error,RMSE_N_error,RMSE_U_error))    
    
Distance_2Derror=[]
ecef_x=[]
ecef_y=[]
ecef_z=[]
E=[]
N=[]
U=[]
True_Lat=22.996658750
True_Lon=120.222584889
True_Hei=98.2110
if __name__=='__main__': 
    
    
    file_name='NCKU_trimble_b31_0615.pos'
    
    #data = pd.read_csv('NCKU_trimble_b31_0615_pd.pos',sep=" ")
    #myframe = pd.DataFrame(data)
    
    #input_nmea = open(file_name, 'r')

    #RTKlog_name = open(file_name+'_log', 'w')
    True_x,True_y,True_z=pm.geodetic2ecef(True_Lat ,True_Lon,True_Hei)
    
    l1,l2,h=pm.ecef2geodetic(True_x,True_y,True_z)
    line = '$GPGGA,092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,*76'

    f = open(file_name,'r')
    line=f.readline()
    while 1:
        line=f.readline()
        if line:
            if str(line[0:1])=='%':
                continue
            x=float(line[25:38])
            y=float(line[40:53])
            z=float(line[56:68])
            ecef_x.append(x)
            ecef_y.append(y)
            ecef_z.append(z)  
            l1,l2,h=pm.ecef2geodetic(x,y,z)
            e,n,u=pm.ecef2enu(x,y,z,True_Lat,True_Lon,True_Hei)
            E.append(e)
            N.append(n)
            U.append(u)
            error=getDistance(l1, l2,True_Lat, True_Lon)         
            Distance_2Derror.append(error*1000) #to m
        else:
            break
    f.close()
    #error=getDistance(25.060835, 121.544242,True_Lat, True_Lon)
    #Distance_2Derror.append(error)
    


    

    plot_enu(E,N,U)    




    plot_cdf(Distance_2Derror)
    
    
    plot_ecef(ecef_x,ecef_y,ecef_z)    
    
    
    DISTANCE=np.sqrt(np.power(E,2)+np.power(N,2))
    t=range(0,len(DISTANCE),1)
    plt.figure('ECEF')
    plt.plot(t,DISTANCE, 'b')
    plt.title("2Derror")
    plt.grid(True)
    plt.show()



    plt.subplot(221)
    plt.hist(Distance_2Derror)
    plt.subplot(222)
    hist, bin_edges = np.histogram(Distance_2Derror)
    plt.plot(hist)
        
    plt.grid(True)
    plt.show()

  


    t=range(0,len(Distance_2Derror),1)
    plt.figure('ECEF')
    #plt.plot(t,Distance_2Derror, 'r')
    plt.plot(t,Distance_2Derror,t,DISTANCE)
    plt.grid(True)
    plt.show()

    RMSE_2D_error=sqrt(sum(np.power(Distance_2Derror,2))/len(Distance_2Derror))
    MSE_2D_error=(sum(np.power(Distance_2Derror,2))/len(Distance_2Derror))
    print("2DMean_error= %s" %np.mean(Distance_2Derror))
    print("2DStd_error= %s" %np.std(Distance_2Derror))
    print("2DRmse_error(RMSE)= %s" %RMSE_2D_error)
    print("2DMse_error(MSE,MDE)= %s" %MSE_2D_error)
    
    
    
    
    
    
    
    
    
    mu, sigma = 0, 3 # mean and standard deviation
    s = np.random.normal(mu, sigma, 10000) #Create Gaussian Noise
    #Plot Gaussian Noise
    plt.subplot(1,2,1);
    plt.xlim(0,1000)
    plt.ylim(-20,20)
    plt.plot(np.linspace(1, 10000, num = 10000),s )
    
    #Plot Gaussian Distribution
    plt.subplot(1,2,2);
    count, bins, ignored = plt.hist(Distance_2Derror, 30, normed=True)
    #plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * 
    #         np.exp( - (bins - mu)**2 / (2 * sigma**2) ), 
    #         linewidth=2, color='r')
    plt.show()
    
    plot_cdf(s)