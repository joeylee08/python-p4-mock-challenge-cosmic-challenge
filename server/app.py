#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route('/')
def home():
    return ''

class Scientists(Resource):
    def get(self):
        try:
            scientist_data = [scientist.to_dict() for scientist in Scientist.query.all()]
            return make_response(scientist_data, 200)
        except Exception as e:
            return make_response({"errors:", str(e)}, 400)
    def post(self):
        try:
            new_scientist = Scientist(
                name = request.get_json()['name'], 
                field_of_study = request.get_json()['field_of_study']
            )
            db.session.add(new_scientist)
            db.session.commit()
            return new_scientist.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return make_response({"errors" : str(e)}, 400)
        

api.add_resource(Scientists, '/scientists')

class ScientistById(Resource):
    def get(self, id):
        try:
            scientist_by_id = Scientist.query.filter_by(id=id).first().to_dict()
            return make_response(scientist_by_id, 201)
        except Exception as e:
            return make_response({"errors" : str(e)}, 404)
        
    def patch(self, id):
        try:
            scientist_by_id = Scientist.query.filter(Scientist.id==id).first().to_dict()
            if scientist_by_id:
                for k, v in request.get_json().items():
                    setattr(scientist_by_id, k, v)
                db.session.commit()
                db.session.refresh(scientist_by_id)
                return make_response(scientist_by_id, 201)
            else:
                return make_response({"error" : "Scientist not found"}, 404)
        except Exception as e:
            db.session.rollback()
            return make_response({"errors" : str(e)}, 202)
        
    def delete(self, id):
        try:
            scientist_by_id = Scientist.query.filter(Scientist.id==id).first().to_dict()
            if scientist_by_id:
                db.session.delete(scientist_by_id)
                db.session.commit()
                return make_response({}, 204)
            else:
                return make_response({"error" : "Scientist not found"}, 404)
        except Exception as e:
            return make_response({"errors" : str(e)})

api.add_resource(ScientistById, '/scientists/<int:id>')

class Planets(Resource):
    def get(self, id):
        pass

api.add_resource(Planets, '/planets')

class Missions(Resource):
    def post(self, id):
        pass

api.add_resource(Missions, '/missions')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
