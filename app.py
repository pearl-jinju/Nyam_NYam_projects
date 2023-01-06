import streamlit as st
import geocoder
import pandas as pd
import pickle
import re
from tqdm import tqdm
from ast import literal_eval

MAX_VECTORS = 8
# g = geocoder.ip('me')

# g  = g.latlng
# latitude = g[0]
# longitude = g[1]
# st.write(f"{latitude}:{longitude}")


# streamlit_app.py

from google.oauth2 import service_account
from google.cloud import storage

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = storage.Client(credentials=credentials)

# Retrieve file contents.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
@st.experimental_memo(ttl=600)
def read_file(bucket_name, file_path):
    bucket = client.bucket(bucket_name)
    content = bucket.blob(file_path).download_as_string().decode("utf-8")
    return content

bucket_name = "streamlit-bucket-nyamnyam"
file_path = "all_data.csv"
content = read_file(bucket_name, file_path)

# Print results.
result_df = pd.DataFrame(columns=['theme_id', 'restaurant_id', 'name', 'road_address', 'phone_number','latitude','longitude','rating','img_url','comment'])
for cnt, line in tqdm(enumerate(content.strip().split("\n"))):
    if cnt == 0:
        continue
    line = re.sub(r"\s","",line) 
    idx, theme_id, restaurant_id, name, road_address, phone_number,latitude,longitude,rating,img_url,comment = line.split(",",maxsplit=10)
    comment = re.sub(r"'","",comment)
    comment = literal_eval(comment)[1:-1].split(",")[:MAX_VECTORS]

    temp_df = pd.DataFrame([[theme_id, restaurant_id, name, road_address, phone_number,latitude,longitude,rating,img_url,comment]])
    temp_df.columns = ['theme_id', 'restaurant_id', 'name', 'road_address', 'phone_number','latitude','longitude','rating','img_url','comment']
    result_df = pd.concat([result_df,temp_df])



print(result_df)

    # theme_id,restaurant_id,name,road_address,phone_number,latitude,longitude,rating,img_url,comment = line.split(",")
    
    # st.write(f"{theme_id}:{restaurant_id}:{name}:{road_address}:{phone_number}:{latitude}:{longitude}:{rating}:{img_url}:{comment}:")

# # load
# with open('data.pickle', 'rb') as f:
#     data = pickle.load(f)
