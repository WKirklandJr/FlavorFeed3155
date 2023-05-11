from flask import Blueprint, request, redirect, render_template
from src.repositories.recipe_repository import recipe_repository_singleton
from src.repositories.tags_repository import tag_repository_singleton

search_router = Blueprint('search', __name__, url_prefix='/search')

@search_router.get('/<tagname>')
def search_tag(tagname):
    tag = tag_repository_singleton.get_tag(tagname)
   
    return render_template('tagged_posts.html', tag=tag)

@search_router.get('')
def search_recipe():
    q = request.args.get('q')
    if q != '':
        found_recipes = recipe_repository_singleton.search_recipe(q)
        return render_template('search_posts.html', search_active=True, recipes=found_recipes, search_query=q)
    else:
        return redirect('/')
