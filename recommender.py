import os
import urllib.request
import zipfile
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings

warnings.filterwarnings('ignore')

DATA_URL = "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
ZIP_FILE = "ml-latest-small.zip"
DATA_DIR = "ml-latest-small"

def download_and_extract_data():
    """Downloads the MovieLens dataset if it doesn't already exist."""
    if not os.path.exists(DATA_DIR):
        print("Downloading MovieLens dataset. This might take a moment...")
        urllib.request.urlretrieve(DATA_URL, ZIP_FILE)
        print("Extracting dataset...")
        with zipfile.ZipFile(ZIP_FILE, 'r') as zip_ref:
            zip_ref.extractall(".")
        print("Extraction complete.")
    else:
        print("Dataset already exists.")

class MovieRecommender:
    def __init__(self):
        self.movies_df = None
        self.similarity_matrix = None
        self.download_data()
        self.train_model()

    def download_data(self):
        download_and_extract_data()

    def train_model(self):
        print("Training recommendation model...")
        # Load the movies dataset
        movies_path = os.path.join(DATA_DIR, "movies.csv")
        self.movies_df = pd.read_csv(movies_path)
        
        # We will use the 'genres' column for our content-based recommendation.
        # Genres are pipe separated (e.g., Adventure|Animation|Children|Comedy|Fantasy).
        # We replace the pipe with a space to make it look like a sentence of tags.
        self.movies_df['genres'] = self.movies_df['genres'].str.replace('|', ' ')
        
        # Initialize CountVectorizer that will convert genres into a matrix of token counts
        count_vectorizer = CountVectorizer()
        genre_matrix = count_vectorizer.fit_transform(self.movies_df['genres'])
        
        # Calculate Cosine Similarity
        self.similarity_matrix = cosine_similarity(genre_matrix, genre_matrix)
        print("Model training complete.")

    def recommend(self, movie_title, num_recommendations=5):
        try:
            # Find the index of the movie in the dataframe
            # Using str.contains to match even if the user doesn't write the exact year
            idx_list = self.movies_df[self.movies_df['title'].str.contains(movie_title, case=False, na=False)].index.tolist()
            if not idx_list:
                return f"Movie '{movie_title}' not found in the dataset."
            
            idx = idx_list[0]
            exact_title = self.movies_df.iloc[idx]['title']
            print(f"Movies similar to: {exact_title}")
            
            # Get the pairwise similarity scores of all movies with that movie
            sim_scores = list(enumerate(self.similarity_matrix[idx]))
            
            # Sort the movies based on the similarity scores in descending order
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            
            # Get the scores of the most similar movies (skipping the first one, which is the movie itself)
            sim_scores = sim_scores[1:num_recommendations+1]
            
            # Get the movie indices
            movie_indices = [i[0] for i in sim_scores]
            
            # Return the top most similar movies
            recommendations = self.movies_df.iloc[movie_indices][['title', 'genres']].reset_index(drop=True)
            return recommendations
            
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == "__main__":
    print("Initializing Movie Recommendation System...")
    recommender = MovieRecommender()
    
    print("\n--- Testing Recommendations ---")
    recommendation_queries = ["Toy Story", "Batman", "Matrix", "Pulp Fiction"]
    
    for query in recommendation_queries:
        print("\n---------------------------------------------------------")
        result = recommender.recommend(query)
        print(result)
    
    print("\n---------------------------------------------------------")
    print("Setup complete! You can copy this code and use it in your Jupyter notebook or web app.")
