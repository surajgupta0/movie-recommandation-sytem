import pickle as pkl
import numpy as np
import pandas as pd
import streamlit as st
from pinecone import Pinecone
import requests

with open('movie.pkl', 'rb') as movie_file:
    movie_data = pkl.load(movie_file)


movie_data = pd.DataFrame(movie_data)

pc = Pinecone(api_key="pcsk_28BYaV_271pDGPxzVmbyU4io4GriUoX7sYjNseGoYH7iZpUjgcSHXBoxdNKi8CKwCLgLvi")

index = pc.Index("movie-recommandation")

def recommend_movie(title):
    Li = []
    
    movie_index = movie_data[movie_data['title'] == title].index[0]
    movies_list = index.query(id=str(movie_index), top_k=6).matches
    
    count = 0
    for i in movies_list:
        mv_id = movie_data.iloc[int(i.id)]['id']
        url = f"https://api.themoviedb.org/3/movie/{mv_id}?api_key=d9c7af84b1594e65459170798ff20a2d"
        response = requests.get(url)
        data = response.json()
        if count < 5 and data.get('title'):
            Li.append(data)
            count += 1
            if count == 5:
                break
    return Li

st.title('Movie Recommadation System')
selected_movie = st.selectbox('Select a movie', movie_data['title'])

if st.button('Recommend'):
    recommendations = recommend_movie(selected_movie)
    st.write('Recommended Movies:')
    count = 0
    cols = st.columns(5)  # Create 5 columns for the top 5 recommendations
    
    for data in recommendations:
        
        poster_url = "https://image.tmdb.org/t/p/w780"
        if data.get('belongs_to_collection') and data['belongs_to_collection']['poster_path']:
            poster_url += data['belongs_to_collection']['poster_path']
        elif data.get('poster_path'):
            poster_url += data['poster_path']   
        movie_title = data['title']
        release_date = data['release_date']
        overview = data['overview']
        
        print(cols)
        with cols[count]:
            st.image(poster_url, width=150)
            st.markdown(f"<h6>{movie_title}</h6>", unsafe_allow_html=True)
        count += 1
        
        


