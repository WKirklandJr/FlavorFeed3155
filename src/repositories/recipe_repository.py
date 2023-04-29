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

    def create_recipe(self, title, is_vegan, ingredients, equipment, duration, difficulty, instructions, recipe_image, date_posted):
        # Update parameters as new variables are implemented
        create_recipe = Recipe(title, is_vegan, ingredients, equipment,
                               duration, difficulty, instructions, recipe_image, date_posted)
        db.session.add(create_recipe)
        db.session.commit()
        return create_recipe

    def update_recipe(recipe_id):
        # TODO: edit a specific recipe in the db
        recipe_to_update = Recipe.query.get(recipe_id)
        if request.method == "POST":
            recipe_to_update.recipe_title = request.form['title']
            recipe_to_update.recipe_is_vegan = request.form['is_vegan']
            recipe_to_update.recipe_ingredients = request.form['ingredients']
            recipe_to_update.recipe_equipment = request.form['equipment']
            recipe_to_update.recipe_duration = request.form['duration']
            recipe_to_update.recipe_difficulty = request.form['difficulty']
            recipe_to_update.recipe_instructions = request.form['instructions']
            recipe_to_update.recipe_recipe_image = request.form['recipe_image']
            try:
                db.session.commit()
                return recipe_to_update
            except:
                return abort(400)

    def delete_recipe(recipe_id):
        # TODO: delete a specific recipe in the db
        recipe_to_delete = Recipe.query.get_or_404(recipe_id)
        db.session.delete(recipe_to_delete)
        db.sesion.commit()
        return recipe_to_delete


# Singleton: Restricts the instantiation of a class to a single instance
recipe_repository_singleton = RecipeRepository()
