from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model untuk Film
class Film(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

# Inisialisasi database
@app.before_first_request
def create_tables():
    db.create_all()

# Endpoint untuk membuat film baru
@app.route('/films', methods=['POST'])
def create_film():
    data = request.get_json()
    new_film = Film(
        title=data['title'],
        genre=data['genre'],
        price=data['price'],
        stock=data['stock']
    )
    db.session.add(new_film)
    db.session.commit()
    return jsonify({'message': 'Film created successfully!'}), 201

# Endpoint untuk membaca semua film
@app.route('/films', methods=['GET'])
def get_films():
    films = Film.query.all()
    results = [
        {
            'id': film.id,
            'title': film.title,
            'genre': film.genre,
            'price': film.price,
            'stock': film.stock
        } for film in films
    ]
    return jsonify(results)

# Endpoint untuk membaca film berdasarkan ID
@app.route('/films/<int:id>', methods=['GET'])
def get_film(id):
    film = Film.query.get(id)
    if not film:
        return jsonify({'message': 'Film not found'}), 404
    result = {
        'id': film.id,
        'title': film.title,
        'genre': film.genre,
        'price': film.price,
        'stock': film.stock
    }
    return jsonify(result)

# Endpoint untuk mengupdate film berdasarkan ID
@app.route('/films/<int:id>', methods=['PUT'])
def update_film(id):
    data = request.get_json()
    film = Film.query.get(id)
    if not film:
        return jsonify({'message': 'Film not found'}), 404
    film.title = data.get('title', film.title)
    film.genre = data.get('genre', film.genre)
    film.price = data.get('price', film.price)
    film.stock = data.get('stock', film.stock)
    db.session.commit()
    return jsonify({'message': 'Film updated successfully'})

# Endpoint untuk menghapus film berdasarkan ID
@app.route('/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    film = Film.query.get(id)
    if not film:
        return jsonify({'message': 'Film not found'}), 404
    db.session.delete(film)
    db.session.commit()
    return jsonify({'message': 'Film deleted successfully'})

# Jalankan server
if __name__ == '__main__':
    app.run(debug=True)
