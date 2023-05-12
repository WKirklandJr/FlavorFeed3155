from flask import Blueprint, session, render_template, request, redirect, abort
from src.models import db, Recipe, Tag, Bookmark
from src.repositories.user_repository import user_repository_singleton
from src.repositories.recipe_repository import recipe_repository_singleton
from src.repositories.tags_repository import tag_repository_singleton
from src.repositories.comment_repository import comment_repository_singleton
from werkzeug.utils import secure_filename
import os, datetime

recipes_router = Blueprint('recipes', __name__, url_prefix='/recipes')

# GET all recipes
@recipes_router.get('')
def recipes():
    tab_title='All Recipes'
    all_recipes = recipe_repository_singleton.get_all_recipes()
    
    return render_template('recipes.html', recipes=all_recipes, title=tab_title)

# GET single recipe
@recipes_router.get('/<int:recipe_id>')
def get_recipe(recipe_id):

    single_recipe = recipe_repository_singleton.get_recipe_by_id(recipe_id)
    recipe_comments = comment_repository_singleton.get_comment_by_recipe_id(recipe_id)

    isbookmarked = False
    if 'user' in session:
        current_recipe = recipe_repository_singleton.filter_recipe_by_id(recipe_id)

        for bookmark in current_recipe.bookmark:
            if bookmark.user_id ==  session['user']['user_id']:
                isbookmarked = True   
    
    return render_template('get_single_recipe.html', recipe=single_recipe, comments=recipe_comments, isbookmarked=isbookmarked)


#GET beginner recipes
@recipes_router.get('/beginners')
def get_beginner():
    beginner_recipes = recipe_repository_singleton.get_recipe_by_difficulty('Beginner')
    tab_title='For Beginners'

    return render_template('recipes.html', recipes=beginner_recipes, title=tab_title)

#GET vegan recipes
@recipes_router.get('/vegan')
def get_vegan():
    vegan_recipes = recipe_repository_singleton.get_recipe_by_vegan(True)
    tab_title='Vegan Recipes'

    return render_template('recipes.html', recipes=vegan_recipes, title=tab_title)

#GET < 5 ingredient recipes

@recipes_router.get('/fiveingredients')
def get_5_ingredients():
    all_recipes = recipe_repository_singleton.get_all_recipes()
    subfive = []

    for recipe in all_recipes:
        ingredientlist = recipe.ingredients.split(",")
        if len(ingredientlist) < 5:
            subfive.append(recipe)
             
    tab_title='< 5 Ingredient Recipes'
    return render_template('recipes.html', recipes=subfive, title=tab_title)

#GET hour less recipes 
@recipes_router.get('/hour')
def get_hour_recipes():
    
    hour_recipe = recipe_repository_singleton.get_recipe_by_duration('61')
    tab_title='< Hour Recipes'

    return render_template('recipes.html', recipes=hour_recipe, title=tab_title)



# GET new recipe
@recipes_router.get('/new')
def create_recipe_page():

    if 'user' not in session:
        return redirect('/login')
    
    return render_template('create_recipe.html')

# POST new recipe
@recipes_router.post('/new')
def create_recipe():

    if 'user' not in session:
        return redirect('/login')

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
        user_id = session['user']['user_id']

    tagstring = request.form.get('tags')
    taglist = tagstring.split(",")

    created_recipe = recipe_repository_singleton.create_recipe\
        (title, is_vegan, ingredients, equipment, duration, difficulty, instructions, img_filename, date_posted,user_id)
    

    for tagname in taglist:  
        
        existing_tag = tag_repository_singleton.get_tag(tagname)

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
    
    updated_recipe.tags.clear()
    
    for tagname in taglist:  
        
        existing_tag = tag_repository_singleton.get_tag(tagname)

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

@recipes_router.post('/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    recipe_repository_singleton.delete_recipe(recipe_id)
    return redirect('/recipes')

#---------- RECIPE COMMENTS
@recipes_router.post('/<int:recipe_id>/comment')
def post_comment(recipe_id):
    if 'user' not in session:
        return redirect('/login')
    
    data = request.form.get('comment')

    if not data:
        abort(400)

    comment_repository_singleton.create_comment(session['user']['user_id'], recipe_id, data)

    return redirect(f'/recipes/{recipe_id}')

@recipes_router.post('/<int:recipe_id>/deletecomment/<int:comment_id>')
def delete_comment(comment_id, recipe_id): 
    comment_repository_singleton.delete_comment(comment_id)
    return redirect(f'/recipes/{recipe_id}')

#---------- BOOKMARKS
@recipes_router.post('/<int:recipe_id>/bookmark')
def bookmark_post(recipe_id):
    
    if 'user' not in session:
        return redirect('/login')
    
    current_recipe = recipe_repository_singleton.filter_recipe_by_id(recipe_id)
    get_user = user_repository_singleton.filter_user_by_id(session['user']['user_id'])
    current_recipe.bookmark.append(get_user)

    db.session.commit()

    return redirect(f'/recipes/{recipe_id}')

@recipes_router.post('/<int:recipe_id>/unbookmark')
def unbookmark_post(recipe_id):
    
    if 'user' not in session:
        return redirect('/login')

    current_recipe = recipe_repository_singleton.filter_recipe_by_id(recipe_id)
    get_user = user_repository_singleton.filter_user_by_id(session['user']['user_id'])
    current_recipe.bookmark.remove(get_user)
    db.session.commit()
    return redirect(f'/recipes/{recipe_id}')
