import matplotlib.pyplot as plt
import pynmea2
import math
import numpy as np
import re
import pymap3d as pm
from math import radians, cos, sin, asin, sqrt
EARTH_REDIUS = 6378.137

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
Distance_2Derror=[]
ecef_x=[]
ecef_y=[]
ecef_z=[]

True_Lat=25.062247
True_Lon=121.544236
if __name__=='__main__': 
    file_name='tesst.nmea'
    input_nmea = open(file_name, 'r')

    RTKlog_name = open(file_name+'_log', 'w')
    line = '$GPGGA,092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,*76'
    #record = pynmea2.parse(line)
    for line in input_nmea:
        
        if 'GGA' in line:
            record = pynmea2.parse(line)
            Write_RTKlibFormat(RTKlog_name,line)
            
            #aa='{:02d}°{:02d}′{:07.4f}″'.format(int(record.latitude), int(record.latitude_minutes), record.latitude_seconds)
            #int(record.latitude) int(record.latitude_minutes) record.latitude_seconds
            #tset_z=parse_dms()  
            
            
            
            
            x,y,z=pm.geodetic2ecef(record.latitude ,record.longitude,record.altitude)
            
            
            
            
            ecef_x.append(x)
            ecef_y.append(y)
            ecef_z.append(z)
            error=getDistance(record.latitude, record.longitude,True_Lat, True_Lon)         
            Distance_2Derror.append(error)
            '''
            print('Latitude: {:02d}°{:02d}′{:07.4f}″'.format(int(record.latitude), int(record.latitude_minutes), record.latitude_seconds))
            print('Longitude: {:02d}°{:02d}′{:07.4f}″'.format(int(record.longitude), int(record.longitude_minutes), record.longitude_seconds))
            print('Altitude: {:.3f}'.format(record.altitude))
            '''
            
        #if 'GPGSA' in line:
            #Write_RTKlibFormat(RTKlog_name,line)
        if 'GPRMC' in line:
            Write_RTKlibFormat(RTKlog_name,line)
    RTKlog_name.close()
    
    

    #error=getDistance(25.060835, 121.544242,True_Lat, True_Lon)
    #Distance_2Derror.append(error)
    


    
    t=range(0,len(ecef_x),1)
    plt.figure('ECEF')
    plt.subplot(311)
    plt.plot(t,ecef_x, 'r',)
    plt.grid(True)
    plt.subplot(312)
    plt.plot(t,ecef_y, 'r',)
    plt.grid(True)
    plt.subplot(313)
    plt.plot(t,ecef_z, 'r',)   
    plt.grid(True)
    plt.show()
    
    print("2Derror= %s" %np.mean(Distance_2Derror))