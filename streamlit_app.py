import streamlit as st
import numpy as np
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

# title
st.title('Persona Route - Jeju Island')

# header
st.write('Hello, *World!* :sunglasses:')

client_id = "262649bc897c4329b00de59ca0f039a5"
client_secret = "32c47244efc24d9f9ba33ce18e40f0fd"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

st.title("Spotify 노래 검색")
search_query = st.text_input("노래 검색")

selected_songs_features = []

if st.button("검색"):
    results = sp.search(q=search_query, type='track')
    tracks = results['tracks']['items']

    if tracks:
        st.subheader("검색 결과")

        for i, track in enumerate(tracks):
            st.write(f"**{track['name']}** by {track['artists'][0]['name']}")
            
            if track['album']['images']:
                album_image_url = track['album']['images'][0]['url']
                st.image(album_image_url, caption='Album Image', width=200)
            
            st.write(f"Listen on Spotify: [Link]({track['external_urls']['spotify']})")
            
            if st.button(f"Select {track['name']}_{i}"):
                st.write(f"Selected Track: **{track['name']}** by {track['artists'][0]['name']}")
                st.image(album_image_url, caption='Album Image', width=400)
                st.write(f"Listen on Spotify: [Link]({track['external_urls']['spotify']})")
                st.write("---")
                
            st.write("---") 
    else:
        st.warning("검색 결과가 없습니다.")

# map으로 표시하는 방법
#지도 위에 표시될 점 좌표 값을 위도경도에 담습니다 .
base_position =  [37.5073423, 127.0572734]
#중심점의 위도, 경도 좌표를 리스트에 담습니다.

# base_position에, 랜덤으로 생성한 값을 더하여 5개의 좌표를 데이터 프레임으로 생성하였고,
# 컬럼명은 위도 :lat  경도 lon으로 지정하였습니다. 


map_data = pd.DataFrame(
    np.random.randn(5, 1) / [20, 20] + base_position , 
    columns=['lat', 'lon'])
# map data 생성 : 위치와 경도 

print(map_data)

# google big query 연결("https://docs.streamlit.io/knowledge-base/tutorials/databases/gcs")