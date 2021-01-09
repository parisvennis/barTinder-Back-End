from flask_sqlalchemy import SQLAlchemy
from datetime import timezone

db = SQLAlchemy()

class User(db.Model):

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    birth_date = db.Column(db.DateTime, unique=False, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "user_id": self.user_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date
            # do not serialize the password, its a security breach
        }

class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    drink_id = db.Column(db.Integer, unique=False, nullable=False)
    drink_name = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "drink_id": self.drink_id,
            "drink_name": self.drink_name
            # do not serialize the password, its a security breach
        }