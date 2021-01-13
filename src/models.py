from flask_sqlalchemy import SQLAlchemy
from datetime import timezone

db = SQLAlchemy()

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    birth_date = db.Column(db.DateTime, unique=False, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "user_id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "favorites": list(map(lambda x: x.serialize(),self.favorites))
            # do not serialize the password, its a security breach
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drink_id = db.Column(db.Integer, unique=False, nullable=False)
    drink_name = db.Column(db.String(250), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __repr__(self):
        return '<Favorite %r>' % self.user_id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "drink_id": self.drink_id,
            "drink_name": self.drink_name
            # do not serialize the password, its a security breach
        }