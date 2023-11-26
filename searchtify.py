import streamlit as st
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

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
        
        
        
