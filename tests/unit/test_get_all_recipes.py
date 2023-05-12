from src.repositories.recipe_repository import recipe_repository_singleton
from src.repositories.user_repository import user_repository_singleton
from app import app
from src.models import db, Recipe, User

def test_get_all_users():
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
        
        all_recipes = recipe_repository_singleton.get_all_recipes()
        
        assert recipe in all_recipes
        assert recipe_2 in all_recipes