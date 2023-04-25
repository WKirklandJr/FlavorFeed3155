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
    title = db.Column(db.String, nullable=False)
    is_vegan = db.Column(db.Boolean, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    equipment = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    recipe_image = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False)
    #tags = db.Column(db.String, nullable=False)

    # Users are not implemented yet
    #author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    #author = db.relationship('User', backref='author')

    def __init__\
        (self, title,is_vegan,ingredients,equipment,duration,difficulty,instructions,recipe_image,date_posted) -> None:
        self.title = title
        self.is_vegan = is_vegan
        self.ingredients = ingredients
        self.equipment = equipment
        self.duration = duration
        self.difficulty = difficulty
        self.instructions = instructions
        self.recipe_image = recipe_image
        self.date_posted = date_posted

