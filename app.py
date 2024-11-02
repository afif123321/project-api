# app.py
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# Data film (database sederhana)
films = [
    {"id": 1, "title": "Inception", "director": "Christopher Nolan", "year": 2010, "genre": "Sci-Fi"},
    {"id": 2, "title": "The Matrix", "director": "Lana Wachowski, Lilly Wachowski", "year": 1999, "genre": "Action"},
    {"id": 3, "title": "Interstellar", "director": "Christopher Nolan", "year": 2014, "genre": "Sci-Fi"},
    {"id": 4, "title": "The Dark Knight", "director": "Christopher Nolan", "year": 2008, "genre": "Action"},
    {"id": 5, "title": "Parasite", "director": "Bong Joon-ho", "year": 2019, "genre": "Thriller"},
    {"id": 6, "title": "Avengers: Endgame", "director": "Anthony Russo, Joe Russo", "year": 2019, "genre": "Action"},
    {"id": 7, "title": "Pulp Fiction", "director": "Quentin Tarantino", "year": 1994, "genre": "Crime"},
    {"id": 8, "title": "Fight Club", "director": "David Fincher", "year": 1999, "genre": "Drama"},
    {"id": 9, "title": "Forrest Gump", "director": "Robert Zemeckis", "year": 1994, "genre": "Drama"},
    {"id": 10, "title": "The Godfather", "director": "Francis Ford Coppola", "year": 1972, "genre": "Crime"}
]

# Helper functions
def get_all_films():
    return films

def get_film_by_id(film_id):
    return next((film for film in films if film["id"] == film_id), None)

# Resource untuk daftar film (GET & POST)
class FilmList(Resource):
    def get(self):
        return jsonify(get_all_films())

    def post(self):
        new_film = request.get_json()
        new_film["id"] = films[-1]["id"] + 1 if films else 1
        films.append(new_film)
        return jsonify(new_film), 201

# Resource untuk film individu (GET, PUT, DELETE)
class Film(Resource):
    def get(self, film_id):
        film = get_film_by_id(film_id)
        if film:
            return jsonify(film)
        return jsonify({"error": "Film not found"}), 404

    def put(self, film_id):
        film = get_film_by_id(film_id)
        if not film:
            return jsonify({"error": "Film not found"}), 404
        update_data = request.get_json()
        film.update(update_data)
        return jsonify(film)

    def delete(self, film_id):
        global films
        films = [film for film in films if film["id"] != film_id]
        return jsonify({"message": "Film deleted"}), 204

# Menambahkan endpoint ke API
api.add_resource(FilmList, "/films")
api.add_resource(Film, "/films/<int:film_id>")

# Menjalankan aplikasi
if __name__ == "__main__":
    app.run(debug=True)
