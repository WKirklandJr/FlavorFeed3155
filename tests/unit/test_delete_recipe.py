from src.repositories.recipe_repository import recipe_repository_singleton
from src.repositories.user_repository import user_repository_singleton
from app import app
from src.models import db, Recipe, User

def test_create_recipe():
    with app.app_context():
        db.session.query(Recipe).delete()
        db.session.query(User).delete()
        db.session.commit()

        user = user_repository_singleton.create_user('test@example.com', 'testuser', 'password123')

        recipe = recipe_repository_singleton.create_recipe('test_recipe'\
            , False, 'chicken, rice, beans', 'pan, spatula', 30, 'Intermediate'\
            , 'cook it', '.../static/post-images/chicken.png', '2023-05-11 15:42:12-07', user.user_id)
        
        recipe_2 = recipe_repository_singleton.create_recipe('test_recipe_2'\
            , False, 'chicken, rice, beans, broccoli', 'pan, spatula', 30, 'Intermediate'\
            , 'cook it', '.../static/post-images/chicken.png', '2023-05-11 15:42:12-07', user.user_id)
        
        recipe_repository_singleton.delete_recipe(recipe_2.recipe_id)
        
        assert recipe in recipe_repository_singleton.get_all_recipes()
        assert recipe_2 not in recipe_repository_singleton.get_all_recipes()