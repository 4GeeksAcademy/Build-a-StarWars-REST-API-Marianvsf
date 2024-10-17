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
    favorites = db.relationship('FavoritePlanet', back_populates='planet')

class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    lastname = db.Column(db.String(250))
    description = db.Column(db.String(250))
    model = db.Column(db.String(250))
    manufacturer = db.Column(db.String(250))
    favorites = db.relationship('FavoriteVehicle', back_populates='vehicle')

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250))
    color_eyes = db.Column(db.String(250))
    birth_year = db.Column(db.String(250))
    gender = db.Column(db.String(6))
    hair_color = db.Column(db.String(250))
    favorites = db.relationship('FavoriteCharacter', back_populates='character')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    apellido = db.Column(db.String(250))
    email = db.Column(db.String(250))
    fecha_ingreso = db.Column(db.String(250))
    is_active = db.Column(db.Boolean(), default=True, unique=False, nullable=False)
    favorites = db.relationship('Favorite', back_populates='user')

class Login(db.Model):
    __tablename__ = 'logins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250))
    password = db.Column(db.String(250))
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    favorites = db.Column(db.Enum('personaje', 'vehiculo', 'planeta', name='favorite_types'))
    fcharacter_id = db.Column(db.Integer, db.ForeignKey('favoritecharacters.id'))
    fcvehicle_id = db.Column(db.Integer, db.ForeignKey('favoritevehicles.id'))
    fplanet_id = db.Column(db.Integer, db.ForeignKey('favoriteplanets.id'))
    user = db.relationship('User', back_populates='favorites')

class FavoriteCharacter(db.Model):
    __tablename__ = 'favoritecharacters'
    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship('Character', back_populates='favorites') 

class FavoriteVehicle(db.Model):
    __tablename__ = 'favoritevehicles'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle = db.relationship('Vehicle', back_populates='favorites') 

class FavoritePlanet(db.Model):
    __tablename__ = 'favoriteplanets'
    id = db.Column(db.Integer, primary_key=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship('Planet', back_populates='favorites')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }