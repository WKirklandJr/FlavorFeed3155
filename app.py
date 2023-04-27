from flask import Flask, session, redirect, render_template, request, abort
from dotenv import load_dotenv
import os, datetime
from werkzeug.utils import secure_filename

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

#--------- HOME PAGES

@app.get('/')
def index():
    

    return render_template('index.html')


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

    return redirect('/')

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
    #get variables from form
    is_vegan = bool(request.form.get('is_vegan'))
    duration = request.form.get('duration')
    title = request.form.get('title')
    ingredients = request.form.get('ingredients')
    equipment = request.form.get('equipment')
    difficulty = request.form.get('difficulty')
    instructions = request.form.get('instructions')
    
    if not title or not ingredients or not equipment or not duration or not difficulty or not instructions:
        print('One or more fields are missing or empty')
        abort(400)


    #image file data
    print(request.files)
    if 'recipe_image' not in request.files:
        print('No recipe image file was uploaded')
        abort(400)
    
    recipe_image = request.files['recipe_image']
    if recipe_image.filename == '' or recipe_image.filename.rsplit('.', 1)[1] not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        print('Invalid file format for recipe image')
        abort(400)

    img_filename = secure_filename(recipe_image.filename)
    recipe_image.save(os.path.join('static', 'post-images', img_filename))

    #datetime data
    date_posted = datetime.datetime.now()
    print(date_posted.ctime())

    #datetime data
    created_recipe = recipe_repository_singleton.create_recipe\
        (title, is_vegan, ingredients, equipment, duration, difficulty, instructions, img_filename, date_posted)
    return redirect(f'/recipes/{created_recipe.recipe_id}')



@app.post('/recipes/int:recipe_id>')
def update_recipe():
    recipe_repository_singleton.update_recipe(recipe_id)
    return redirect(f'/recipes/<int:recipe_id>')


@app.post('/recipes/<int:recipe_id>/delete')
def delete_recipe():
    recipe_repository_singleton.delete_recipe(recipe_id)
    return redirect('/recipes')

#POST PAGES

# User pages
@app.get('/user/profile')
def profile():
    if 'user' not in session:
        return redirect('/login')
    
    return render_template('get_single_profile.html')

@app.get('/profile')
def edit_profile():
    return render_template('edit_profile.html')

