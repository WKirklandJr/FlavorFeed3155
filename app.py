from flask import Flask, session, redirect, render_template, request, abort
from dotenv import load_dotenv
import os, datetime, functools
from werkzeug.utils import secure_filename

from src.models import User, Tag, Recipe, db
from security import bcrypt
from src.repositories.recipe_repository import recipe_repository_singleton
from src.repositories.user_repository import user_repository_singleton



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
    

#--------- HOME PAGES

@app.get('/')
def index():    
    all_recipes = recipe_repository_singleton.get_all_recipes()
    
    return render_template('index.html', recipes=all_recipes )


@app.get('/about')
def about():
    return render_template('about.html')


#-----LOGIN PAGES
@app.get('/login')
def login_form():
    if 'user' in session:
        return redirect('/')
    
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
        'username': existing_user.username,
        'user_id': existing_user.user_id
    }

    return redirect('/')

@app.get('/register')
def register():
    if 'user' in session:
        return redirect('/')
    
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
    author_info = User.query.filter_by(user_id = single_recipe.user_id).first()




    return render_template('get_single_recipe.html', recipe=single_recipe, author=author_info)

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


    if 'user' in session:
        user_id= session['user']['user_id']



    tagstring = request.form.get('tags')
    taglist = tagstring.split(",")

    created_recipe = recipe_repository_singleton.create_recipe\
        (title, is_vegan, ingredients, equipment, duration, difficulty, instructions, img_filename, date_posted,user_id)
    
    for tagname in taglist:  
        existing_tag = Tag.query.filter_by(tagname = tagname.lower()).first()

        if existing_tag is not None:     
            created_recipe.tags.append(existing_tag)

        if existing_tag is None:
            if tagname[0] == ' ':
                cropped_tag = tagname[1:]
                created_recipe.tags.append(Tag(cropped_tag.lower()))
            else:
                created_recipe.tags.append(Tag(tagname.lower()))
                     
    db.session.commit()

    return redirect(f'/recipes/{created_recipe.recipe_id}')



@app.post('/recipes/<int:recipe_id>/edit')
def update_recipe(recipe_id):
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

 
    recipe_repository_singleton.update_recipe(recipe_id, title, is_vegan,\
        ingredients, equipment, duration, difficulty, instructions, img_filename)
    
   
    tagstring = request.form.get('tags')
    taglist = tagstring.split(",")
     
    updated_recipe = Recipe.query.filter_by(recipe_id = recipe_id).first()
    
    

    updated_recipe.tags.clear()

    for tagname in taglist:  
        
        existing_tag = Tag.query.filter_by(tagname = tagname.lower()).first()

        if existing_tag is not None:     
            updated_recipe.tags.append(existing_tag)

        if existing_tag is None:
            if tagname[0] == ' ':
                cropped_tag = tagname[1:]
                updated_recipe.tags.append(Tag(cropped_tag.lower()))
            else:    
                updated_recipe.tags.append(Tag(tagname.lower()))
                     
    db.session.commit()

    return redirect(f'/recipes/{recipe_id}')


@app.post('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    recipe_repository_singleton.delete_recipe(recipe_id)
    return redirect('/recipes')



#---------- RECIPE COMMENTS
@app.post('/recipes/<int:recipe_id>')
def post_comment(recipe_id):
    #TODO: request.form.get comment data and publish a post on the recipe page
    # use the article below for help:
    # https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-sqlalchemy

    return redirect(f'/recipes/{recipe_id}')


#-------------- RECIPE TAGS
@app.get('/search/<tagname>')
def search_tag(tagname):
    tag = Tag.query.filter_by(tagname=tagname).first_or_404()
    return render_template('search_posts.html', tag=tag)


#-------------- USER PAGES


@app.get('/users/<int:user_id>')
def get_user(user_id):

    single_user = user_repository_singleton.get_user_by_id(user_id)

    return render_template('get_single_profile.html', user=single_user)


@app.get('/profile/<int:user_id>/edit')
def get_edit_profile(user_id):
    
    if 'user' not in session:
        return redirect('/login')
    

    session_user = db.session.query(User).filter(User.username == session.get('user')['username']).first()
    user_id = session_user.user_id

    if user_id != session_user.user_id:
        print('Incorrect session user. Access denied.')
        abort(400) 
    else:   
        single_user = user_repository_singleton.get_user_by_id(user_id)
        return render_template('edit_profile.html', user=single_user)


@app.post('/profile/<int:user_id>/edit')
def update_user(user_id):

    username = request.form.get('username')
    skill = request.form.get('skill')
    social = request.form.get('social')
    about  = request.form.get('about')


     #image file data
    print(request.files)
    if 'profile_picture' not in request.files:
        print('No profile image file was uploaded')
        abort(400)
    
    profile_picture = request.files['profile_picture']
    if profile_picture.filename == '' or profile_picture.filename.rsplit('.', 1)[1] not in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
        print('Invalid file format for profile image')
        abort(400)

    img_filename = secure_filename(profile_picture.filename)
    profile_picture.save(os.path.join('static', 'profile-images', img_filename))


    user_repository_singleton.update_user(user_id, username, skill, social, about, img_filename)
    
    return redirect(f'/users/{user_id}')
