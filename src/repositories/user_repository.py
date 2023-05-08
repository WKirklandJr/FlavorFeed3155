from src.models import db, User

class UserRepository:

    def create_user(self, email, username, password):
        new_user = User(email, username, password)
        return new_user

    def get_all_users():
        all_users = User.query.all()
        return all_users

    def get_user_by_id(self, user_id):
        get_user = User.query.get(user_id)
        return get_user
    
    def filter_user_by_id(self, user_id):
        get_user = User.query.filter_by(user_id=user_id).first()
        return get_user

    def get_user_by_username(self, username):
        get_user = User.query.filter_by(username=username).first()
        return get_user
    
    def get_user_by_recipe(self, recipe):
        get_user = User.query.filter_by(user_id = recipe.user_id).first()
        return get_user
    
    def get_user_by_comment(self, comment):
        get_user = User.query.filter_by(user_id = comment.user_id).first()
        return get_user

    def update_user(self, user_id, username , skill, social, about, profile_picture):
        update_user = User.query.get(user_id)
        update_user.username = username
        update_user.skill = skill
        update_user.social = social
        update_user.about = about
        update_user.profile_picture = profile_picture
        db.session.commit()
        return update_user


user_repository_singleton = UserRepository()
