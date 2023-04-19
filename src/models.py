from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    skill_level= db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    #time_posted = db.Column(db.Date, nullable=False)
    title = db.Column(db.String, nullable=False)
    #image = db.Column(db.String, nullable=True)
    is_vegan = db.Column(db.Boolean, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    equipment = db.Column(db.String, nullable=False)
    #duration = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    #tags = db.Column(db.String, nullable=False)

    # Users are not implemented yet
    #author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    #author = db.relationship('User', backref='author')