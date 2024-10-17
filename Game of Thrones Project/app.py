import streamlit as st # type: ignore
import pickle
import requests # type: ignore
import numpy as np # type: ignore

# Fetch character data from Thrones API
api_data = requests.get("https://thronesapi.com/api/v2/Characters").json()

# Load your local dataframe
df = pickle.load(open('data.pkl', 'rb'))
df = df.head(25)

# Clean up character names
df['character'] = df['character'].str.replace('Jaime', 'Jamie')
df['character'] = df['character'].str.replace('Lord Varys', 'Varys')
df['character'] = df['character'].str.replace('Bronn', 'Lord Bronn')
df['character'] = df['character'].str.replace('Sandor Clegane', 'The Hound')
df['character'] = df['character'].str.replace('Robb Stark', 'Rob Stark')

# Function to fetch character image from the API
def fetch_image(name, api_data):
    for item in api_data:
        if item['fullName'] == name:
            return item['imageUrl']
    return None  # Return None if the character is not found

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
        st.text("Image not available")

with col2:
    st.header(recommended_character)
    if recommended_character_image_url:
        st.image(recommended_character_image_url)
    else:
        st.text("Image not available")
