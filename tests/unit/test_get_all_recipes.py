from src.repositories.recipe_repository import recipe_repository_singleton
from app import app
from src.models import db, Recipe

def test_create_recipe():
    with app.app_context():
        db.session.query(Recipe).delete()
        db.session.commit()

        recipe = recipe_repository_singleton.create_recipe('test_recipe'\
            , False, 'chicken, rice, beans', 'pan, spatula', 30, 'Intermediate'\
            , 'cook it', '.../static/post-images/chicken.png', '2023-05-11 15:42:12-07', '1')
        
        recipe_2 = recipe_repository_singleton.create_recipe('test_recipe_2'\
            , False, 'chicken, rice, beans, broccoli', 'pan, spatula', 30, 'Intermediate'\
            , 'cook it', '.../static/post-images/chicken.png', '2023-05-11 15:42:12-07', '1')
        
        all_recipes = recipe_repository_singleton.get_all_recipes()
        
        assert recipe in all_recipes
        assert recipe_2 in all_recipes