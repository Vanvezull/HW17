# app.py

from flask import request
from flask_restx import Api, Resource
from config import app
from models import *

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route('/')  # Представление для получения всех фильмов, а так же фильмов по директору и жанру
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id', type=int)
        genre_id = request.args.get('genre_id')
        if director_id:
            return MovieSchema(many=True).dump(Movie.query.filter(Movie.director_id == director_id).all()), 200
        if genre_id:
            return MovieSchema(many=True).dump(Movie.query.filter(Movie.genre_id == genre_id).all()), 200
        return MovieSchema(many=True).dump(Movie.query.all()), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)
        return "", 201

@movie_ns.route('/<int:id>')  # Представление для получения фильма по id
class MovieView(Resource):
    def get(self, id):
        return MovieSchema().dump(Movie.query.get(id)), 201

    def put(self, id):
        movie = db.session.query(Movie).get(id)
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre_id = req_json.get("genre_id")
        movie.director_id = req_json.get("director_id")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, id):
        movie = db.session.query(Movie).get(id)

        db.session.delete(movie)
        db.session.commit()
        return ""


@director_ns.route('/')  # Представление для получения всех режиссеров
class MoviesView(Resource):
    def get(self):
        return DirectorSchema(many=True).dump(Movie.query.all()), 200


@director_ns.route('/<int:id>')  # Представление для получения режиссера по id
class MovieView(Resource):
    def get(self, id):
        return DirectorSchema().dump(Movie.query.get(id)), 201


@genre_ns.route('/') # Представление для получения всех жанров
class MoviesView(Resource):
    def get(self):
        return GenresSchema(many=True).dump(Movie.query.all()), 200


@genre_ns.route('/<int:id>') # Представление для получения жанра по id
class MovieView(Resource):
    def get(self, id):
        return GenresSchema().dump(Movie.query.get(id)), 201


if __name__ == '__main__':
    app.run(debug=True)
