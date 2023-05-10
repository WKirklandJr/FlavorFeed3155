from flask import Flask, session, redirect, render_template, request, abort
from dotenv import load_dotenv
import os, functools

from src.models import db
from security import bcrypt

# Repositories
from src.repositories.user_repository import user_repository_singleton
from src.repositories.recipe_repository import recipe_repository_singleton
from src.repositories.tags_repository import tag_repository_singleton
from src.repositories.comment_repository import comment_repository_singleton

# Routers
from src.routers.home_router import home_router
from src.routers.recipes_router import recipes_router
from src.routers.profile_router import profile_router

load_dotenv()

app = Flask(__name__)

# Database connection
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASS')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] \
    = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = os.getenv('APP_SECRET')

db.init_app(app)
bcrypt.init_app(app)

def userauth(route):
    @functools.wraps(route)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return route(*args, **kwargs)
        return redirect('/login')
    return wrapper
    
# Gets session username across application
@app.context_processor
def getusername():
    return {'username': session.get('user')} 

# Gets session user ID across application
@app.context_processor
def getuserID():
    if 'user' in session:
        return {'user_id': session.get('user') } 
    return ''

# HOME PAGES
app.register_blueprint(home_router)

# RECIPES PAGES
app.register_blueprint(recipes_router)

# RECIPE TAGS
@app.get('/search/<tagname>')
def search_tag(tagname):
    tag = tag_repository_singleton.get_tag(tagname)

    bookmarked_recipes = None
    if 'user' in session:
        bookmarked_recipes = recipe_repository_singleton.get_recipes_by_bookmark(session['user']['user_id'])

   
    return render_template('search_posts.html', tag=tag, bookmarked=bookmarked_recipes)



# USER PAGES
@app.get('/users/<int:user_id>')
def get_user(user_id):
    single_user = user_repository_singleton.get_user_by_id(user_id)
    user_recipes = recipe_repository_singleton.get_recipes_by_user(user_id)
    user_comments = comment_repository_singleton.get_comment_by_user_id(user_id)

    bookmarked_recipes = None
    if 'user' in session:
        bookmarked_recipes = recipe_repository_singleton.get_recipes_by_bookmark(session['user']['user_id'])

    return render_template('get_single_profile.html', user=single_user, recipes=user_recipes,comments=user_comments, bookmarked=bookmarked_recipes)

# PROFILE PAGES
app.register_blueprint(profile_router)
