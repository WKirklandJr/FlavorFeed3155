from src.models import db, Recipe

class RecipeRepository:

    def get_all_recipes(self):
        # Get all recipes
        # This will need to change as the number of recipes increase
        all_recipes = Recipe.query.all()
        return all_recipes
    
    def get_recipe_by_id(self, recipe_id):
        
        get_recipe = Recipe.query.get(recipe_id)
        return get_recipe
    
# Singleton: Restricts the instantiation of a class to a single instance
recipe_repository_singleton = RecipeRepository()
