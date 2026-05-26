from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    date_sub: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    lastname: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    favorite = relationship('Favorite', back_populates='user')

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "date_sub": self.date_sub,
            "name": self.name,
            "lastname": self.lastname,
            "is_active": self.is_active
        }


class Character(db.Model):

    __tablename__ = 'character'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    height: Mapped[int] = mapped_column()
    mass: Mapped[int] = mapped_column()
    hair_color: Mapped[str] = mapped_column()
    skin_color: Mapped[str] = mapped_column()
    eye_color: Mapped[str] = mapped_column()
    birth_year: Mapped[int] = mapped_column()
    gender: Mapped[str] = mapped_column()
    homeworld: Mapped[str] = mapped_column()
    films: Mapped[str] = mapped_column()
    species: Mapped[str] = mapped_column()
    vehicles: Mapped[str] = mapped_column()
    starships: Mapped[str] = mapped_column()
    created: Mapped[str] = mapped_column()
    edited: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()

    favorite = relationship('Favorite', back_populates='character')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "homeworld": self.homeworld,
            "films": self.films,
            "species": self.species,
            "vehicles": self.vehicles,
            "starships": self.starships,
            "created": self.created,
            "edited": self.edited,
            "url": self.url
        }


class Planet(db.Model):

    __tablename__ = 'planet'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    rotation_period: Mapped[int] = mapped_column()
    orbital_period: Mapped[int] = mapped_column()
    diameter: Mapped[int] = mapped_column()
    climate: Mapped[str] = mapped_column()
    gravity: Mapped[str] = mapped_column()
    terrain: Mapped[str] = mapped_column()
    surface_water: Mapped[int] = mapped_column()
    population: Mapped[int] = mapped_column()
    residents: Mapped[str] = mapped_column()
    films: Mapped[str] = mapped_column()
    created: Mapped[str] = mapped_column()
    edited: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()

    favorite = relationship('Favorite', back_populates='planet')

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "population": self.population,
            "residents": self.residents,
            "films": self.films,
            "created": self.created,
            "edited": self.edited,
            "url": self.url
        }


class Favorite(db.Model):

    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id")
    )

    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"),
        nullable=True
    )

    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"),
        nullable=True
    )

    user = relationship("User", back_populates="favorite")
    character = relationship("Character", back_populates="favorite")
    planet = relationship("Planet", back_populates="favorite")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id
        }