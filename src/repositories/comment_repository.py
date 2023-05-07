from src.models import db, user_recipe_comment

class CommentRepository:

    def create_comment(self, user_id, recipe_id, comment):
        new_comment = user_recipe_comment(user_id, recipe_id, comment)

        db.session.add(new_comment)
        db.session.commit()

        return new_comment

    def get_comment_by_recipe_id(self, recipe_id):
        get_comments = db.session.query(user_recipe_comment).filter_by(recipe_id = recipe_id).all()

        return get_comments
    
    def get_comment_by_user_id(self, user_id):
        get_comments = db.session.query(user_recipe_comment).filter_by(user_id = user_id).all()

        return get_comments
    
# Singleton: Restricts the instantiation of a class to a single instance   
comment_repository_singleton = CommentRepository()
