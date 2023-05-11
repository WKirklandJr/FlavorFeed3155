from src.models import db, Recipe

class RecipeRepository:

    def get_all_recipes(self):
        # Get all recipes
        all_recipes = Recipe.query.all()
        return all_recipes

    def get_recipe_by_id(self, recipe_id):
        get_recipe = Recipe.query.get(recipe_id)
        return get_recipe
    
    def filter_recipe_by_id(self, recipe_id):
        get_recipe = Recipe.query.filter_by(recipe_id = recipe_id).first()
        return get_recipe
    
    def get_recipes_by_user(self, user_id):
        get_recipe = Recipe.query.filter_by(user_id = user_id).all()
        return get_recipe
    
    def get_recipe_by_difficulty(self, difficulty):
        get_recipe = Recipe.query.filter_by(difficulty = difficulty).all()
        return get_recipe
    

    def get_recipe_by_vegan(self, isvegan):
        get_recipe = Recipe.query.filter_by(is_vegan = isvegan).all()
        return get_recipe
    
    
    def get_recipe_by_duration(self, duration):
        get_recipe = Recipe.query.filter(Recipe.duration < duration).all()
        return get_recipe


    def get_recipes_by_bookmark(self, user_id):
        get_recipe = Recipe.query.join(Recipe.bookmark).filter_by(user_id = user_id).all()
        return get_recipe
    

    def get_all_bookmarked_recipes(self):
        bookmarked_recipes = Recipe.query.join(Recipe.bookmark).all()

        for recipe in bookmarked_recipes:
            recipe.num_bookmarks = len(recipe.bookmark)

        bookmarked_recipes_sorted = sorted(bookmarked_recipes, key=lambda x : x.num_bookmarks, reverse=True)
        return bookmarked_recipes_sorted


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

        return update_recipe

    def delete_recipe(self, recipe_id):
        # TODO: delete a specific recipe in the db
        recipe_to_delete = Recipe.query.filter_by(recipe_id = recipe_id).first_or_404()
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return recipe_to_delete
    
    def search_recipe(self, title):
        found_recipes = Recipe.query.filter(Recipe.title.ilike(f'%{title}%')).all()
        return found_recipes

# Singleton: Restricts the instantiation of a class to a single instance
recipe_repository_singleton = RecipeRepository()
