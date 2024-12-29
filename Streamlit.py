import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# Load dataset
dataset = pd.read_csv('data/processed_series_data.csv')

# Prepare TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(dataset['text'])

# Define search function
def search(query, top_n=10):
   query_vec = vectorizer.transform([query])
   scores = cosine_similarity(query_vec, tfidf_matrix).flatten()
   top_indices = scores.argsort()[-top_n:][::-1]
   return dataset.iloc[top_indices].assign(score=scores[top_indices]), scores[top_indices]

# Streamlit app configuration
st.set_page_config(page_title="Series Search App", layout="wide")

# Custom CSS for dark theme with white headers and overview text
st.markdown(
    """
    <style>
        body {
            background-color: black;
            color: white;
        }
        .stApp {
            background-color: black;
        }
        .stTextInput>div>div>input {
            background-color: #333;
            color: white;
            border: 1px solid #555;
        }
        .stTextInput>div>div>input::placeholder {
            color: #bbb;
        }
        .stButton>button {
            background-color: #333;
            color: white;
            border: 1px solid #555;
        }
        .stButton>button:hover {
            background-color: #555;
        }
        .search-container {
            margin-top: 20px;
        }
        .result-container {
            background-color: #1e1e1e;
            padding: 10px;
            margin-bottom: 15px;
            border-radius: 8px;
            display: flex;
            align-items: center;
        }
        .result-container img {
            width: 80px;
            height: auto;
            margin-right: 15px;
            border-radius: 5px;
        }
        .result-container strong {
            font-size: 16px;
            color: #ffcc00;
        }
        .result-container span {
            color: white !important;
        }
        .result-container a {
            color: #1e90ff;
        }
        .result-container a:hover {
            color: #ff4500;
        }
        .attribution {
            margin-top: 20px;
            font-size: 14px;
            color: #bbb;
            text-align: center;
        }
        .attribution a {
            color: #1e90ff;
        }
        .attribution a:hover {
            color: #ff4500;
        }
        h1, h2, h3 {
            color: white !important;
        }
        label {
            color: white !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# App title
st.title("Series Search App")

# Input for user query
query = st.text_input("Enter what you're searching for:", placeholder="Search for a series by title, keyword, or description...")

# Search and display results
if query:
    results, scores = search(query)

    if not results.empty:
        st.subheader("Search Results")

        for _, row in results.iterrows():
            # Format result
            name = row['name']
            overview = row['overview']
            slug_url = f"https://thetvdb.com/series/{row['slug']}"
            image_url = f"https://thetvdb.com{row['image']}" if pd.notna(row['image']) and row['image'].strip() else None
            score = row['score']

            if image_url:
                image_tag = f"<img src=\"{image_url}\" alt=\"{name}\">"
            else:
                image_tag = f"<div style=\"width: 80px; height: auto; margin-right: 15px; background-color: #555; display: flex; justify-content: center; align-items: center; color: white; font-size: 12px;\">{name}</div>"

            st.markdown(
                f"""
                <div class="result-container">
                    {image_tag}
                    <div>
                        <strong>{name}</strong><br>
                        <span>{overview}</span><br>
                        <span>Score: {score:.2f}</span><br>
                        <a href="{slug_url}" target="_blank">Click here for more details</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No results found. Please try a different query.")

    # Attribution section
    st.markdown(
        """
        <div class="attribution">
            Metadata provided by <a href="https://thetvdb.com/subscribe" target="_blank">TheTVDB</a>. 
            Please consider adding missing information or subscribing.
        </div>
        """,
        unsafe_allow_html=True
    )