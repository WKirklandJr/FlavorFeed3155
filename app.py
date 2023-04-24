from flask import Flask, redirect, render_template, request, abort
from dotenv import load_dotenv
import os

from src.models import User, db
from security import bcrypt
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
bcrypt.init_app(app)

#--------- HOME PAGES

@app.get('/')
def index():
    return render_template('index.html')


@app.get('/about')
def about():
    return render_template('about.html')


#--------- USER PAGES
@app.get('/profile')
def edit_profile():
    return render_template('edit_profile.html')



#--------- RECIPES PAGES

@app.get('/recipes')
def recipes():
    all_recipes = recipe_repository_singleton.get_all_recipes()
    return render_template('recipes.html', recipes=all_recipes)

@app.get('/recipes/<int:recipe_id>')
def get_recipe(recipe_id):

    single_recipe = recipe_repository_singleton.get_recipe_by_id(recipe_id)
    return render_template('get_single_recipe.html', recipe=single_recipe)

@app.get('/recipes/<int:recipe_id>/edit')
def get_edit_recipe(recipe_id):

    single_recipe = recipe_repository_singleton.get_recipe_by_id(recipe_id)
    return render_template('edit_recipe.html', recipe=single_recipe)

@app.get('/recipes/new')
def create_recipe_page():
    return render_template('create_recipe.html')

@app.post('/recipes')
def create_recipe():
    
    #!!TODO finish implementing create_recipe

    #TODO retrieve duration int value from form
    #  and add to created_recipe parameters
    is_vegan = request.form.get('is_vegan', None,type=bool)

    #TODO retrieve duration int value from form
    #  and add to created_recipe parameters
    duration = request.form.get('duration', type=int)

    title = request.form.get('title', '')
    ingredients = request.form.get('ingredients', '')
    equipment = request.form.get('equipment', '')
    difficulty = request.form.get('difficulty', '')
    text = request.form.get('text', '')
 

    #Values to implement later
    #image =
    #time_posted =
    #tags = 

    #TODO: add is_Vegan and duration conditions to if statement
    if title =='' or ingredients=='' or equipment=='' or difficulty =='' or text =='':
        abort(400)

    created_recipe = recipe_repository_singleton.create_recipe\
        (title, is_vegan, ingredients,equipment,duration,difficulty,text)
    return redirect(f'/recipes/{created_recipe.recipe_id}')


@app.post('/recipes/int:recipe_id>')
def update_recipe():
    #TODO: Implement Update Recipe
    return redirect(f'/recipes/<int:recipe_id>')

@app.post('/recipes/<int:recipe_id>/delete')
def delete_recipe():
    #TODO: Implement Delete Recipe
    return()

#POST PAGES


#LOGIN PAGES
@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/register')
def register():
    return render_template('registration.html')

@app.post('/register')
def signup():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    if not email or not username or not password:
        abort(400)

    hashed_password = bcrypt.generate_password_hash(password).decode()

    new_user = User(email, username, hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/login')
 