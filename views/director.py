from flask_restx import Resource, Namespace
from models import Director, DirectorSchema
from setup_db import db

director_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        try:
            all_directors = db.session.query(Director).all()
            return directors_schema.dump(all_directors), 200
        except Exception as e:
            return f'{e}', 404


@director_ns.route('/<int:bid>')
class DirectorsView(Resource):
    def get(self, bid: int):
        try:
            note = Director.query.get(bid)
            return director_schema.dump(note), 200
        except Exception as e:
            return "", 404
