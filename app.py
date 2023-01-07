import streamlit as st
import pandas as pd
import pickle
import re
from tqdm import tqdm
from ast import literal_eval
from main import getLocation, getNearRestaurant
from streamlit.components.v1 import html
from urllib import parse
from streamlit_javascript import st_javascript

#TODO streamlit viewport 문제 mobile responsive

#=========================================== config 영역
MAX_VECTORS = 8


st.set_page_config(
    page_title="모든 맛집이 내 손안에! 냠냠"
  )

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
        font-weight: 900;

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
if 'selected_list' not in st.session_state:
    st.session_state['selected_list'] = []
# 위치 값 가져오기
curr_location = getLocation()



# 검색범위 슬라이더
st.subheader("검색 범위")
radius = st.slider("radius_slider",min_value=1000,max_value=50000,value=1500,label_visibility="hidden")
st.markdown("---")

# 데이터 불러오기
all_data = pd.read_csv("all_data.csv")
all_data = getNearRestaurant(all_data,curr_location['latitude'], curr_location['longitude'],radius)

# 내 주변 맛집 주요키워드 출력
keyword_list = []
for idx in range(len(all_data['comment'])):
    for vector in literal_eval(all_data['comment'].iloc[idx])[:2]:
        keyword_list.append(vector)
keyword_list = sorted(list(set(keyword_list)))

st.subheader("주변 맛집 주요 키워드")


selected_list = st.session_state["selected_list"]

col1,col2,col3,col4 =st.columns(4)
for idx, keyword in enumerate(keyword_list):
    keyword = "  "+keyword+"  "
    keyword = keyword[:10]
    if idx%4 == 0:
        if col1.button(f'{keyword}'):
            selected_list.append(keyword)
            selected_list = list(set(selected_list))
    elif idx%4 == 1:
        if col2.button(f'{keyword}'):
            selected_list.append(keyword)
            selected_list = list(set(selected_list))
    elif idx%4 == 2:
        if col3.button(f'{keyword}'):
            selected_list.append(keyword)
            selected_list = list(set(selected_list))
    elif idx%4 == 3:
        if col4.button(f'{keyword}'):
            selected_list.append(keyword)
            selected_list = list(set(selected_list))


        


st.markdown("---")

html = """
<h2 >
내 주변 맛집
</h2>
"""
st.markdown(html, unsafe_allow_html=True)



for id, idx in enumerate(range(len(all_data))):
    name = all_data['name'].iloc[idx]
    road_address = all_data['road_address'].iloc[idx]
    distance = all_data['distance'].iloc[idx]
    img = all_data['img_url'].iloc[idx]
    comment = all_data['comment'].iloc[idx]
    st.markdown("---")
    cola, colb = st.columns(2)   
    name_html = f"""
    <h2 style=text-align:center;>
    {name}
    </h2>
    
    """
    
    cola.markdown(name_html, unsafe_allow_html=True)
    colb.subheader(road_address)
    colb.subheader(f"{distance}m")
    st.image(img)
    col1_add,col2_add,col3_add,col4_add =st.columns(4)
    for idx,keyword in enumerate(literal_eval(comment)[:4]):
        # 버튼 고유값 생성(중복시 오류)
        button_keyword = "  "+keyword+"  "+" "*(id+1)

        if idx%4 == 0:
            if col1_add.button(button_keyword):
                selected_list.append(keyword)
                selected_list = list(set(selected_list))
        elif idx%4 == 1:
            if col2_add.button(button_keyword):
                selected_list.append(keyword)
                selected_list = list(set(selected_list))
        elif idx%4 == 2:
            if col3_add.button(button_keyword):
                selected_list.append(keyword)
                selected_list = list(set(selected_list))
        elif idx%4 == 3:
            if col4_add.button(button_keyword):
                selected_list.append(keyword)
                selected_list = list(set(selected_list))
    name_insta = parse.quote(name)
    name_etc = parse.quote(name+" 맛집")
    
    _,_,_,_,_,_,_,col_button1, col_button2, col_button3 =st.columns(10)
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
            
            
            
            
            
            
            
st.sidebar.header("내가 선택한 키워드")
st.sidebar.multiselect("selected_list",
                selected_list,
                selected_list,label_visibility="hidden")
st.sidebar.image("https://www.shutterstock.com/ko/blog/wp-content/uploads/sites/17/2018/02/101-Color-Combinations-STTK-Post-update12.jpg?w=760&h=537")
        
