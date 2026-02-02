from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "7adf97be58453945d750084884c7ee3b"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# -------------------------
# PELÍCULAS POPULARES
# -------------------------
@app.route("/")
def index():
    url = f"{BASE_URL}/movie/popular"
    params = {
        "api_key": API_KEY,
        "language": "es-MX",
        "page": 1
    }

    response = requests.get(url, params=params).json()
    movies = response.get("results", [])[:10]

    return render_template(
        "index.html",
        movies=movies,
        image_url=IMAGE_URL
    )

# -------------------------
# BÚSQUEDA
# -------------------------
@app.route("/search")
def search():
    query = request.args.get("query")
    page = request.args.get("page", 1)

    movies = []
    total_pages = 1

    if query:
        url = f"{BASE_URL}/search/movie"
        params = {
            "api_key": API_KEY,
            "language": "es-MX",
            "query": query,
            "page": page
        }
        response = requests.get(url, params=params).json()
        movies = response.get("results", [])
        total_pages = response.get("total_pages", 1)

    return render_template(
        "search.html",
        movies=movies,
        query=query,
        page=int(page),
        total_pages=total_pages,
        image_url=IMAGE_URL
    )

# -------------------------
# DETALLE
# -------------------------
@app.route("/detalle/<int:movie_id>")
def detalle(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "es-MX"
    }

    movie = requests.get(url, params=params).json()

    # Reparto
    credits_url = f"{BASE_URL}/movie/{movie_id}/credits"
    credits = requests.get(credits_url, params=params).json()
    cast = credits.get("cast", [])[:6]

    # Trailer
    video_url = f"{BASE_URL}/movie/{movie_id}/videos"
    videos = requests.get(video_url, params=params).json()
    trailer = None
    for v in videos.get("results", []):
        if v["type"] == "Trailer" and v["site"] == "YouTube":
            trailer = v["key"]
            break

    return render_template(
        "detalle.html",
        movie=movie,
        cast=cast,
        trailer=trailer,
        image_url=IMAGE_URL
    )

if __name__ == "__main__":
    app.run(debug=True)