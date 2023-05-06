from flask import Blueprint, session, render_template, request, redirect, abort
from src.models import db, User
from src.repositories.recipe_repository import recipe_repository_singleton
from security import bcrypt

home_router = Blueprint('home', __name__, url_prefix='/')

# GET index
@home_router.get('')
def index():    
    all_recipes = recipe_repository_singleton.get_all_recipes()
    
    return render_template('index.html', recipes=all_recipes )

# GET about
@home_router.get('about')
def about():
    return render_template('about.html')

# GET register
@home_router.get('register')
def register():
    if 'user' in session:
        return redirect('/')
    
    return render_template('registration.html')

# POST register
@home_router.post('register')
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

# GET login
@home_router.get('login')
def login_form():
    if 'user' in session:
        return redirect('/')
    
    return render_template('login.html')

# POST login
@home_router.post('login')
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
        'username': existing_user.username,
        'user_id': existing_user.user_id
    }

    return redirect('/')

# GET logout
@home_router.get('logout')
def logout():
    if 'user' in session:
        del session['user']
    return redirect('/login')
