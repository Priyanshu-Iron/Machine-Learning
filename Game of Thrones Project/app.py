import streamlit as st # type: ignore
import pickle
import requests # type: ignore
import numpy as np # type: ignore
import pandas as pd # type: ignore
import os

# Load your local dataframe
if os.path.exists('data.pkl'):
    df = pickle.load(open('data.pkl', 'rb'))
    df = df.head(25)
else:
    st.error("data.pkl file not found")
    st.stop()

# Clean up character names
df['character'] = df['character'].str.replace('Jaime', 'Jamie')
df['character'] = df['character'].str.replace('Lord Varys', 'Varys')
df['character'] = df['character'].str.replace('Bronn', 'Lord Bronn')
df['character'] = df['character'].str.replace('Sandor Clegane', 'The Hound')
df['character'] = df['character'].str.replace('Robb Stark', 'Rob Stark')

# Fetch character data from Thrones API
@st.cache_data
def get_api_data():
    try:
        response = requests.get("https://thronesapi.com/api/v2/Characters")
        if response.status_code == 200:
            return response.json()
        else:
            st.warning(f"API request failed with status code: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error fetching API data: {e}")
        return []

# Function to fetch character image from the API
def fetch_image(name, api_data):
    for item in api_data:
        if item['fullName'].lower() == name.lower() or name.lower() in item['fullName'].lower():
            return item['imageUrl']
    return None  # Return None if the character is not found

# Get API data
api_data = get_api_data()

# Streamlit app title
st.title("Game Of Thrones Personality Matcher")

# List of characters from the dataframe
characters = df['character'].values

# Dropdown to select a character
selected_character = st.selectbox("Select a character", characters)

# Fetch closest match using Euclidean distance
character_id = np.where(df['character'].values == selected_character)[0][0]
x = df[['x', 'y']].values

distances = []
for i in range(len(x)):
    distances.append(np.linalg.norm(x[character_id] - x[i]))

recommended_id = sorted(list(enumerate(distances)), key=lambda x: x[1])[1][0]
recommended_character = df['character'].values[recommended_id]

# Fetch images for the selected and recommended characters
image_url = fetch_image(selected_character, api_data)
recommended_character_image_url = fetch_image(recommended_character, api_data)

# Display the selected character and the recommended character
col1, col2 = st.columns(2)

with col1:
    st.header(selected_character)
    if image_url:
        st.image(image_url)
    else:
        st.text(f"Image not available for {selected_character}")

with col2:
    st.header(f"Most similar: {recommended_character}")
    if recommended_character_image_url:
        st.image(recommended_character_image_url)
    else:
        st.text(f"Image not available for {recommended_character}")

# Add similarity score
similarity = 1 - (distances[recommended_id] / max(distances))
st.info(f"Similarity score: {similarity:.2%}")

# Add character traits explanation
st.subheader("Why these characters match:")
st.write("""
This recommendation is based on personality trait similarity in a 2D space where:
- X-axis represents traits like honor vs pragmatism
- Y-axis represents traits like compassion vs ruthlessness

Characters positioned close to each other in this space have similar personality traits.
""")