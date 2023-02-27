from flask_restx import Resource, Namespace
from models import Genre, GenreSchema
from setup_db import db

genre_ns = Namespace('genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genre_ns.route('/')
class GenreView(Resource):
    def get(self):
        try:
            all_genres = db.session.query(Genre).all()
            return genres_schema.dump(all_genres)
        except Exception as e:
            return f'{e}', 404


@genre_ns.route('/<int:bid>')
class GenreView(Resource):
    def get(self, bid: int):
        try:
            genre = Genre.query.get(bid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return "", 404
