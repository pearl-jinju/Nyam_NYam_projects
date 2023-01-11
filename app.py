import streamlit as st
import pandas as pd
import pickle
import re
from tqdm import tqdm
from ast import literal_eval
from main import getLocation, getRestaurant
from streamlit.components.v1 import html
from urllib import parse
from streamlit_javascript import st_javascript
import random



#TODO streamlit viewport 문제 mobile responsive

#=========================================== config 영역
MAX_VECTORS = 8


st.set_page_config(
    page_title="모든 맛집이 내 손안에! 냠냠",
    layout="centered"
  )



# 주변거리 함수
def distance_to_text(distance):
    if distance<1000:
        distance_text = "1KM 이내"
    elif distance<3000:
        distance_text = "3KM 이내"
    elif distance<5000:
        distance_text = "5KM 이내"
    elif distance<10000:
        distance_text = "10KM 이내"
    elif distance<15000:
        distance_text = "15KM 이내"
    else:
        distance_text = "15KM 초과"
    
    return distance_text


#===========================================sytle 영역

    
# 버튼 style
m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        width:75%;
        display: inline-block;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap; 
        align="center";
        float: mid;
        background-color: rgb(239, 198, 56);
        color: black;
        font-size;50%;
        font-weight: bold;

    }
    div.stButton > button:first-child {
            cursor: pointer;
            transition: all .2s ease-in-out;
        }
    div.stButton > button:first-child:hover {
            transform: scale(1.03);
            border: 3px solid gold;
    </style>""", unsafe_allow_html=True)

# 배경 style

def add_bg_from_url(url):
    
    if url=="default":
        st.markdown( f"""
                    <style> .stApp {{
                    background-color: rgb(43, 16, 59);
                    background-size: cover; }}
                    </style>
                    """, unsafe_allow_html=True )
    else:
        st.markdown( f"""
                    <style> .stApp {{ background-image:
                    url({url}); 

                    background-size: cover; }}
                    </style>
                    """, unsafe_allow_html=True )

# url =  "https://us.123rf.com/450wm/patthana/patthana1803/patthana180300058/97378454-%EC%B6%94%EC%83%81-%EB%B8%94%EB%A3%A8-%ED%86%A4-%EC%BB%AC%EB%9F%AC-%EB%8B%A4%EA%B0%81%ED%98%95-%EC%82%BC%EA%B0%81%ED%98%95-%EB%B0%B0%EA%B2%BD-%EB%B2%A1%ED%84%B0-%EC%9D%BC%EB%9F%AC%EC%8A%A4%ED%8A%B8-%EB%A0%88%EC%9D%B4-%EC%85%98.jpg?ver=6"

# 배경 초기화
add_bg_from_url("default") 

# =========================================이미지 hover 적용
st.markdown(
    """
    <style>
    img {
        cursor: pointer;
        transition: all .2s ease-in-out;
        width: 95%;
        height: 95%;
        margin: auto;
    }
    img:hover {
        transform: scale(1.05);
        border: 3px solid gold;
        border-radius: 7px;
        -moz-border-radius: 7px;
        -khtml-border-radius: 7px;
        -webkit-border-radius: 7px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


#===============================================
# session 값 초기화
# vector list
if 'selected_list' not in st.session_state:
    st.session_state['selected_list'] = []
    
if 'selected_restraunt' not in st.session_state:
    st.session_state['selected_restraunt'] = []
# 위치 값 가져오기
curr_location = getLocation()

# selected_list session 불러오기

# selected_restraunt session 불러오기
selected_restraunt = st.session_state['selected_restraunt'][:3]
st.session_state['selected_restraunt'] = selected_restraunt

with st.container():

    nyamnyam_html = """
    <h1 style=text-align:center; >
    세상의 모든 맛집! Nyam-Nyam! 
    </h1>
    """
    st.markdown(nyamnyam_html, unsafe_allow_html=True)

    st.markdown("---")

    # 검색범위 슬라이더
    radius_html = """
    <h4 style=text-align:center; >
    탐색 반경을 설정해주세요<span style="font-size: 20px;">  (단위:m)</span></h4>

    """
    st.markdown(radius_html, unsafe_allow_html=True)
    
    radius = st.slider("radius_slider",min_value=1500,max_value=30000,value=10000,label_visibility="hidden")
    st.markdown("---")

    # 데이터 불러오기
    all_data = pd.read_csv("all_data.csv")
    print(st.session_state['selected_list'])
    all_data = getRestaurant(all_data,curr_location['latitude'], curr_location['longitude'], radius, st.session_state['selected_list'])
    # all_data = getRestaurant(all_data,37.541, 126.986, radius, st.session_state['selected_list'])

    # 내 주변 맛집 주요키워드 출력
    keyword_list = []
    for idx in range(len(all_data['comment'])):
        for vector in literal_eval(all_data['comment'].iloc[idx])[:2]:
            if vector not in keyword_list:
                keyword_list.insert(0,vector)
            
    keyword_list_length = len(keyword_list)
    keyword_list = sorted(list(set(keyword_list)))


    
    main_keywords_html = """
    <h4 style=text-align:center; >
    주변 맛집 주요 키워드
    </h4>
    """
    st.markdown(main_keywords_html, unsafe_allow_html=True)


    selected_restraunt = st.session_state["selected_restraunt"]

    st.markdown("---")
    col1,col2,col3,col4 =st.columns(4)
    for idx, keyword in enumerate(keyword_list):
        keyword = "  "+keyword+"  "
        if idx%4 == 0:
            if col1.button(f'{keyword}'):
                if keyword not in st.session_state['selected_list']:    
                    st.session_state['selected_list'].insert(0,keyword)
        elif idx%4 == 1:
            if col2.button(f'{keyword}'):
                if keyword not in st.session_state['selected_list']:  
                    st.session_state['selected_list'].insert(0,keyword)
        elif idx%4 == 2:
            if col3.button(f'{keyword}'):
                if keyword not in st.session_state['selected_list']:  
                    st.session_state['selected_list'].insert(0,keyword)
        elif idx%4 == 3:
            if col4.button(f'{keyword}'):
                if keyword not in st.session_state['selected_list']:  
                    st.session_state['selected_list'].insert(0,keyword)


    


    st.markdown("---")

    title_html = """
    <h1 style=text-align:center; >
    내 주변 맛집
    </h1>
    """
    st.markdown(title_html, unsafe_allow_html=True)



    for id, idx in enumerate(range(len(all_data))):
        
        st.markdown("<hr style=height: 3px;>", unsafe_allow_html=True)
        name = all_data['name'].iloc[idx]
        road_address = all_data['road_address'].iloc[idx]
        distance = all_data['distance'].iloc[idx]
        img = all_data['img_url'].iloc[idx]
        comment = all_data['comment'].iloc[idx]
        cola, colb = st.columns(2)   
        
        # 가게명 html
        name_html = f"""
        <h2 style=text-align:center;  >
        {name}
        </h2>
        """
        # 주소 html
        road_address_html = f"""
        <h6 style=text-align:center;  >
        {road_address}
        </h6>
        """
        # 거리를 텍스트로 변환
        distance_text = distance_to_text(distance)
        distance_text_html = f"""
        <h1 style=text-align:center;  >
        {distance_text}
        </h1>
        """
        
        cola.markdown(name_html, unsafe_allow_html=True)
        cola.markdown(road_address_html, unsafe_allow_html=True)
        colb.markdown(distance_text_html, unsafe_allow_html=True)

        st.image(img)
        col1_add,col2_add,col3_add,col4_add =st.columns(4)
        for idx,keyword in enumerate(literal_eval(comment)[:4]):
            # 버튼 고유값 생성(중복시 오류)
            button_keyword = "  "+keyword+"  "+" "*(id+1)

            if idx%4 == 0:
                if col1_add.button(button_keyword):
                    if keyword not in st.session_state['selected_list']:
                        st.session_state['selected_list'].insert(0,keyword)
            elif idx%4 == 1:
                if col2_add.button(button_keyword):
                    if keyword not in st.session_state['selected_list']:
                        st.session_state['selected_list'].insert(0,keyword)
            elif idx%4 == 2:
                if col3_add.button(button_keyword):
                    if keyword not in st.session_state['selected_list']:
                        st.session_state['selected_list'].insert(0,keyword)             
            elif idx%4 == 3:
                if col4_add.button(button_keyword):
                    if keyword not in st.session_state['selected_list']:
                       st.session_state['selected_list'].insert(0,keyword)          
                    
        st.markdown("---")
        name_insta = parse.quote(name)
        name_etc = parse.quote(name+" 맛집")
        
        detail, col_button1, col_button2, col_button3, button_all =st.columns([0.2,0.1,0.1,0.1,0.5])
        
        detail_text= """
                    <h5 style="text-align:right;" >
                    링크 바로가기
                    </h5>
                    """
        
        detail.markdown(detail_text,unsafe_allow_html=True)        
        
        button1= f"""
            <a type ='button' class="first"   href="https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query={name_etc}" target='_blank'>
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQb93sjSI5hrWVQzD3NoQ1fU3M3xQtWPKACw&usqp=CAU" style = "border-radius: 30%; overflow: hidden;  width: 100%; height:100%;"/>
            </a>"""
        
        col_button1.markdown(button1,unsafe_allow_html=True)
        
        button2= f"""
            <a type ='button' class="second"   href="https://www.instagram.com/explore/tags/{name_insta}/" target='_blank'>
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Instagram_logo_2022.svg/1200px-Instagram_logo_2022.svg.png" style = "border-radius: 30%; overflow: hidden; width: 100%; height:100%;"/>
            </a>"""
        
        col_button2.markdown(button2,unsafe_allow_html=True)
        
        button3= f"""
            <a type ='button' class="third"   href="https://www.youtube.com/results?search_query={name_etc}" target='_blank'>
            <img src="https://w7.pngwing.com/pngs/447/350/png-transparent-iphone-youtube-computer-icons-logo-youtube-logo-electronics-sign-mobile-phones.png" style = "border-radius: 30%; overflow: hidden; width: 100%; height: 100%;" />
            </a>"""
        
        col_button3.markdown(button3,unsafe_allow_html=True)
        
        if button_all.button(name+"과/와 비슷한 맛집 찾기!"):
            for keyword_vector in random.sample(literal_eval(comment)[:10],5):
                if keyword_vector not in st.session_state['selected_list']:
                    st.session_state['selected_list'].insert(0,keyword_vector)

            selected_restraunt.insert(0,[name,img,road_address])
            # 중복 확인
            selected_restraunt = list(set([str(ls) for ls in selected_restraunt]))
            # str을 다시 list로
            selected_restraunt = [literal_eval(i) for i in selected_restraunt]
            

    st.sidebar.header("내가 선택한 키워드")
    st.sidebar.text("최대 10개까지만 저장됩니다.")
    st.sidebar.multiselect("selected_list",
                            st.session_state['selected_list'],
                            st.session_state['selected_list'],label_visibility="hidden")

    st.sidebar.header("내가 선택한 식당")
    st.sidebar.text("최대 3개까지만 저장됩니다.")
    # selected_restraunt session 불러오기
    selected_restraunt = st.session_state['selected_restraunt'][:3]
    st.session_state['selected_restraunt'] = selected_restraunt
    
    for restraunt in selected_restraunt:
        name_side_value = restraunt[0]
        img_side_value = restraunt[1]
        road_address_side_value = restraunt[2]
        
        # 컨테이너 초기화
        selected_restraunt_side = st.empty()
        
        with selected_restraunt_side.container():
            name_side =st.sidebar.subheader(name_side_value)
            road_address_side = st.sidebar.text(road_address_side_value)
            img_side = st.sidebar.image(img_side_value)
            
        if st.sidebar.button(f"{name_side_value}_삭제",key=f"{name_side_value}_삭제"):
            selected_restraunt_side.empty()
        

            
