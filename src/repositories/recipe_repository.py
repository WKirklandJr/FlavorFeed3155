from src.models import db, Recipe


class RecipeRepository:

    def get_all_recipes(self):
        # Get all recipes
        all_recipes = Recipe.query.all()
        return all_recipes

    def get_recipe_by_id(self, recipe_id):
        get_recipe = Recipe.query.get(recipe_id)
        return get_recipe

    def create_recipe(self, title, is_vegan, ingredients, equipment, duration, difficulty, instructions, recipe_image, date_posted, user_id):
        # Update parameters as new variables are implemented
        create_recipe = Recipe(title, is_vegan, ingredients, equipment,
                               duration, difficulty, instructions, recipe_image, date_posted, user_id)
        db.session.add(create_recipe)
        db.session.commit()
        return create_recipe

    def update_recipe(self, recipe_id, title, is_vegan, ingredients, equipment, duration, difficulty, instructions, recipe_image):
        update_recipe = Recipe.query.get(recipe_id)
        update_recipe.title = title
        update_recipe.is_vegan = is_vegan
        update_recipe.ingredients = ingredients
        update_recipe.equipment = equipment
        update_recipe.duration = duration
        update_recipe.difficulty = difficulty
        update_recipe.instructions = instructions
        update_recipe.recipe_image = recipe_image
        db.session.commit()
        return update_recipe

    def delete_recipe(recipe_id):
        # TODO: delete a specific recipe in the db
        recipe_to_delete = Recipe.query.get_or_404(recipe_id)
        db.session.delete(recipe_to_delete)
        db.sesion.commit()
        return recipe_to_delete


# Singleton: Restricts the instantiation of a class to a single instance
recipe_repository_singleton = RecipeRepository()
