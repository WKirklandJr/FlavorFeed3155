from flask import Flask, session, redirect, render_template, request, abort
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

app.secret_key = os.getenv('APP_SECRET')

db.init_app(app)
bcrypt.init_app(app)

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
def login_form():
    if 'user' in session:
        return redirect('/user/profile')
    
    return render_template('login.html')

@app.post('/login')
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        abort(400)

    existing_user = User.query.filter_by(username=username).first()

    if not existing_user:
        return redirect('/login')
    
    if not bcrypt.check_password_hash(existing_user.password, password):
        return redirect('/login')
    
    session['user'] = {
        'username': username
    }

    return redirect('/user/profile')

@app.get('/register')
def register():
    if 'user' in session:
        return redirect('user/profile')
    
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

@app.get('/logout')
def logout():
    if 'user' in session:
        del session['user']
    return redirect('/login')

#RECIPES PAGES

@app.get('/recipes')
def recipes():
    all_recipes = recipe_repository_singleton.get_all_recipes()
    return render_template('recipes.html', recipes=all_recipes)

@app.get('/recipes/<int:recipe_id>')
def get_recipe(recipe_id):

    single_recipe = recipe_repository_singleton.get_recipe_by_id(recipe_id)
    return render_template('get_single_recipe.html', recipe=single_recipe)


@app.get('/recipes/new')
def create_recipe():
    return render_template('create_recipe.html')

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

# User pages
@app.get('/user/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    
    return render_template('get_single_profile.html')
