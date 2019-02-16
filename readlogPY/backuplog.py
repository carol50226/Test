import matplotlib.pyplot as plt
import pynmea2
import cgi
import math
import numpy as np
from math import radians, cos, sin, asin, sqrt
import pyproj
import re
import pymap3d as pm

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

def parse_dms(dms):
    parts = re.split('[^\d\w]+', dms)
    lat = dms2dd(parts[0], parts[1], parts[2], parts[3])
    lng = dms2dd(parts[4], parts[5], parts[6], parts[7])

    return (lat, lng)

## ==========================================================================================================================
def np_getDistance(A , B ):# 先緯度後經度
    ra = 6378140  # radius of equator: meter
    rb = 6356755  # radius of polar: meter
    flatten = 0.003353 # Partial rate of the earth
    # change angle to radians
    
    radLatA = np.radians(A[:,0])
    radLonA = np.radians(A[:,1])
    radLatB = np.radians(B[:,0])
    radLonB = np.radians(B[:,1])
 
    pA = np.arctan(rb / ra * np.tan(radLatA))
    pB = np.arctan(rb / ra * np.tan(radLatB))
    
    x = np.arccos( np.multiply(np.sin(pA),np.sin(pB)) + np.multiply(np.multiply(np.cos(pA),np.cos(pB)),np.cos(radLonA - radLonB)))
    c1 = np.multiply((np.sin(x) - x) , np.power((np.sin(pA) + np.sin(pB)),2)) / np.power(np.cos(x / 2),2)
    c2 = np.multiply((np.sin(x) + x) , np.power((np.sin(pA) - np.sin(pB)),2)) / np.power(np.sin(x / 2),2)
    dr = flatten / 8 * (c1 - c2)
    distance = 0.001 * ra * (x + dr)
    return distance

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

rangeUpdateTime = [0.0]


if __name__=='__main__': 
    input = open('serverlog.txt', 'r')
    file_name='tesst.nmea'
    input_nmea = open(file_name, 'r')

    RTKlog_name = open(file_name+'_log', 'w')
    line = '$GPGGA,092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,*76'
    #record = pynmea2.parse(line)
    for line in input_nmea:
        
        if 'GGA' in line:
            record = pynmea2.parse(line)
            Write_RTKlibFormat(RTKlog_name,line)

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
    
    
    
    A=np.matrix([[25.060835, 121.544242]])
    B=np.matrix([[25.062247, 121.544236]])
    

    Distance_2=np_getDistance(A,B)
    Distance_3=getDistance(25.060835, 121.544242,25.062247, 121.544236)
    x = 0
    y = 45
    z = 1000
    
    ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
    lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
    lon, lat, alt = pyproj.transform(ecef, lla, x, y, z, radians=True)

    print ( Distance_2, Distance_3)
    dd = parse_dms("36°57'9' N 110°4'21' W")
    
    x,y,z=pm.geodetic2ecef(22.99665875 ,120.222584889,98.211)
    x,y,z=pm.ecef2geodetic(x,y,z)
    print(x,y,z)
    print(dd)
    print(dd2dms(dd[0]))

    for line in input:
        line = line.split()
        if 'update' in line:
            rangeUpdateTime.append(float(line[-1]))
    
    plt.figure('frame time')
    plt.subplot(211)
    plt.plot(rangeUpdateTime, '.r',)
    plt.grid(True)
    plt.subplot(212)
    plt.plot(rangeUpdateTime)
    plt.grid(True)
    plt.show()