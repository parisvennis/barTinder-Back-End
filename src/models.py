from flask_sqlalchemy import SQLAlchemy
from datetime import timezone

db = SQLAlchemy()

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    birth_date = db.Column(db.Date, unique=False, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name
            # do not serialize the password, its a security breach
        }

class Drinks(db.Model):
    
    drink_id = db.Column(db.Integer, primary_key=True)
    drink_name = db.Column(db.String(250), unique=False, nullable=False)
    instructions = db.Column(db.Text(), unique=False, nullable=False)
    measurements = db.Column(db.Text(), unique=False, nullable=False)
    thumbnail = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return '<Drinks %r>' % self.drink_name

    def serialize(self):
        return {
            "drink_id": self.drink_id,
            "drink_name": self.drink_name,
            "instructions": self.instructions,
            "measurements": self.measurements,
            "thumbnail": self.thumbnail
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    
    user_id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "drink_id": self.drink_id
            # do not serialize the password, its a security breach
        }