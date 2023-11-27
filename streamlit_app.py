import streamlit as st
import numpy as np
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import folium
import base64
from streamlit_folium import st_folium
import xyzservices
import xyzservices.providers as xyz
from itertools import permutations

# title
st.title(':musical_note: Persona Route - Jeju Island :airplane:')

# spotify client id
client_id = "262649bc897c4329b00de59ca0f039a5"
client_secret = "32c47244efc24d9f9ba33ce18e40f0fd"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# step 1: music finder
st.header("Step :one:")
st.subheader(":musical_score: Spotify 노래 검색")
col1, col2, col3 = st.columns(3)

## find music1 ------------------------------------------------------
selected_track_title1 = ''
selected_track1 = None

with col1: 
    prev_qry1 = ""
    search_query1 = st.text_input("노래 검색", key=4)

    if st.button("검색", key=1) or (prev_qry1 != search_query1):
        prev_qry1 = search_query1
        results = sp.search(q=search_query1, type='track')
        tracks = results['tracks']['items']

        container1 = st.empty()

        if tracks:
            container1.subheader("검색 결과")
            track_list = []
            track_title_list = []

            for i, track in enumerate(tracks):
                track_list.append(track)
                track_title_list.append(f"{i}. {track['name']} - {track['artists'][0]['name']}")
                
                if track['album']['images']:
                     album_image_url = track['album']['images'][0]['url']
                
            selected_track_title1 = st.radio('Select', track_title_list)
            selected_track1 = track_list[int(selected_track_title1[0])]
            
        else:
            st.warning("검색 결과가 없습니다.")


## find music2 ------------------------------------------------------

selected_track_title2 = ''
selected_track2 = None

with col2: 
    prev_qry2 = ""
    search_query2 = st.text_input("노래 검색", key=5)

    if st.button("검색", key=2) or (prev_qry2 != search_query2):
        prev_qry2 = search_query2
        results = sp.search(q=search_query2, type='track')
        tracks = results['tracks']['items']

        container2 = st.empty()

        if tracks:
            container2.subheader("검색 결과")
            track_list = []
            track_title_list = []

            for i, track in enumerate(tracks):
                track_list.append(track)
                track_title_list.append(f"{i}. {track['name']} - {track['artists'][0]['name']}")
                
                if track['album']['images']:
                     album_image_url = track['album']['images'][0]['url']
                
            selected_track_title2 = st.radio('Select', track_title_list)
            selected_track2 = track_list[int(selected_track_title2[0])]
            
        else:
            st.warning("검색 결과가 없습니다.")

## find music3 ------------------------------------------------------

selected_track_title3 = ''
selected_track3 = None

with col3: 
    prev_qry3 = ""
    search_query3 = st.text_input("노래 검색", key=6)

    if st.button("검색", key=3) or (prev_qry3 != search_query3):
        prev_qry3 = search_query3
        results = sp.search(q=search_query3, type='track')
        tracks = results['tracks']['items']

        container3 = st.empty()

        if tracks:
            container3.subheader("검색 결과")
            track_list = []
            track_title_list = []

            for i, track in enumerate(tracks):
                track_list.append(track)
                track_title_list.append(f"{i}. {track['name']} - {track['artists'][0]['name']}")
                
                if track['album']['images']:
                     album_image_url = track['album']['images'][0]['url']
                
            selected_track_title3 = st.radio('Select', track_title_list)
            selected_track3 = track_list[int(selected_track_title3[0])]
            
        else:
            st.warning("검색 결과가 없습니다.")


# show selected music

col4, col5, col6 = st.columns(3)

with col4:
    if selected_track1 != None:
        album_image_url = selected_track1['album']['images'][0]['url']
        st.image(album_image_url, width=200)
        st.write(selected_track_title1[2:])

with col5:
    if selected_track2 != None:
        album_image_url = selected_track2['album']['images'][0]['url']
        st.image(album_image_url, width=200)
        st.write(selected_track_title2[2:])

with col6:
    if selected_track3 != None:
        album_image_url = selected_track3['album']['images'][0]['url']
        st.image(album_image_url, width=200)
        st.write(selected_track_title3[2:])

# bring selected music properties -> calculate mean

# predict travel spot from mean

# step 2 : show travel spot using checkbox

# bring travel spot selected 

# step 3: draw map
def findShortestPath(dists, num_selected):
    permutation_list = list(permutations(range(num_selected)))
    st.write(permutation_list)
    shortest_dist = 99999
    shortest_path = []

    for permutation in permutation_list:
        dist = 0
        for i in range(num_selected - 1):
            dist += dists[permutation[i]][permutation[i+1]]
        if dist < shortest_dist:
            shortest_dist = dist
            shortest_path = permutation

    return shortest_dist, shortest_path 

st.header("Step :three:")
st.subheader(":map: Persona Route")

m = folium.Map(location=[33.375000, 126.55000], min_zoom=9, zoom_start=10, min_lat= 33, max_lat = 33.7, min_lon = 126, max_lon = 127.1, max_bounds=True)
points = pd.read_csv('coordinates.csv', header=0, index_col=0)

selected_places = ['민속자연사박물관', '해녀박물관', '서핑', '보롬왓', '서바이벌 게임']
num_selected = len(selected_places)
selected_coords = []
dists = [[99999]*num_selected for _ in range(num_selected)]


for place in selected_places:
    place_coord = [points.loc[place][0], points.loc[place][1]]
    
    # pic = base64.b64encode(open('smu.jpg','rb').read()).decode()
    # image_src = 'https://lh7-us.googleusercontent.com/acGpfQjQDFnOdZ_EJgHQQRrfQSBz8CYDfxc9jJbvwbw1GWg0189XiJ6Lb2kKuu_hvFXu1rZDOePSK668vRQ_LiDajAgRn61U4fgPbQEVZO9yckX0WYEVihqyCR86oNilPaZt-NEiDoCff4geZpc40wXR_FREew'
    # image_tag = '<img src="' + image_src +'">'.format(pic)
    # iframe = folium.IFrame(image_tag, width=300, height=300)
    # popup = folium.Popup(iframe, max_width=650)
    
    folium.Marker(place_coord, tooltip=place, icon=folium.Icon(color='beige')).add_to(m)
    selected_coords.append(place_coord)

for i in range(num_selected):
    for j in range(i):
        dists[i][j] = ((selected_coords[i][0] - selected_coords[j][0]) ** 2 + (selected_coords[i][1] - selected_coords[j][1]) ** 2) ** 0.5
        dists[j][i] = dists[i][j]

shortest_dist, shortest_path_i = findShortestPath(dists, num_selected)

shortest_path_coords = []

for i in shortest_path_i:
    shortest_path_coords.append(selected_coords[i])


folium.PolyLine(shortest_path_coords).add_to(m)

st_data = st_folium(m, width=700, height=500)

col1, col2, col3 = st.columns(3)
with col1:
    st.write(shortest_dist)
with col2:
    st.write(2)
with col3:
    st.write(3)

st.write(points)
