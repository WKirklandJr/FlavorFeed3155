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
    

    def create_recipe(self, title, is_vegan, ingredients,equipment,duration,difficulty,instructions,recipe_image,date_posted):
        # Update parameters as new variables are implemented
        create_recipe = Recipe(title, is_vegan, ingredients,equipment,duration,difficulty,instructions,recipe_image,date_posted)
        db.session.add(create_recipe)
        db.session.commit()
        return create_recipe
    
    def update_recipe():
        #TODO: edit a specific recipe in the db
        return None

    def delete_recipe():
        #TODO: delete a specific recipe in the db
        return None

        

    
# Singleton: Restricts the instantiation of a class to a single instance
recipe_repository_singleton = RecipeRepository()
