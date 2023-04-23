from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, nullable=False)
    skill = db.Column(db.String, nullable=False)
    social = db.Column(db.String, nullable=False)
    about = db.Column(db.String, nullable=False)
    
    def __init__(self, email, username, password) -> None:
        self.email = email
        self.username = username
        self.password = password
        self.profile_picture = ''
        self.skill = 'Novice'
        self.social = ''
        self.about = ''

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    #time_posted = db.Column(db.Date, nullable=False)
    title = db.Column(db.String, nullable=False)
    #image = db.Column(db.String, nullable=True)
    is_vegan = db.Column(db.Boolean, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    equipment = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
    #tags = db.Column(db.String, nullable=False)

    # Users are not implemented yet
    #author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    #author = db.relationship('User', backref='author')