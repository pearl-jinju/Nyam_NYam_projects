import geocoder
from haversine import haversine
import pandas as pd

def getLocation():    
    # 현재 위치 불러오기
    g = geocoder.ip('me')
    g  = g.latlng
    latitude = g[0]
    longitude = g[1]
    result_dict = {"latitude":latitude,"longitude":longitude}
    return result_dict

def getNearRestaurant(df,latitude,longitude,radius_around=30000):
    # 위도, 경도 리스트 생성
    df['distance'] = df.apply(lambda x: int(haversine((latitude, longitude),(float(x['latitude']), float(x['longitude'])), unit='m')),axis=1 ) 
    # 주변거리 기준 필터링
    df = df[df['distance']<radius_around]
    # 거리순 정렬
    df = df.sort_values(by="distance")
    return df
    