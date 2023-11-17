from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship

    # Add serialization rules


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    
    
    # Add relationship

    # Add serialization rules

    # Add validation
    @validates('name')
    def validate_name(self, _, value):
        if not value:
            raise ValueError('Name must be provided.')
        else:
            return value

    @validates('field_of_study')
    def validate_field_of_study(self, _, value):
        if not value:
            raise ValueError('Field of study must be provided.')
        else:
            return value


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    scientist_id = db.Column(db.String, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    # Add relationships

    # Add serialization rules

    # Add validation
    @validates('name')
    def validate_name(self, _, value):
        if not value:
            raise ValueError('Name must be provided.')
        else:
            return value
        
    @validates('scientist_id')
    def validate_scientist_id(self, _, value):
        if not value:
            raise ValueError("Scientist Id must be provided.")
        elif not isinstance(value, int):
            raise ValueError("Scientist Id must be an integer.")
        else:
            return value
        
    @validates('planet_id')
    def validate_planet_id(self, _, value):
        if not value:
            raise ValueError("Planet Id must be provided.")
        elif not isinstance(value, int):
            raise ValueError("Planet Id must be an integer.")
        else:
            return value


# add any models you may need.
