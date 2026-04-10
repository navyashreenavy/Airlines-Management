from flask import Flask, render_template, request
from recommender import MovieRecommender

app = Flask(__name__)

# Initialize the recommender once when the app starts
print("Initializing the ML Recommendation Engine...")
recommender = MovieRecommender()

@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = None
    query = ""
    error = None
    
    if request.method == "POST":
        query = request.form.get("movie_query", "").strip()
        if query:
            # Get recommendations as a DataFrame or error string
            result = recommender.recommend(query, num_recommendations=6)
            
            if isinstance(result, str):
                error = result
            else:
                # Convert the DataFrame to a list of dicts for Jinja parsing
                recommendations = result.to_dict('records')
                
    return render_template("movies.html", query=query, recommendations=recommendations, error=error)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
