import streamlit as st
import geocoder
import pandas as pd
import pickle
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
file_path = "all_data.pkl"
print("dasdasd")
content = read_file(bucket_name, file_path)


# Print results.
for line in content.strip().split("\n"):
    name, pet = line.split(",")
    st.write(f"{name} has a :{pet}:")

# # load
# with open('data.pickle', 'rb') as f:
#     data = pickle.load(f)
