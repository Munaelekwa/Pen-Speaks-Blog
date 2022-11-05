from datetime import datetime
from db import db
from flask_login import UserMixin


# User model for the database. 
# Stores dynamic information gotten from the register form in the columns defined
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Blogpost', backref='author', lazy=True)

    def __repr__(self):
        return f"User <{self.firstname}, {self.lastname}>"

# Contact model for the contact page
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    message = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"User <{self.name}, {self.email}>"

# Blogpost model to store posts made by users
class Blogpost(db.Model):       
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Title <{self.title}>"
