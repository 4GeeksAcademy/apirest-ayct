"""
This module takes care of starting the API Server
"""

import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_cors import CORS

from utils import APIException, generate_sitemap
from admin import setup_admin

from models import db, User, Character, Planet, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")

if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://",
        "postgresql://"
    )
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

USER_ACTUAL = 1


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/people', methods=['GET'])
def get_people():
    people = Character.query.all()
    results = []
    for person in people:
        results.append(person.serialize())
    return jsonify(results), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):

    person = Character.query.get(people_id)
    if person is None:
        return jsonify({"msg": "Character not found"}), 404
    return jsonify(person.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    results = []
    for planet in planets:
        results.append(planet.serialize())
    return jsonify(results), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    results = []
    for user in users:
        results.append(user.serialize())
    return jsonify(results), 200


@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorite.query.filter_by(user_id=USER_ACTUAL).all()
    results = []
    for favorite in favorites:
        results.append(favorite.serialize())
    return jsonify(results), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    favorite = Favorite(user_id=USER_ACTUAL, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite planet added"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    favorite = Favorite(user_id=USER_ACTUAL, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorite character added"}), 200


@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    favorite = Favorite.query.filter_by(
        planet_id=planet_id, user_id=USER_ACTUAL).first()
    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite deleted"}), 200


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    favorite = Favorite.query.filter_by(
        character_id=people_id, user_id=USER_ACTUAL).first()
    if favorite is None:
        return jsonify({"msg": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"msg": "Favorite deleted"}), 200


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False
            )