import matplotlib.pyplot as plt
import pynmea2
import math
import numpy as np
import re
import sys
import pymap3d as pm
from math import radians, cos, sin, asin, sqrt
EARTH_REDIUS = 6378.137
Knot2kmhr = 1.852 #1.852 km/hr
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

True_Lat=25.062247
True_Lon=121.544236
def getGGA_time(line):
    if 'GGA' in line:
        data = line.split(',')
        hhmmss = data[1]
    return hhmmss
def getGGA_userPOS(line):
    if 'GGA' in line:
        record = pynmea2.parse(line)
        x,y,z=pm.geodetic2ecef(record.latitude ,record.longitude,record.altitude)

        lat = record.latitude
        lon = record.longitude
        #ecef_x.append(x)
        #ecef_y.append(y)
        #ecef_z.append(z)
        
    
        #error=getDistance(record.latitude, record.longitude,True_Lat, True_Lon)         
        #Distance_2Derror.append(error)   
    return (lat,lon,x,y,z)
def getRMC_speed(line):
        record = pynmea2.parse(line)
        speed = record.spd_over_grnd * Knot2kmhr
        
        return(speed)
def write_csv(file_name,data,hhmmss):
    file_name.write(hhmmss)
    file_name.write(" ")
    file_name.write(data)  
def main(file_name):
    file_1_hhmmss = []
    file_1_index = []
    file_1_speed = []
    index = 0
    Distance_2Derror=[]
    ecef_x=[]
    ecef_y=[]
    ecef_z=[]
    
    input_nmea = open(file_name, 'r')
    csv_name = open(file_name+'_csv', 'w')
    #record = pynmea2.parse(line)
    for line in input_nmea:
        
        if 'GGA' in line:
            index = index +1

                  
            hhmmss = getGGA_time(line)
            file_1_hhmmss.append(hhmmss)
            file_1_index.append(index)


            lat,lon,x,y,z = getGGA_userPOS(line)
            ecef_x.append(x)
            ecef_y.append(y)
            ecef_z.append(z)

            
        #if 'GPGSA' in line:
            #Write_RTKlibFormat(RTKlog_name,line)
        if 'GPRMC' in line:
            tmpRMC = line
            speed = getRMC_speed(line)
            file_1_speed.append(speed)
        if 'GPGSA' in line:
            write_csv(csv_name,tmpRMC,hhmmss)
            record = pynmea2.parse(line)
        if 'GPGSV' in line:
            record = pynmea2.parse(line)
        if 'DBG' in line:
            record = pynmea2.parse(line)
            #Write_RTKlibFormat(RTKlog_name,line)
            
    input_nmea.close()
    csv_name.close()
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
    
    plt.figure('SPEED')
    t=range(0,len(file_1_speed),1)
    plt.plot(t,file_1_speed, 'r',)
    plt.grid(True)
    plt.show()
    
    return file_1_hhmmss,file_1_speed
if __name__=='__main__': 
    file_name='tesst.nmea'
    #sys.argv[1]
    #main(sys.argv[1])
    hhmmss_1,speed_1 = main(file_name)
    hhmmss_2,speed_2 = main(file_name)
    A = np.array(hhmmss_1)

    #A = A.astype(int)
    #A = list(map(int, A))
    plt.figure('SPEED')
    t1 = range(0,len(hhmmss_1)+1,1)
    t2 = range(0,len(hhmmss_2),1)
    plt.plot(t1,speed_1, 'r',)
    plt.plot(t1,speed_2, 'g',)
    plt.grid(True)
    plt.show()    

    
    #print("2Derror= %s" %np.mean(Distance_2Derror))