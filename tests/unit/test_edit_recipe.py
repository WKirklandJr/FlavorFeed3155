from src.repositories.recipe_repository import recipe_repository_singleton
from app import app
from src.models import db, Recipe

def test_edit_recipe():
    with app.app_context():
        db.session.query(Recipe).delete()
        db.session.commit()
        
        recipe = recipe_repository_singleton.create_recipe('test_recipe'\
            , False, 'chicken, rice, beans', 'pan, spatula', 30, 'Intermediate'\
            , 'cook it', '.../static/post-images/chicken.png', '2023-05-11 15:42:12-07', '1')
        recipe_id = recipe.recipe_id

        recipe_repository_singleton.update_recipe(recipe_id, 'Delicious Chicken Recipe'\
            , False, 'chicken, rice, beans, salt, pepper', 'pan, spatula', 35, 'Intermediate'\
            , 'cook it', '.../static/post-images/chicken.png')
        
        assert recipe.title == 'Delicious Chicken Recipe'
        assert recipe.ingredients == 'chicken, rice, beans, salt, pepper'
        assert recipe.equipment == 'pan, spatula'
        assert recipe.duration == 35
        assert recipe.difficulty == 'Intermediate'