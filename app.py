from flask import Flask, redirect, render_template, request, abort
from dotenv import load_dotenv
import os

from src.models import db
from src.repositories.recipe_repository import recipe_repository_singleton

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

db.init_app(app)

#HOME PAGES

@app.get('/')
def index():
    return render_template('index.html')
#TODO:index.html page

@app.get('/about')
def about():
    return render_template('about.html')

#LOGIN PAGES
@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/register')
def register():
    return render_template('registration.html')


#RECIPES PAGES

@app.get('/recipes')
def recipes():
    all_recipes = recipe_repository_singleton.get_all_recipes()
    return render_template('recipes.html', recipes=all_recipes)

@app.get('/recipes/<int:recipe_id>')
def get_recipe():
    return('get_single_recipe.html')

@app.get('/recipes/new')
def create_recipe():
    return()

@app.get('/recipes/<int:recipe_id>/edit')
def get_edit_recipe():
    return('edit_recipe.html')

@app.post('/recipes/int:recipe_id>')
def update_recipe():
    return redirect()

@app.post('/recipes/<int:recipe_id>/delete')
def delete_recipe():
    return()

#POST PAGES
#TODO: