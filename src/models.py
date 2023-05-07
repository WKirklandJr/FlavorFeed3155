from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()

# Table for users
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, nullable=True)
    skill = db.Column(db.String, nullable=True)
    social = db.Column(db.String, nullable=True)
    about = db.Column(db.String, nullable=True) 
    recipes = db.relationship('Recipe', backref='author', passive_deletes=True)


    
    def __init__(self, email, username, password) -> None:
        self.email = email
        self.username = username
        self.password = password
        self.profile_picture = ''
        self.skill = ''
        self.social = ''
        self.about = ''



#Table for tags
class Tag(db.Model):
   __tablename__ = 'tags'

   tag_id = db.Column(db.Integer, primary_key=True)
   tagname = db.Column(db.String, nullable=False)

   def __init__(self, tagname):
       self.tagname = tagname



# # Junction table for the n:n relationship b/w users and recipes
bookmarks = db.Table(
    'bookmarks',
    db.Column('user_id', db.Integer, \
              db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True),
    db.Column('tag_id', db.Integer, \
              db.ForeignKey('recipes.recipe_id', ondelete='CASCADE'), primary_key=True)
)

# Junction table for the n:n relationship b/w recipes and tags
recipe_tag = db.Table(
   'recipe_tag',
   db.Column('recipe_id', db.Integer, \
             db.ForeignKey('recipes.recipe_id', ondelete='CASCADE'), primary_key=True),
   db.Column('tag_id', db.Integer, \
             db.ForeignKey('tags.tag_id', ondelete='CASCADE'), primary_key=True)
)

# Table for recipes
class Recipe(db.Model):
    __tablename__ = 'recipes'

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
    user_id = db.Column(db.String, db.ForeignKey('users.user_id',  ondelete='CASCADE'), nullable=False)
    tags = db.relationship('Tag', secondary=recipe_tag, backref='recipes', passive_deletes=True)
    #bookmark = db.relationship('User', secondary=bookmarks, backref='recipes')


    def __init__\
        (self, title,is_vegan,ingredients,equipment,duration,difficulty,instructions,recipe_image,date_posted,user_id) -> None:
        self.title = title
        self.is_vegan = is_vegan
        self.ingredients = ingredients
        self.equipment = equipment
        self.duration = duration
        self.difficulty = difficulty
        self.instructions = instructions
        self.recipe_image = recipe_image
        self.date_posted = date_posted
        self.user_id = user_id



class Comment(db.Model):
    __tablename__ = 'user_recipe_comments'

    comment_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id', ondelete='CASCADE'))
    comment = db.Column(db.String, nullable=False)

    def __init__(self, user_id, recipe_id, comment):
        self.user_id = user_id
        self.recipe_id = recipe_id
        self.comment = comment
