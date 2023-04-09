from src.models import db, Recipe

class RecipeRepository:

    def get_all_recipes(self):
        # Get all recipes
        # This will need to change as the number of recipes increase
        all_recipes = Recipe.query.all()
        return all_recipes
    
# Singleton: Restricts the instantiation of a class to a single instance
recipe_repository_singleton = RecipeRepository()
