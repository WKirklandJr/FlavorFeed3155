from flask import Blueprint, session, render_template, request, redirect, abort
from src.models import db, User, Recipe, Tag
from src.repositories.recipe_repository import recipe_repository_singleton
from werkzeug.utils import secure_filename
import os, datetime

recipes_router = Blueprint('recipes', __name__, url_prefix='/recipes')

# GET all recipes
@recipes_router.get('')
def recipes():
    all_recipes = recipe_repository_singleton.get_all_recipes()
    return render_template('recipes.html', recipes=all_recipes)

# GET single recipe
@recipes_router.get('/<int:recipe_id>')
def get_recipe(recipe_id):

    single_recipe = recipe_repository_singleton.get_recipe_by_id(recipe_id)
    author_info = User.query.filter_by(user_id = single_recipe.user_id).first()

    return render_template('get_single_recipe.html', recipe=single_recipe, author=author_info)

# GET new recipe
@recipes_router.get('/new')
def create_recipe_page():
    return render_template('create_recipe.html')

# POST new recipe
@recipes_router.post('')
def create_recipe():
    # Get variables from form
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
        existing_tag = Tag.query.filter_by(tagname = tagname).first()

        if existing_tag is not None:     
            created_recipe.tags.append(existing_tag)

        if existing_tag is None:
            created_recipe.tags.append(Tag(tagname))
                     
    db.session.commit()

    return redirect(f'/recipes/{created_recipe.recipe_id}')

# GET edit recipe
@recipes_router.get('/<int:recipe_id>/edit')
def get_edit_recipe(recipe_id):

    single_recipe = recipe_repository_singleton.get_recipe_by_id(recipe_id)
    return render_template('edit_recipe.html', recipe=single_recipe)

# POST edit recipe
@recipes_router.post('/<int:recipe_id>/edit')
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
    
    #post_tags = Tag.query.filter_by(db.recipe_tag).all()
    #update_recipe.tags.remove(post_tags)

    for tagname in taglist:  
        
        existing_tag = Tag.query.filter_by(tagname = tagname).first()

        if existing_tag is not None:     
            updated_recipe.tags.append(existing_tag)

        if existing_tag is None:
            updated_recipe.tags.append(Tag(tagname))
                     
    db.session.commit()

    return redirect(f'/recipes/{recipe_id}')

@recipes_router.post('/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    recipe_repository_singleton.delete_recipe(recipe_id)
    return redirect('/recipes')

#---------- RECIPE COMMENTS
@recipes_router.post('<int:recipe_id>/comment')
def post_comment(recipe_id):
    #TODO: request.form.get comment data and publish a post on the recipe page
    # use the article below for help:
    # https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-sqlalchemy

    return redirect(f'/recipes/{recipe_id}')
