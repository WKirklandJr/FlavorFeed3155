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

@app.get('/')
def index():
    return render_template('index.html')

@app.get('/recipes')
def recipes():
    all_recipes = recipe_repository_singleton.get_all_recipes()
    return render_template('recipes.html', recipes=all_recipes)

@app.get('/recipes/<id>')
def get_recipe():
    return()

@app.get('/recipes/new')
def new_recipe():
    return()

@app.post('/recipes')
def create_recipe():
    return()

@app.get('/recipes/<id>/edit')
def edit_recipe():
    return()

@app.post('/recipes/<id>')
def update_recipe():
    return()

@app.post('/recipes/<id>/delete')
def delete_recipe():
    return()
