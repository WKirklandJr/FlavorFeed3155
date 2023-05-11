import pytest
from app import app
from src.models import Recipe
from src.repositories.recipe_repository import recipe_repository_singleton



def test_all_recipes_page():
    test_app = app.test_client()

    #no input
    response = test_app.get('/recipes')
    data = response.data.decode('utf-8')
    assert response.status_code == 200
    assert '<h1 class="m-3 pt-4 ml-5">' in data
    

    #one input
    # recipe =  Recipe('Test Recipe', False, 'ingredients', 'equipment', '10', 'Beginner', 'instructions', 'recipe_image.png', 'date_posted', 3)

    # recipe_repository_singleton.create_recipe(recipe)
    # response = test_app.get('/recipes')
    # data = response.data.decode('utf-8')
    # assert response.status_code == 200
    # assert '<div class="card query-postcard ">'in data
    
