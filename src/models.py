from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

# Tablas de asociación para favoritos
favorite_characters = Table(
    "favorite_characters",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("character_id", ForeignKey("character.id"), primary_key=True),
)

favorite_locations = Table(
    "favorite_locations",
    db.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("location_id", ForeignKey("location.id"), primary_key=True),
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)

    favorite_character_list: Mapped[list["Character"]] = relationship(
        secondary=favorite_characters,
        back_populates="favorited_by"
    )

    favorite_location_list: Mapped[list["Location"]] = relationship(
        secondary=favorite_locations,
        back_populates="favorited_by"
    )

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
    
    def serialize_with_favorites(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "favorite_characters": [char.serialize() for char in self.favorite_character_list],
            "favorite_locations": [loc.serialize() for loc in self.favorite_location_list],
        }


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    species: Mapped[str] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=True)
    image: Mapped[str] = mapped_column(String(200), nullable=True)

    favorited_by: Mapped[list["User"]] = relationship(
        secondary=favorite_characters,
        back_populates="favorite_character_list"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "species": self.species,
            "status": self.status,
            "gender": self.gender,
            "image": self.image,
        }


class Location(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=True)
    dimension: Mapped[str] = mapped_column(String(100), nullable=True)

    favorited_by: Mapped[list["User"]] = relationship(
        secondary=favorite_locations,
        back_populates="favorite_location_list"
    )

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "dimension": self.dimension,
        }