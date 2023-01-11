import geocoder
from haversine import haversine
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from ast import literal_eval

def getLocation():    
    # 현재 위치 불러오기
    g = geocoder.ip('me')
    g  = g.latlng
    latitude = g[0]
    longitude = g[1]
    result_dict = {"latitude":latitude,"longitude":longitude}
    return result_dict

def getRestaurant(df,latitude, longitude, radius_around, vectors=[]):
    # 위도, 경도 리스트 생성
    df['distance'] = df.apply(lambda x: int(haversine((latitude, longitude),(float(x['latitude']), float(x['longitude'])), unit='m')),axis=1 ) 
    # 주변거리 기준 필터링
    df = df[df['distance']<radius_around+500]
    df = df.sort_values(by='distance')
    df = df.iloc[:100,:]
    

    
    if vectors:
        # 사용할 vector만 추출
        df['comment'] = df['comment'].apply(lambda x: literal_eval(x.replace(" ",""))[:10])
        # 추출된 맛집리스트 초기화
        restaurant_df = df
        # 유저 벡터 df 생성
        user_vector_df = pd.DataFrame([[" ".join(vectors)]])
        user_vector_df.columns=['comment']
        user_vector = " ".join(user_vector_df.values[0])
        
        # 추출된 맛집 리스트 + 유저백터 df 생성
        restaurant_plus_user_vector_df = pd.concat([restaurant_df, user_vector_df])
        # 추출된 맛집 리스트 + 유저백터 인덱스 저장
        index_list = list(restaurant_plus_user_vector_df.index)
        # target_index 수정
        index_list[-1] = 1000000
        
        # 추출된 맛집리스트 
        
        restaurant_df = restaurant_df[['comment']]
        restaurant_df['comment'] = restaurant_df['comment'].apply(lambda x: " ".join(x))
        vector_list = []
        for i in range(len(restaurant_df)):
            v = restaurant_df.iloc[i].values[0]
            vector_list.append(v)
        vector_list.append(user_vector)

        vectorizer  = CountVectorizer(min_df=0, ngram_range=(1, 5))  # min_df: 단어장에 들어갈 최소빈도, ngram_range: 1 <= n <= 2
        restaurant_plus_user_vector_sparse_matrix = vectorizer.fit_transform(vector_list)
        user_similarity = cosine_similarity(restaurant_plus_user_vector_sparse_matrix, restaurant_plus_user_vector_sparse_matrix)
        user_similarity = pd.DataFrame(user_similarity)
        user_similarity.index = index_list
        user_similarity.columns = index_list
        user_similarity = user_similarity.sort_values(by=1000000,ascending=False).iloc[1:,-1:]
        user_similarity.columns = ['accuracy']
        user_similarity_idx = list(user_similarity.index)
        result_df = df.loc[user_similarity_idx]
        result_df = result_df.iloc[:20,:]
        return result_df
        
       
    #     return restaurant_plus_user_vector_result
        
    else:
        return df.iloc[:20,:]


    
#TODO 현재선택된 벡터와 유사한 가게 찾는 함수