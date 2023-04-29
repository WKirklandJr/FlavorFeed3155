from src.models import db, User

class UserRepository:

    def get_all_users():
        return()
    
    def get_user_by_id(self, user_id):
        get_user = User.query.get(user_id)
        return get_user
    
user_repository_singleton = UserRepository()
