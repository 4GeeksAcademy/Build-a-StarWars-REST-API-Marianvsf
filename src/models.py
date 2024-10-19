from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    gravity = db.Column(db.String(250))
    population = db.Column(db.String(250))
    climate = db.Column(db.String(250))
    favorite_planets = db.relationship('FavoritePlanet', back_populates='planet')
   
    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate
            # do not serialize the password, its a security breach
        }

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    favorite_vehicles = db.relationship('FavoriteVehicle', back_populates='vehicle')
    
    def __repr__(self):
        return '<Vehicle %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "manufacturer": self.manufacturer
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(6))
    hair_color = db.Column(db.String(250))
    favorite_characters = db.relationship('FavoriteCharacter', back_populates='character')

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "hair_color": self.hair_color
            # do not serialize the password, its a security breach
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))
    password = db.Column(db.String(50))
    fecha_ingreso = db.Column(db.String(250))
    is_active = db.Column(db.Boolean(), default=True, unique=False, nullable=False)
    favorite_characters = db.relationship('FavoriteCharacter', back_populates='user')
    favorite_vehicles = db.relationship('FavoriteVehicle', back_populates='user')
    favorite_planets = db.relationship('FavoritePlanet', back_populates='user')

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_ingreso": self.fecha_ingreso,
            "is_active": self.is_active
            # do not serialize the password, its a security breach
        }
    def serialize_favorites(self):
        result = {}
        result['favorites'] = {}
        result["user"] = self.serialize()
        if len(self.favorite_characters) > 0:
            result["favorites"]["characters"] = [character.character.serialize() for character in self.favorite_characters] 
        if len(self.favorite_vehicles) > 0:
            result["favorites"]["vehicles"] = [vehicle.vehicle.serialize() for vehicle in self.favorite_vehicles] 
        if len(self.favorite_planets) > 0:
            result["favorites"]["planets"] = [planet.planet.serialize() for planet in self.favorite_planets] 
        return result

# class Favorite(db.Model):
#     __tablename__ = 'favorites'
#     id = db.Column(db.Integer, primary_key=True)
#     usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     favorites = db.Column(db.Enum('personaje', 'vehiculo', 'planeta', name='favorite_types'))
#     fcharacter_id = db.Column(db.Integer, db.ForeignKey('favoritecharacters.id'))
#     fcvehicle_id = db.Column(db.Integer, db.ForeignKey('favoritevehicles.id'))
#     fplanet_id = db.Column(db.Integer, db.ForeignKey('favoriteplanets.id'))
#     user = db.relationship('User', back_populates='favorites')

class FavoriteCharacter(db.Model):
    __tablename__ = 'favoritecharacters'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    character = db.relationship(Character)
    user = db.relationship(User)

    def __repr__(self):
        return '<FavoriteCharacter %r>' % self.id
    

class FavoriteVehicle(db.Model):
    __tablename__ = 'favoritevehicles'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    # vehicle = db.relationship('Vehicle', back_populates='favorites') 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    vehicle = db.relationship(Vehicle)
    user = db.relationship(User)
    
    def __repr__(self):
        return '<FavoriteVehicle %r>' % self.id
    
class FavoritePlanet(db.Model):
    __tablename__ = 'favoriteplanets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    # planet = db.relationship('Planet', back_populates='favorites')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    planet = db.relationship(Planet)
    user = db.relationship(User)
    
    def __repr__(self):
        return '<FavoritePlanet %r>' % self.id