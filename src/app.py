"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Vehicle, Character, FavoriteCharacter, FavoriteVehicle, FavoritePlanet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/character', methods=['GET'])
def get_all_characters():

    all_characters = Character.query.all()
    if not len(all_characters) > 0:
        return jsonify({"error": "Characters not found"}), 404
    serialized_characters = [character.serialize() for character in all_characters]
    return jsonify(serialized_characters), 200

@app.route('/character/<int:character_id>', methods=['GET'])
def get_one_character(character_id):

    character = Character.query.get(character_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200

@app.route('/planet', methods=['GET'])
def get_all_planets():

    all_planets = Planet.query.all()
    if not len(all_planets) > 0:
        return jsonify({"error": "Planets not found"}), 404
    serialized_planets = [planet.serialize() for planet in all_planets]
    return jsonify(serialized_planets), 200

@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_one_planet(planet_id):

    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

@app.route('/vehicle', methods=['GET'])
def get_all_vehicles():

    all_vehicles = Vehicle.query.all()
    if not len(all_vehicles) > 0:
        return jsonify({"error": "Vehicles not found"}), 404
    serialized_vehicles = [vehicle.serialize() for vehicle in all_vehicles]
    return jsonify(serialized_vehicles), 200

@app.route('/vehicle/<int:vehicle_id>', methods=['GET'])
def get_one_vehicle(vehicle_id):

    vehicle = Vehicle.query.get(vehicle_id)
    if not vehicle:
        return jsonify({"error": "Vehicle not found"}), 404
    return jsonify(vehicle.serialize()), 200


@app.route('/user', methods=['GET'])
def get_all_users():

    all_users = User.query.all()
    if not len(all_users) > 0:
        return jsonify({"error": "Users not found"}), 404
    serialized_users = [user.serialize() for user in all_users]
    return jsonify(serialized_users), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_one_user(user_id):

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize_favorites()), 200

@app.route('/favorite/user/<int:user_id>/character/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):

    try:
        # Validar usuario y Id del character
        if not isinstance(user_id, int) or not isinstance(character_id, int):
            return jsonify({"error": "Invalid user or character ID"}), 400
        # verificar si el character ya existe como favorito
        is_favorite = FavoriteCharacter.query.filter_by(user_id=user_id, character_id=character_id).first()
        if is_favorite:
            return jsonify({"error": "Character is already a favorite"}), 409
        # crear un FavoriteCharacter object nuevo
        new_favorite = FavoriteCharacter(user_id=user_id, character_id=character_id)
        # agregar el favorito nuevo a la base de datos y hacer el commit con los cambios
        db.session.add(new_favorite)
        db.session.commit()
        # retornar una respuesta JSON indicando éxito
        return jsonify({"message": "Character added to favorites successfully"}), 201

    except Exception as e:
        # Manejar los errores en la base de datos y otras excepciones 
        return jsonify({"error": str(e)}), 500

@app.route('/favorite/user/<int:user_id>/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):

    try:
        # Validar usuario y Id del planet
        if not isinstance(user_id, int) or not isinstance(planet_id, int):
            return jsonify({"error": "Invalid user or planet ID"}), 400
        # verificar si el planet ya existe como favorito
        is_favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if is_favorite:
            return jsonify({"error": "planet is already a favorite"}), 409
        # crear un Favoriteplanet object nuevo
        new_favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
        # agregar el favorito nuevo a la base de datos y hacer el commit con los cambios
        db.session.add(new_favorite)
        db.session.commit()
        # retornar una respuesta JSON indicando éxito
        return jsonify({"message": "Planet added to favorites successfully"}), 201

    except Exception as e:
        # Manejar los errores en la base de datos y otras excepciones 
        return jsonify({"error": str(e)}), 500


@app.route('/favorite/user/<int:user_id>/vehicle/<int:vehicle_id>', methods=['POST'])
def add_favorite_vehicle(user_id, vehicle_id):

    try:
        # Validar usuario y Id del vehicle
        if not isinstance(user_id, int) or not isinstance(vehicle_id, int):
            return jsonify({"error": "Invalid user or vehicle ID"}), 400
        # verificar si el vehicle ya existe como favorito
        is_favorite = FavoriteVehicle.query.filter_by(user_id=user_id, vehicle_id=vehicle_id).first()
        if is_favorite:
            return jsonify({"error": "Vehicle is already a favorite"}), 409
        # crear un Favoritevehicle object nuevo
        new_favorite = FavoriteVehicle(user_id=user_id, vehicle_id=vehicle_id)
        # agregar el favorito nuevo a la base de datos y hacer el commit con los cambios
        db.session.add(new_favorite)
        db.session.commit()
        # retornar una respuesta JSON indicando éxito
        return jsonify({"message": "Vehicle added to favorites successfully"}), 201

    except Exception as e:
        # Manejar los errores en la base de datos y otras excepciones 
        return jsonify({"error": str(e)}), 500





# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
