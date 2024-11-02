# app.py
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# Data film (database sederhana)
films = [
    {
        "id": 1,
        "title": "Inception",
        "director": "Christopher Nolan",
        "year": 2010,
        "genre": "Sci-Fi"
    },
    {
        "id": 2,
        "title": "The Matrix",
        "director": "Lana Wachowski, Lilly Wachowski",
        "year": 1999,
        "genre": "Action"
    }
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
