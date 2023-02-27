from flask import request
from flask_restx import Resource, Namespace
from models import Movie, MovieSchema
from setup_db import db

movie_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')
        if director_id:
            movies = Movie.query.filter(Movie.director_id == director_id).all()
            return movies_schema.dump(movies), 200
        if genre_id:
            movies = Movie.query.filter(Movie.genre_id == genre_id).all()
            return movies_schema.dump(movies), 200
        if year:
            movies = Movie.query.filter(Movie.year == year).all()
            return movies_schema.dump(movies), 200
        try:
            all_movies = db.session.query(Movie).all()
            return movies_schema.dump(all_movies)
        except Exception as e:
            return f'{e}', 404

    def post(self):
        req_json = request.json
        new_user = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_user)
        return "", 201

    def put(self, uid):  # Замена данных
        movie = Movie.query.get(uid)
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

    def delete(self, bid: int):
        user = Movie.query.get(bid)
        db.session.delete(user)
        db.session.commit()
        return "", 204


@movie_ns.route('/<int:bid>')
class MoviesView(Resource):
    def get(self, bid: int):
        try:
            genre = Movie.query.get(bid)
            return movie_schema.dump(genre), 200
        except Exception as e:
            return "", 404


# @movie_ns.route("/")
# class ClassView(Resource):
#     def get(self):
#         director_id = request.args.get('director_id')
#         genre_id = request.args.get('genre_id')
#         year = request.args.get('year')
#         if director_id:
#             movies = Movie.query.filter(Movie.director_id == director_id).all()
#             return movies_schema.dump(movies), 200
#         if genre_id:
#             movies = Movie.query.filter(Movie.genre_id == genre_id).all()
#             return movies_schema.dump(movies), 200
#         if year:
#             movies = Movie.query.filter(Movie.year == year).all()
#             return movies_schema.dump(movies), 200
